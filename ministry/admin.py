from django.contrib import admin

from .models import ChatMessage, Entity, EntityAccount, FinanceEntry, LeadershipMember, NewsItem, Post, PostMedia


class LeadershipMemberInline(admin.TabularInline):
    model = LeadershipMember
    extra = 1


@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'is_national_office', 'members', 'is_active')
    list_filter = ('is_national_office', 'is_active', 'city')
    search_fields = ('name', 'code', 'city')
    inlines = [LeadershipMemberInline]


@admin.register(EntityAccount)
class EntityAccountAdmin(admin.ModelAdmin):
    list_display = ('entity', 'user', 'created_by', 'created_at')
    search_fields = ('entity__name', 'user__email', 'user__username')


@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at', 'is_published')
    list_filter = ('is_published', 'published_at')
    search_fields = ('title', 'summary')


@admin.register(FinanceEntry)
class FinanceEntryAdmin(admin.ModelAdmin):
    list_display = ('label', 'amount', 'entity', 'recorded_at')
    list_filter = ('recorded_at', 'entity')
    search_fields = ('label',)


class PostMediaInline(admin.TabularInline):
    model = PostMedia
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'created_at', 'likes_count', 'comments_count', 'is_public')
    list_filter = ('is_public', 'created_at')
    search_fields = ('content', 'author__email', 'author__username')
    inlines = [PostMediaInline]


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'author', 'created_at', 'is_public')
    list_filter = ('room', 'is_public', 'created_at')
    search_fields = ('message', 'author__email', 'author__username')

