import random
import os
from faker import Faker
from django.core.management.base import BaseCommand
from apps.users.models import BlogUser, UserFollowing
from apps.posts.models import Post
from django.core.files import File
from django.utils.text import slugify


class Command(BaseCommand):
    help = "Populate the database with example users, follow relationships, and posts"

    def handle(self, *args, **kwargs):
        faker = Faker()
        num_users = 100
        num_posts_per_user = random.randint(1, 5)
        profile_images_dir = "examples/profile_images/"  # Path to your example images
        profile_images = [os.path.join(profile_images_dir, f) for f in os.listdir(profile_images_dir)]

        # Step 1: Create Users
        self.stdout.write("Creating users...")
        users = []
        for _ in range(num_users):
            username = faker.unique.user_name()
            email = faker.unique.email()
            bio = faker.sentence(nb_words=10)
            image_path = random.choice(profile_images) if profile_images else None

            user = BlogUser(
                username=username,
                email=email,
                bio=bio,
                slug=slugify(username),
            )
            user.set_password("password123")  # Default password for all users
            if image_path:
                with open(image_path, "rb") as img_file:
                    user.image.save(os.path.basename(image_path), File(img_file), save=False)
            users.append(user)

        BlogUser.objects.bulk_create(users)
        users = list(BlogUser.objects.all())  # Refresh to get actual IDs
        self.stdout.write(f"Created {len(users)} users.")

        # Step 2: Create Random Following Relationships
        self.stdout.write("Creating follow relationships...")
        followings = []
        for user in users:
            num_followings = random.randint(5, 20)  # Each user follows 5-20 other users
            following_users = random.sample(users, num_followings)
            for following_user in following_users:
                if user != following_user and not UserFollowing.objects.filter(
                    user_id=user, following_user_id=following_user
                ).exists():
                    followings.append(UserFollowing(user_id=user, following_user_id=following_user))

        UserFollowing.objects.bulk_create(followings)
        self.stdout.write(f"Created {len(followings)} follow relationships.")

        # Step 3: Create Posts
        self.stdout.write("Creating posts...")
        posts = []
        for user in users:
            num_posts = random.randint(1, num_posts_per_user)  # 1-5 posts per user
            for _ in range(num_posts):
                title = faker.sentence(nb_words=6)
                content = faker.paragraph(nb_sentences=10)
                slug = slugify(title)
                post = Post(
                    title=title,
                    content=content,
                    slug=slug,
                    created_by=user,
                )
                posts.append(post)

        Post.objects.bulk_create(posts)
        self.stdout.write(f"Created {len(posts)} posts.")

        self.stdout.write(self.style.SUCCESS("Database populated successfully!"))
