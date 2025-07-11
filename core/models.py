from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    title = models.CharField(
        max_length=255,
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    content = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )
    featurette = models.ImageField(
        upload_to='blog/images/',
        blank=True,
        null=True,
    )
    tags = models.ManyToManyField(
        'Tag',
        blank=True,
        related_name='posts',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    published_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    view_count = models.PositiveIntegerField(
        default=0,
    )
    is_featured = models.BooleanField(
        default=False,
    )
    meta_description = models.CharField(
        max_length=160,
        blank=True,
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['author', '-created_at']),
            models.Index(fields=['slug']),
        ]
    
    def __str__(self):
        return self.title
  
    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})
    
    @property
    def is_published(self):
        return self.status == 'published'
      
class Tag(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )
    description = models.TextField(
        blank=True,
    )
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('blog:tag_detail', kwargs={'slug': self.slug})


class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    reviewer_name = models.CharField(
        max_length=100,
        blank=True,
        default='Anonymous',
    )
    email = models.EmailField(
        blank=True,
    )
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
    )
    comment = models.TextField(
        max_length=1000,
        blank=True,
   )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        indexes = [
            models.Index(fields=['post', '-created_at']),
            models.Index(fields=['is_approved', '-created_at']),
            models.Index(fields=['rating']),
        ]
    
    def __str__(self):
        return f"{self.reviewer_name or 'Anonymous'} - {self.rating} stars for '{self.post.title}'"
    
    @property
    def display_name(self):
        return self.reviewer_name or 'Anonymous'