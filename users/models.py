from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_client = models.BooleanField(default=False)
    is_lawyer = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'CustomUser'
    
    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username



class Client(CustomUser):

    class Meta:
        verbose_name = 'ClientUser'

    def save(self, *args, **kwargs):
        self.is_client = True
        self.is_lawyer = False
        super().save(*args, **kwargs)

    def __str__(self):
        return super().username



class Lawyer(CustomUser):
    rate = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = "LawyerUser"

    def save(self, *args, **kwargs):
        self.is_client = False
        self.is_lawyer = True
        super().save(*args, **kwargs)

    def __str__(self):
        return super().username

    def clean(self):
        if self.rate < 0 or self.rate > 5:
            raise ValidationError("Rate must be between 0:5")
        return super().clean()

class LawyerProfile(models.Model):
    lawyer = models.OneToOneField(Lawyer, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profiles/', blank=True, null=True, default='profiles/default-user.jpg')
    experience = models.TextField(blank=True, null=True)
    experience_years = models.IntegerField(null=True, blank=True)
    bio = models.TextField(blank=True, null=True)

class VerifyToken(models.Model):
    token = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.token[0:60]} ..."


@receiver(post_save, sender=Lawyer)
def create_layer_profile(sender, instance, created, **kwagrs):
    if created:
        LawyerProfile.objects.create(lawyer=instance)