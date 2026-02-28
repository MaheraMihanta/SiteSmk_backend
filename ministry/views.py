from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ChatMessage, Entity, EntityAccount, FinanceEntry, NewsItem, Post, PostMedia
from .serializers import (
    ChatMessageCreateSerializer,
    ChatMessageSerializer,
    EntityDetailSerializer,
    EntitySerializer,
    FinanceSummarySerializer,
    NewsItemSerializer,
    PostCreateSerializer,
    PostSerializer,
    ProfileSerializer,
    ProfileUpdateSerializer,
    ProvisionEntityAccountSerializer,
)
from .services import generate_password, provision_entity_account


class EntityListView(generics.ListAPIView):
    queryset = Entity.objects.filter(is_active=True).order_by('name')
    serializer_class = EntitySerializer
    permission_classes = [permissions.AllowAny]


class EntityDetailView(generics.RetrieveAPIView):
    queryset = Entity.objects.filter(is_active=True)
    serializer_class = EntityDetailSerializer
    permission_classes = [permissions.AllowAny]


class NewsListView(generics.ListAPIView):
    serializer_class = NewsItemSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return NewsItem.objects.filter(is_published=True)


class FinanceSummaryView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        entries = list(FinanceEntry.objects.select_related('entity').all())
        summary_payload = FinanceSummarySerializer.from_entries(entries)
        serializer = FinanceSummarySerializer(summary_payload)
        return Response(serializer.data)


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.select_related('author', 'author__entity_account__entity').prefetch_related('media')

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCreateSerializer
        return PostSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save(author=request.user)

        for uploaded in request.FILES.getlist('media'):
            media_type = self._detect_media_type(uploaded.content_type)
            PostMedia.objects.create(
                post=post,
                file=uploaded,
                media_type=media_type,
                name=uploaded.name,
            )

        output = PostSerializer(post, context=self.get_serializer_context())
        headers = self.get_success_headers(output.data)
        return Response(output.data, status=status.HTTP_201_CREATED, headers=headers)

    @staticmethod
    def _detect_media_type(content_type: str | None) -> str:
        if not content_type:
            return 'document'
        if content_type.startswith('image/'):
            return 'photo'
        if content_type.startswith('video/'):
            return 'video'
        return 'document'


class ChatMessageListCreateView(generics.ListCreateAPIView):
    queryset = ChatMessage.objects.select_related('author').filter(room='general', is_public=True)

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ChatMessageCreateSerializer
        return ChatMessageSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().order_by('-created_at')[:50]
        serializer = ChatMessageSerializer(list(reversed(queryset)), many=True, context=self.get_serializer_context())
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class MyProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def _build_payload(self, request, user):
        entity_account = getattr(user, 'entity_account', None)
        avatar = ''
        cover = ''
        entity_name = ''
        city = ''
        friends = 0

        if entity_account:
            entity_name = entity_account.entity.name
            city = entity_account.entity.city
            friends = entity_account.entity.members
            if entity_account.avatar:
                avatar = request.build_absolute_uri(entity_account.avatar.url)
            if entity_account.cover:
                cover = request.build_absolute_uri(entity_account.cover.url)

        profile_payload = {
            'name': user.get_display_name(),
            'bio': entity_account.bio if entity_account else '',
            'entity': entity_name,
            'city': city,
            'joinedDate': user.date_joined.date().isoformat(),
            'postsCount': user.posts.count(),
            'friends': friends,
            'email': user.email,
            'role': user.role,
            'avatar': avatar,
            'cover': cover,
        }

        recent_posts = Post.objects.filter(author=user).prefetch_related('media').order_by('-created_at')[:10]
        return {
            'profile': ProfileSerializer(profile_payload).data,
            'recentPosts': PostSerializer(recent_posts, many=True, context={'request': request}).data,
        }

    def get(self, request):
        return Response(self._build_payload(request, request.user))

    def patch(self, request):
        serializer = ProfileUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        user = request.user
        validated = serializer.validated_data
        user_fields_to_update = []

        if 'display_name' in validated:
            user.display_name = validated['display_name'].strip()
            user_fields_to_update.append('display_name')

        if user_fields_to_update:
            user.save(update_fields=user_fields_to_update)

        entity_account = getattr(user, 'entity_account', None)
        has_avatar_upload = bool(request.FILES.get('avatar'))
        has_cover_upload = bool(request.FILES.get('cover'))
        wants_bio_update = 'bio' in validated

        if entity_account:
            account_fields_to_update = []

            if wants_bio_update:
                entity_account.bio = validated.get('bio', '').strip()
                account_fields_to_update.append('bio')

            if has_avatar_upload:
                entity_account.avatar = request.FILES['avatar']
                account_fields_to_update.append('avatar')

            if has_cover_upload:
                entity_account.cover = request.FILES['cover']
                account_fields_to_update.append('cover')

            if account_fields_to_update:
                entity_account.save(update_fields=account_fields_to_update)
        elif wants_bio_update or has_avatar_upload or has_cover_upload:
            return Response({'detail': 'Kaonty an\'ilay sampana tsy hita.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(self._build_payload(request, user))


class ProvisionEntityAccountView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = ProvisionEntityAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        entity = get_object_or_404(Entity, pk=serializer.validated_data['entity_id'], is_active=True)

        try:
            account, generated_password = provision_entity_account(
                entity=entity,
                email=serializer.validated_data['email'],
                display_name=serializer.validated_data['display_name'],
                created_by=request.user,
            )
        except ValueError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {
                'detail': 'Voaforona tsara ny kaonty.',
                'generatedPassword': generated_password,
                'account': {
                    'userId': account.user_id,
                    'entityId': account.entity_id,
                    'email': account.user.email,
                    'displayName': account.user.get_display_name(),
                    'role': account.user.role,
                },
            },
            status=status.HTTP_201_CREATED,
        )


class AdminEntityAccountListView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        accounts = EntityAccount.objects.select_related('entity', 'user').order_by('entity__name')
        payload = [
            {
                'entityId': account.entity_id,
                'entity': account.entity.name,
                'email': account.user.email,
                'displayName': account.user.get_display_name(),
                'role': account.user.role,
                'isActive': account.user.is_active,
                'createdAt': account.created_at,
            }
            for account in accounts
        ]
        return Response(payload)


class AdminPostModerationListView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = PostSerializer
    queryset = Post.objects.select_related('author', 'author__entity_account__entity').prefetch_related('media')


class AdminPostDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Post.objects.all()


class AdminResetEntityPasswordView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        entity_id = request.data.get('entity_id')
        if not entity_id:
            return Response({'detail': 'Tsy maintsy omena ny entity_id.'}, status=status.HTTP_400_BAD_REQUEST)

        account = get_object_or_404(EntityAccount.objects.select_related('user'), entity_id=entity_id)
        new_password = generate_password()
        account.user.set_password(new_password)
        account.user.save(update_fields=['password'])

        return Response(
            {
                'detail': 'Voaova tsara ny teny miafina.',
                'entityId': account.entity_id,
                'email': account.user.email,
                'generatedPassword': new_password,
            }
        )

