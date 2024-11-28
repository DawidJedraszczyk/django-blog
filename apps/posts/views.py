from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from .models import Post
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from apps.users.models import BlogUser

class PostsMixin(LoginRequiredMixin):
    login_url = reverse_lazy('account_login')


class PostMainView(PostsMixin, View):
    template_name = 'posts/post_main.html'

    def get_posts(self):
        return Post.objects.all().order_by('-created_at')

    def get(self, request, *args, **kwargs):
        posts = self.get_posts()
        post_form = PostForm()
        users = self.request.user.get_unfollowed_users()
        return render(request, self.template_name, {'posts': posts, 'post_form': post_form, 'users': users})

    def post(self, request, *args, **kwargs):
        if request.POST.get('form_type') == 'post_form':
            post_form = PostForm(request.POST)
            if post_form.is_valid():
                post = post_form.save(commit=False)
                post.created_by = request.user
                post.save()
                return redirect('post_main')
        else:
            post_form = PostForm()

        posts = self.get_posts()
        users = self.request.user.get_unfollowed_users()
        return render(request, self.template_name, {'posts': posts, 'post_form': post_form, 'users': users})


class PostDetailView(PostsMixin, DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

class PostCreateView(PostsMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'
    success_url = reverse_lazy('post_main')

class PostUpdateView(PostsMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'
    success_url = reverse_lazy('post_main')

class PostDeleteView(PostsMixin, DeleteView):
    model = Post
    template_name = 'posts/post_delete.html'
    success_url = reverse_lazy('post_main')