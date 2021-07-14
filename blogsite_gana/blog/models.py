from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

# Create your models here.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,
                    self).get_queryset()\
                        .filter(status='published')

# Database model for the Posts created
class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250) # Title field for the post title
    slug = models.SlugField(max_length=250, unique_for_date='publish') # field intended to be used for URLs
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts') # Author of the blog
    body = models.TextField() # Body of the post
    publish = models.DateTimeField(default=timezone.now) # Time when the post is published
    created = models.DateTimeField(auto_now_add=True) # Time when the post is first created
    updated = models.DateTimeField(auto_now=True) # Last time when the post is updated
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft') # Shows whether the post is a draft or published
    tags = TaggableManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
        args=[self.publish.year,
        self.publish.month,
        self.publish.day,
        self.slug])

    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ('created',)
    def __str__(self):
        return f'Commen by {self.name} on {self.post}'