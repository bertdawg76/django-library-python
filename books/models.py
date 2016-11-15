from __future__ import unicode_literals
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User, AbstractBaseUser, PermissionsMixin, UserManager, BaseUserManager


# Create your models here.

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    isLibrarian = models.BooleanField(default=False)
    username = models.CharField(
        max_length=255,
        unique=True,
        default=''
    )
    email = models.EmailField(
        max_length=255,
        unique=True,
        default=''
    )
    # date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_active = models.BooleanField(default=True)
    # is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    # def __str__(self):
    #     return self.user
    objects = UserManager()


    def get_short_name(self):

        return self.username


def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = UserProfile(user=user)
        user_profile.save()
post_save.connect(create_profile, sender=User)

class Book(models.Model):

    book_name = models.CharField(max_length=100)
    book_author = models.CharField(max_length=100)
    book_image = models.ImageField('Uploaded image', default='')
    book_isbn = models.CharField(max_length=100)
    book_genre = models.CharField(max_length=100)
    book_shelf = models.ForeignKey('Shelf', on_delete=models.CASCADE, default=2)
    is_available = models.BooleanField(default=True)

    @property
    def book_due_date(self):
        d = Checkout.objects.filter(book_id=self.id).order_by('-due_date').first()
        print(d)
        if d:
            return d.due_date

        return 'nothing to see'

    def __str__(self):
        return self.book_name

    # @property
    # def book_due_date(self):
    #     d = self.Checkout
    #     return d.due_date


class Checkout(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, default=1)
    issue_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return '{} - {}'.format(self.book.book_name, self.user.username)


class Branch(models.Model):
    location = models.CharField(max_length=100)
    branch_name = models.CharField(max_length=100)

    def __str__(self):
        return self.branch_name

class Shelf(models.Model):

    genre = models.CharField(max_length=100)
    shelf_number = models.IntegerField(default=1)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.genre, self.branch)

class Return(models.Model):

    checkouts = models.ForeignKey(Checkout, max_length=100, default='')
    book = models.ForeignKey(Book, max_length=100, default='')
    return_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    location = models.ForeignKey(Branch, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.checkouts.book.book_name