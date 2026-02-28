from django.urls import path

from .views import (
    AdminEntityAccountListView,
    AdminPostDeleteView,
    AdminPostModerationListView,
    ChatMessageListCreateView,
    EntityDetailView,
    EntityListView,
    FinanceSummaryView,
    MyProfileView,
    NewsListView,
    PostListCreateView,
    ProvisionEntityAccountView,
    AdminResetEntityPasswordView,
)

urlpatterns = [
    path('entities/', EntityListView.as_view(), name='entities'),
    path('entities/<int:pk>/', EntityDetailView.as_view(), name='entity-detail'),
    path('news/', NewsListView.as_view(), name='news'),
    path('finance/summary/', FinanceSummaryView.as_view(), name='finance-summary'),
    path('posts/', PostListCreateView.as_view(), name='posts'),
    path('chat/messages/', ChatMessageListCreateView.as_view(), name='chat-messages'),
    path('profile/me/', MyProfileView.as_view(), name='my-profile'),
    path('admin/provision-account/', ProvisionEntityAccountView.as_view(), name='provision-account'),
    path('admin/entity-accounts/', AdminEntityAccountListView.as_view(), name='admin-entity-accounts'),
    path('admin/posts/', AdminPostModerationListView.as_view(), name='admin-posts'),
    path('admin/posts/<int:pk>/', AdminPostDeleteView.as_view(), name='admin-post-delete'),
    path('admin/reset-entity-password/', AdminResetEntityPasswordView.as_view(), name='admin-reset-entity-password'),
]

