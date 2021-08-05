from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class MyAccountManager(BaseUserManager):
    #Creating Normal user
    def create_user(self,first_name,last_name,username,email,password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email = self.normalize_email(email), #if u enter capital email then it will automatically normalize it to lowercase
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using = self._db)
        return user

    #Creating superuser
    def create_superuser(self,first_name,last_name,username,email,password):
        user = self.create_user(
            email = self.normalize_email(email), #if u enter capital email then it will automatically normalize it to lowercase
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True

        user.save(using = self._db)
        return user




#Creating custom user model (for user)
class Account(AbstractBaseUser):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    username = models.CharField(max_length = 50,unique=True)
    email = models.EmailField(max_length=50,unique=True)
    phone_number = models.CharField(max_length=50)

    #Required field (that will be autogenerated)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD  = 'email'   #Helps you to login with email
    REQUIRED_FIELDS = ['username','first_name','last_name'] #Including email also

    objects = MyAccountManager() #Telling Account that MyAccountManager will take values

    #for Reviews
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email

    def has_perm(self,perm,obj=None):  #It is required in Custom user model
        return self.is_admin

    def has_module_perms(self,add_label):
        return True


    # Notes:-
    # 1. After making changes, delete the existing database and any migrations that have taken place
    # 2. Again create makemigrations and migrate to the new database

    # 3. This will create custom user model for user and superuser and email and password will also be asked in django admin page
    # 4. Superuser can be created with terminal and same field will appear (developer_pulkit@gmail.com,onlinecart)

    # 5. Creating ReadOnly field,list_to_display,clickable_links for password in django admin page (admin.py)
