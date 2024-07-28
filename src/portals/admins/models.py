from django.db import models
from django.utils.text import slugify
from django_resized import ResizedImageField
from src.accounts.models import User


class BlogTag(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Blog Tag"
        verbose_name_plural = "Blog Tags"

    def __str__(self):
        return self.name


class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"

    def __str__(self):
        return self.name


class Blog(models.Model):
    thumbnail = ResizedImageField(
        upload_to='admins/blog/images/articles/thumbnail/', null=True, blank=True, quality=100,
        crop=['middle', 'center'],
        size=[350, 300],
        help_text='Take your time and create thumbnail image for your blog '
                  'size must be 400*400 and available format are JPG, JPEG and PNG only.'
    )
    banner_image = ResizedImageField(
        upload_to='admins/blog/images/articles/banner/', null=True, blank=True, quality=75,
        size=[872, 303],
        help_text='Banner image will be visible at the top of your article, '
                  'size must be 872w*303h and available format are JPG, JPEG and PNG only.'
    )
    title = models.CharField(
        max_length=255, null=False, blank=False, unique=True,
    )
    description = models.TextField(
        null=False, blank=False, default="Description is not provided yet, Please add short introductory paragraph",
    )
    detailed_description = models.TextField(null=False, blank=False)
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    blog_category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(BlogTag)

    slug = models.SlugField(unique=True, null=False, blank=True)
    read_time = models.PositiveIntegerField(null=False, blank=False, default=1, help_text="Add read time in minutes")
    likes = models.PositiveIntegerField(null=False, blank=False, default=0)
    views = models.PositiveIntegerField(null=False, blank=False, default=0)

    is_active = models.BooleanField(default=True, blank=False, null=False)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Blog Article'
        verbose_name_plural = 'Blog Articles'

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.thumbnail.delete(save=True)
        self.banner_image.delete(save=True)
        super(Blog, self).delete(*args, **kwargs)


""" MANAGE FILING """


class Company(models.Model):
    name = models.CharField(max_length=1000, unique=True)
    description = models.TextField(default="Description not provided yet.")
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name


class Filing(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    stripe_payment_intent = models.CharField(max_length=20000, null=True, blank=True)

    amount = models.FloatField(default=0.0)
    is_paid = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']
        verbose_name = "Company Filing"
        verbose_name_plural = "Companies Filings"

    def __str__(self):
        return self.full_name


class CallRequest(models.Model):
    CALL_STATUS_CHOICES = (
        (1, 'Completed'),
        (2, 'Pending'),
        (3, 'Failed'),
        (4, 'No Response'),
    )
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    call_status = models.CharField(max_length=1, choices=CALL_STATUS_CHOICES)
    is_active = models.BooleanField(default=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-call_status', '-id']
        verbose_name = "Call Request"
        verbose_name_plural = "Calls Requests"

    def __str__(self):
        return self.full_name


class Subscriber(models.Model):
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
        verbose_name = "Subscriber"
        verbose_name_plural = "Subscribers"

    def __str__(self):
        return self.email
