from django.urls import path, include
from . import views
from django.utils.translation import gettext_lazy as _

app_name = 'users'

urlpatterns = [
    path(_('user/<str:slug>/'), views.UserDetail.as_view(), name='user_detail'),
    path(_('user/update/<str:slug>/'), views.UserUpdateView.as_view(), name='user_update'),
    path(_('follow/<int:user_id>/'), views.FollowUserView.as_view(), name="follow_user"),
    path(_('unfollow/<int:user_id>/'), views.UnfollowUserView.as_view(), name="unfollow_user"),
    path(_('user/<slug:slug>/followers/'), views.FollowersListView.as_view(), name='user_followers'),
    path(_('user/<slug:slug>/following/'), views.FollowingListView.as_view(), name='user_following'),
]
