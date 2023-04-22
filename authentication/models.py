from django.db import models
import uuid


class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, blank=True, null=True, db_index=True)
    uid = models.CharField(max_length=10, unique=True, blank=True, null=True)
    email = models.CharField(max_length=75,  default=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.uid:
            self.uid = str(uuid.uuid4().hex)[:10]
        super(User, self).save(*args, **kwargs)