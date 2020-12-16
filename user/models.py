from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager


class ProfileManager(UserManager):
	def create(self, *args, **kwargs):
		user = UserProfile(*args, **kwargs)
		user.password = make_password(user.password)
		user.save()
		return user


class UserProfile(AbstractUser):
    """Extension to the default User model.
    
    The only additional field is photo Image field
    """
    
    email = models.EmailField(
    	unique=True, blank=False, max_length=254, verbose_name='email address'
    )
    photo = models.ImageField(upload_to='uploads/', blank=True)
    objects = ProfileManager()
