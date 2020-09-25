from django.db import models
import uuid
from django.utils.text import slugify
from django.conf import settings
from .validators import validate_phone_number
from django.urls import reverse
from django.db.models.signals import post_save
from taggit.managers import TaggableManager
from django.utils.timezone import localdate
from django.utils import timezone
from datetime import datetime


def image_path(obj, filename):
    extension = filename.split('.')[-1]
    unique_id = uuid.uuid4().hex
    new_file_name = unique_id+'.'+extension
    new_file_name = f"{str(obj.name)}/{new_file_name}"
    return f"contact/{datetime.now().date()}/"+new_file_name


class ContactManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='share')


class Contact(models.Model):
    STATUS_CHOICES = (
        ('unshare', 'Unshare'),
        ('share', 'Share'),
    )
    name = models.CharField(max_length=150)
    slug = models.SlugField(
        max_length=200, editable=True, null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='blog_posts', default=1)
    mobile = models.CharField(max_length=20,
                              validators=[validate_phone_number, ], blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    address = models.CharField(
        max_length=100, blank=True, null=True, help_text="Enter Complete Address")
    image = models.ImageField(upload_to=image_path)
    profession = models.CharField(max_length=100)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='share')

    linkedin_url = models.CharField(max_length=200, blank=True, null=True)
    facebook_url = models.CharField(max_length=200, blank=True, null=True)
    github_url = models.CharField(max_length=200, blank=True, null=True)
    bio_url = models.CharField(max_length=200, blank=True, null=True)
    views = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    search_tags = TaggableManager()

    class Meta:
        ordering = ('-created',)
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('contacts:user_post_list', kwargs={
            'author': self.author.username, 'author_id': self.author.id})


def post_save_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            instance.slug = slugify(instance.name)+f"-{instance.id}"
            instance.save()
        except:
            pass


post_save.connect(post_save_model_receiver,
                  sender=Contact)
