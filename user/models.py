from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,db_column='created_at')
    created_by = models.ForeignKey('user.User',db_column='created_by_id',on_delete=models.CASCADE,blank=True,null=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    username = models.CharField(db_column='username',max_length=50,unique=True,verbose_name=_("Username"))

    def __str__(self) -> str:
        return self.username
    
    @property
    def get_full_name(self):
        if self.first_name or self.last_name:
            return self.first_name + ' ' if self.first_name else '' + self.last_name
        return self.username


    class Meta:
        ordering = ['-id']
