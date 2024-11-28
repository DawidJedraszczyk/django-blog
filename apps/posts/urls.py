from django.urls import path
from . import views
from django.utils.translation import gettext_lazy as _


urlpatterns = [
    path('', views.PostMainView.as_view(), name='post_main'),
    path(_('post/<str:slug>/'), views.PostDetailView.as_view(), name='post_detail'),
    path(_('post/create/'), views.PostCreateView.as_view(), name='post_create'),
    path(_('post/update/<str:slug>/'), views.PostUpdateView.as_view(), name='post_update'),
    path(_('post/delete/<str:slug>/'), views.PostDeleteView.as_view(), name='post_delete'),
]