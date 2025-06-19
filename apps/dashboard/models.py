from django.db import models

# Create your models here.

from django.db import models
import uuid
# Create your models here.

class BaseClass(models.Model):
    cid = models.UUIDField(primary_key=True, null=False, blank=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class user(BaseClass):
    email = models.EmailField(max_length=255, blank=False, null=False)
    mobile = models.CharField(max_length=255, null=False, blank=False)
    password = models.CharField(max_length=255, blank=False, null=False)
    otp = models.CharField(max_length=20, default="112233")
    is_active = models.BooleanField(default=False)
