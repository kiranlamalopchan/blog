from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db.models import Count
from tinymce import HTMLField

User = get_user_model()


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to='uploads/img/authors', null=True, blank=True)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title

    @staticmethod
    def get_all_categories():
        return Category.objects.all()


class Post(models.Model):
    title = models.CharField(max_length=250)
    overview = HTMLField(default="Overview")
    timestamp = models.DateTimeField(auto_now_add=True)
    content = HTMLField()
    comment_count = models.IntegerField(default=0, null=True, blank=True)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, null=True, blank=True)
    thumbnail = models.ImageField(upload_to='uploads/img/thumnails/')
    featured = models.BooleanField(default=False)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.title

    @staticmethod
    def get_featured_post():
        return Post.objects.filter(featured=True)

    @staticmethod
    def get_latest_post():
        return Post.objects.order_by('-timestamp')

    @staticmethod
    def get_all_post():
        return Post.objects.all()

    def get_category_count():
        query_set = Post.objects.values(
            'categories__title').annotate(Count('categories__title'))
        return query_set

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"id": self.id})

    @staticmethod
    def get_specific_post(id):
        return Post.objects.filter(id=id)

    @staticmethod
    def get_authors_post(author):
        return Post.objects.filter(author=author)

    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')

    @property
    def comment_count(self):
        return Comment.objects.filter(post=self).count()


class ContactInfo(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_no = models.IntegerField(null=True, blank=True)
    company = models.CharField(max_length=100, null=True, blank=True)
    messages = models.TextField(max_length=500, null=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey(
        'Post', related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class MobilePrice(models.Model):
    content = HTMLField()

    @staticmethod
    def get_mobileprice():
        return MobilePrice.objects.all()
