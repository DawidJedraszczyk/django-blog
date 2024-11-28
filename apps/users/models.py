from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.db.models import Q, Count


class BlogUser(AbstractUser):
    bio = models.TextField(blank=True, max_length=100, null=True, verbose_name=_("Bio"))
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True, verbose_name=_("Image"))
    slug = models.SlugField(unique=True, blank=True, db_index=True, max_length=200)

    def __str__(self):
        return self.username

    def generate_unique_slug(self):
        base_slug = slugify(self.username)
        slug = base_slug
        counter = 1
        while BlogUser.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def get_unfollowed_users(self):
        following_ids = self.following.values_list('following_user_id', flat=True)
        return (BlogUser.objects
                .exclude(Q(id__in=following_ids) | Q(id=self.id))
                .annotate(followers_count=Count('followers'))
                .order_by('-followers_count'))

    def is_followed_by(self, user):
        return UserFollowing.objects.filter(user_id=user.id, following_user_id=self.id).exists()


class UserFollowing(models.Model):
    user_id = models.ForeignKey(BlogUser, related_name="following", on_delete=models.CASCADE)
    following_user_id = models.ForeignKey(BlogUser, related_name="followers", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)