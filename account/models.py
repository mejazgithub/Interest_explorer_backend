from django.db import models
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,PermissionsMixin)
from .utils import user_permission_choices
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self,email,password=None):
        if email==None:
            raise TypeError("User should have a email")
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,email,password):
        if password is None:
            raise TypeError("User must have a password")
        user = self.create_user(email,password=password)
        user.save()

        user.is_superuser   = True
        user.is_staff       = True
        user.is_verified    = True
        user.is_approved    = True
        user.save()
        return user


class UserPermission(models.Model):
    code=models.CharField(max_length=120)
    name=models.CharField(max_length=120)
    def __str__(self):
        return str(self.name)

    def get_code_name(self):
        try:
            obj,created=Permission.objects.get_or_create(codename = self.code , name=self.name,content_type = ContentType.objects.get_for_model(User))
        except Exception as  e:
            pass
        return self.code


class UserRole(models.Model):
    name            = models.CharField(max_length=120)
    permission      = models.ManyToManyField(UserPermission)
    def __str__(self):
        return str(self.name)

    def save(self,*args,**kwargs):
        super(UserRole,self).save(*args,**kwargs)


class User(AbstractBaseUser,PermissionsMixin):

    first_name          = models.CharField(max_length=100, null=True,blank=True)
    last_name           = models.CharField(max_length=100, null=True,blank=True)
    email               = models.EmailField(max_length=50, unique=True, db_index=True)
    profile_picture     = models.ImageField(upload_to="profile_pictures/", default="profile_pictures/avatar_blank.jpg")
    is_approved         = models.BooleanField(default=False)
    is_verified         = models.BooleanField(default=False)
    is_active           = models.BooleanField(default=True)
    is_owner            = models.BooleanField(default=False)
    is_staff            = models.BooleanField(default=False)
    user_role           = models.ForeignKey(UserRole, on_delete=models.CASCADE, null=True, blank=True)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)


    USERNAME_FIELD  = 'email'
    objects = UserManager()

    
    def __str__(self):
        return "%s"%(self.email)


    def get_role(self):
        try:
            if self.is_owner:
                return 'Owner'
            else:
                return self.user_role.name
        except:
            return ''

    def get_permissions_by_role(self):
        if self.is_owner:
            from account.utils import user_permission_choices
            perms = [x[0] for x in user_permission_choices]
            return perms
        return [j.code for j in self.user_role.permission.all()]

def setup_permissions():
    try:
        for i in user_permission_choices:
            try:
                obj,created = UserPermission.objects.get_or_create(code=i[0],name=i[1])
            except:
                pass
    except Exception as e:
        print("exception in permission creation" , e)