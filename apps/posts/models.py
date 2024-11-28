from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('title'))
    content = models.TextField(verbose_name=_('content'))
    image = models.ImageField(upload_to='post_images/', blank=True, null=True, verbose_name=_("Image"))
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('users.BlogUser', on_delete=models.CASCADE, related_name="posts")
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True, db_index=True, max_length=200)

    def __str__(self):
        return self.title

    def generate_unique_slug(self):
        base_slug = slugify(self.title)
        slug = base_slug
        counter = 1
        while Post.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)