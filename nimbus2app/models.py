from django.db import models
import re
# Create your models here.
class UserManager(models.Manager):
    def create_validator(self, reqPOST):
        errors = {}
        email_checker = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(reqPOST['name']) < 2:
            errors['name'] = "Name must be at least 2 characters long"
        if len(reqPOST['username']) < 2:
            errors['username'] = "Username must be at least 2 characters long"
        if not email_checker.match(reqPOST['email']):
            errors['email'] = "Email must be valid"
        if len(reqPOST['password']) < 8:
            errors['password'] = "Password must be at least 8 chcaracters"
        if reqPOST['password'] != reqPOST['confpassword']:
            errors['password'] = "Passwords do not match!"
        return errors

class User(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Image(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title