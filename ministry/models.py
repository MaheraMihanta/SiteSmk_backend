from django.conf import settings
from django.db import models
from django.utils import timezone


class LeadershipRole(models.TextChoices):
    PRESIDENT = 'PRESIDENT', 'President'
    VICE_PRESIDENT_1 = 'VICE_PRESIDENT_1', 'Vice-president 1'
    VICE_PRESIDENT_2 = 'VICE_PRESIDENT_2', 'Vice-president 2'
    TREASURER = 'TREASURER', 'Tresorier'
    FINANCIAL_SECRETARY = 'FINANCIAL_SECRETARY', 'Secretaire financier'
    SECRETARY_GENERAL_1 = 'SECRETARY_GENERAL_1', 'Secretaire general 1'
    SECRETARY_GENERAL_2 = 'SECRETARY_GENERAL_2', 'Secretaire general 2'
    COUNSELOR_1 = 'COUNSELOR_1', 'Conseiller 1'
    COUNSELOR_2 = 'COUNSELOR_2', 'Conseiller 2'
    COUNSELOR_3 = 'COUNSELOR_3', 'Conseiller 3'
    COUNSELOR_4 = 'COUNSELOR_4', 'Conseiller 4'


class Entity(models.Model):
    code = models.SlugField(max_length=50, unique=True)
    name = models.CharField(max_length=160, unique=True)
    city = models.CharField(max_length=80)
    contact = models.CharField(max_length=60, blank=True)
    leader = models.CharField(max_length=120, blank=True)
    members = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    is_national_office = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class LeadershipMember(models.Model):
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='leadership_members')
    role = models.CharField(max_length=40, choices=LeadershipRole.choices)
    member_name = models.CharField(max_length=120)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['entity', 'role'], name='unique_role_per_entity')]
        ordering = ['entity__name', 'role']

    def __str__(self):
        return f"{self.entity.name} - {self.get_role_display()}"


class EntityAccount(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='entity_account')
    entity = models.OneToOneField(Entity, on_delete=models.CASCADE, related_name='account')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='provisioned_entity_accounts',
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['entity__name']

    def __str__(self):
        return f"{self.entity.name} ({self.user.email})"


class NewsItem(models.Model):
    title = models.CharField(max_length=180)
    summary = models.TextField()
    content = models.TextField(blank=True)
    published_at = models.DateField(default=timezone.localdate)
    image = models.FileField(upload_to='news/', blank=True, null=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-published_at', '-id']

    def __str__(self):
        return self.title


class FinanceEntry(models.Model):
    entity = models.ForeignKey(
        Entity,
        on_delete=models.SET_NULL,
        related_name='finance_entries',
        null=True,
        blank=True,
    )
    label = models.CharField(max_length=180)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    recorded_at = models.DateField(default=timezone.localdate)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-recorded_at', '-created_at']

    def __str__(self):
        return f"{self.label} ({self.amount})"


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Post #{self.id} by {self.author_id}"


class MediaType(models.TextChoices):
    PHOTO = 'photo', 'Photo'
    VIDEO = 'video', 'Video'
    DOCUMENT = 'document', 'Document'


class PostMedia(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='media')
    file = models.FileField(upload_to='posts/')
    media_type = models.CharField(max_length=20, choices=MediaType.choices, default=MediaType.PHOTO)
    name = models.CharField(max_length=160, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"Media #{self.id} ({self.media_type})"


class ChatMessage(models.Model):
    room = models.CharField(max_length=50, default='general')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_messages')
    message = models.TextField(max_length=1500)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.room}] {self.author_id}"

