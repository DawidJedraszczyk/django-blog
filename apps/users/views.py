from django.views.generic import DetailView, UpdateView, ListView
from django.views import View
from .models import BlogUser, UserFollowing
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import UserForm
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _


class UsersMixin(LoginRequiredMixin):
    login_url = reverse_lazy('account_login')

class UserDetail(UsersMixin, DetailView):
    model = BlogUser
    template_name = 'users/user_detail.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = self.get_object().posts.all()

        paginator = Paginator(posts, 5)
        page_number = self.request.GET.get('page')
        context['page_obj'] = paginator.get_page(page_number)

        followed = self.get_object().is_followed_by(self.request.user)
        context['followed'] = followed

        return context

class UserUpdateView(UsersMixin, UpdateView):
    model = BlogUser
    form_class = UserForm
    template_name = 'users/user_form.html'

    def get_success_url(self):
        return reverse_lazy('users:user_detail', kwargs={'slug': self.get_object().slug})


class FollowUserView(LoginRequiredMixin, View):
    def post(self, request, user_id):
        following_user = get_object_or_404(BlogUser, id=user_id)
        current_user = request.user

        if not UserFollowing.objects.filter(user_id=current_user, following_user_id=following_user).exists():
            UserFollowing.objects.create(
                user_id=current_user,
                following_user_id=following_user
            )
            return JsonResponse({
                "status": "success",
                "operation_type": "followed",
                "message": _("Now following"),
                "unfollow_url": reverse_lazy('users:unfollow_user', kwargs={'user_id': following_user.id})
            }, status=201)
        else:
            return JsonResponse({"status": "error", "message": _("Already following")}, status=400)


class UnfollowUserView(LoginRequiredMixin, View):
    def post(self, request, user_id):
        target_user = get_object_or_404(BlogUser, id=user_id)
        follow_relationship = UserFollowing.objects.filter(user_id=request.user, following_user_id=target_user)

        if follow_relationship.exists():
            follow_relationship.delete()
            return JsonResponse({
                "status": "success",
                "operation_type": "unfollowed",
                "message": _("Unfollowed successfully"),
                "follow_url": reverse_lazy('users:follow_user', kwargs={'user_id': target_user.id})
            }, status=201)
        else:
            return JsonResponse({"status": "error", "message": _("You are not following this user")}, status=400)

class FollowersListView(ListView):
    model = BlogUser
    template_name = 'users/followers_list.html'
    context_object_name = 'followers'

    def get_queryset(self):
        user = get_object_or_404(BlogUser, slug=self.kwargs['slug'])
        return BlogUser.objects.filter(following__following_user_id=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = get_object_or_404(BlogUser, slug=self.kwargs['slug'])
        return context

class FollowingListView(ListView):
    model = BlogUser
    template_name = 'users/following_list.html'
    context_object_name = 'following'

    def get_queryset(self):
        user = get_object_or_404(BlogUser, slug=self.kwargs['slug'])
        return BlogUser.objects.filter(followers__user_id=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = get_object_or_404(BlogUser, slug=self.kwargs['slug'])
        return context
