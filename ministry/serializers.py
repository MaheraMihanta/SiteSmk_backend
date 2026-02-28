from decimal import Decimal

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import ChatMessage, Entity, FinanceEntry, LeadershipMember, NewsItem, Post, PostMedia

User = get_user_model()


class LeadershipMemberSerializer(serializers.ModelSerializer):
    roleLabel = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = LeadershipMember
        fields = ['role', 'roleLabel', 'member_name']


class EntitySerializer(serializers.ModelSerializer):
    isNationalOffice = serializers.BooleanField(source='is_national_office')

    class Meta:
        model = Entity
        fields = ['id', 'code', 'name', 'city', 'contact', 'members', 'leader', 'description', 'isNationalOffice']


class EntityDetailSerializer(EntitySerializer):
    leadership = LeadershipMemberSerializer(source='leadership_members', many=True, read_only=True)

    class Meta(EntitySerializer.Meta):
        fields = EntitySerializer.Meta.fields + ['leadership']


class NewsItemSerializer(serializers.ModelSerializer):
    date = serializers.DateField(source='published_at')
    image = serializers.SerializerMethodField()

    class Meta:
        model = NewsItem
        fields = ['id', 'title', 'summary', 'content', 'date', 'image']

    def get_image(self, obj):
        if not obj.image:
            return ''
        request = self.context.get('request')
        url = obj.image.url
        return request.build_absolute_uri(url) if request else url


class FinanceTransactionSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = FinanceEntry
        fields = ['label', 'amount', 'type']

    def get_type(self, obj):
        return 'income' if obj.amount >= 0 else 'expense'


class PostMediaSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    type = serializers.CharField(source='media_type')

    class Meta:
        model = PostMedia
        fields = ['id', 'type', 'name', 'url']

    def get_url(self, obj):
        request = self.context.get('request')
        url = obj.file.url
        return request.build_absolute_uri(url) if request else url


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    likes = serializers.IntegerField(source='likes_count')
    comments = serializers.IntegerField(source='comments_count')
    createdAt = serializers.DateTimeField(source='created_at')
    media = PostMediaSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'likes', 'comments', 'createdAt', 'media']

    def get_author(self, obj):
        user = obj.author
        account = getattr(user, 'entity_account', None)
        avatar_url = ''
        entity_name = 'Foibe nasionaly'
        if account:
            entity_name = account.entity.name
            if account.avatar:
                request = self.context.get('request')
                avatar_url = request.build_absolute_uri(account.avatar.url) if request else account.avatar.url

        return {
            'name': user.get_display_name(),
            'avatar': avatar_url,
            'entity': entity_name,
        }


class PostCreateSerializer(serializers.ModelSerializer):
    content = serializers.CharField(required=False, allow_blank=True, default='')

    class Meta:
        model = Post
        fields = ['content']

    def validate(self, attrs):
        request = self.context.get('request')
        content = (attrs.get('content') or '').strip()
        has_media = bool(request and request.FILES.getlist('media'))

        if not content and not has_media:
            raise serializers.ValidationError('Ampidiro lahatsoratra na media farafahakeliny.')

        attrs['content'] = content
        return attrs


class ChatMessageSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()
    createdAt = serializers.DateTimeField(source='created_at')

    class Meta:
        model = ChatMessage
        fields = ['id', 'author', 'message', 'time', 'createdAt']

    def get_author(self, obj):
        return obj.author.get_display_name()

    def get_time(self, obj):
        return obj.created_at.strftime('%H:%M')


class ChatMessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['message']


class ProfileSerializer(serializers.Serializer):
    name = serializers.CharField()
    bio = serializers.CharField()
    entity = serializers.CharField(allow_blank=True)
    city = serializers.CharField(allow_blank=True)
    joinedDate = serializers.CharField()
    postsCount = serializers.IntegerField()
    friends = serializers.IntegerField()
    email = serializers.EmailField()
    role = serializers.CharField()
    avatar = serializers.CharField(allow_blank=True)
    cover = serializers.CharField(allow_blank=True)


class ProfileUpdateSerializer(serializers.Serializer):
    display_name = serializers.CharField(max_length=120, required=False)
    bio = serializers.CharField(required=False, allow_blank=True)


class ProvisionEntityAccountSerializer(serializers.Serializer):
    entity_id = serializers.IntegerField()
    email = serializers.EmailField()
    display_name = serializers.CharField(max_length=120)

    def validate_entity_id(self, value):
        if not Entity.objects.filter(id=value, is_active=True).exists():
            raise serializers.ValidationError('Tsy hita na tsy miasa ilay sampana.')
        return value

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('Efa ampiasaina io email io.')
        return value.lower()


class FinanceSummarySerializer(serializers.Serializer):
    totalCollected = serializers.DecimalField(max_digits=12, decimal_places=2)
    totalSpent = serializers.DecimalField(max_digits=12, decimal_places=2)
    balance = serializers.DecimalField(max_digits=12, decimal_places=2)
    currency = serializers.CharField()
    recentTransactions = FinanceTransactionSerializer(many=True)

    @staticmethod
    def from_entries(entries):
        total_collected = Decimal('0.00')
        total_spent = Decimal('0.00')
        for entry in entries:
            if entry.amount >= 0:
                total_collected += entry.amount
            else:
                total_spent += abs(entry.amount)

        return {
            'totalCollected': total_collected,
            'totalSpent': total_spent,
            'balance': total_collected - total_spent,
            'currency': 'Ar',
            'recentTransactions': entries[:8],
        }

