from django.db import models
from users import models as users_models
from organizations import models as org_models

class Category(models.Model):
    name = models.CharField(max_length=255)

class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class New(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(users_models.Lawyer, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subject = models.TextField(blank=False, null=False)
    image = models.ImageField(upload_to='news/images/', null=True, blank=True)

class SolvedCase(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(users_models.Lawyer, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subject = models.TextField(blank=False, null=False)

class Comment(models.Model):
    user = models.ForeignKey(users_models.CustomUser, on_delete=models.CASCADE)
    new = models.ForeignKey(New, on_delete=models.CASCADE)
    comment = models.TextField(blank=False, null=False)

class Like(models.Model):
    user = models.ForeignKey(users_models.CustomUser, on_delete=models.CASCADE)
    new = models.ForeignKey(New, on_delete=models.CASCADE)

class Case(models.Model):
    CASE_STATUS_CHOICES = [('pending', 'قيد الانتظار'), ('reserved', 'محجوز')]
    user = models.ForeignKey(users_models.CustomUser, on_delete=models.CASCADE)
    description = models.TextField()
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    case_status = models.CharField(max_length=20, choices=CASE_STATUS_CHOICES, default='pending')

class CaseInvetation(models.Model):
    INVETATION_STATUS_CHOICES = [('pending', 'قيد الانتظار'), ('accepted', 'مقبول'), ('rejected','مرفوض')]
    organization = models.ForeignKey(org_models.Organization, on_delete=models.CASCADE)
    user_approvment = models.BooleanField(null=True, blank=True)
    org_approvment = models.BooleanField(null=True, blank=True)
    invetation_status = models.CharField(max_length=15, choices=INVETATION_STATUS_CHOICES, default='pending')
    the_case = models.OneToOneField(Case, on_delete=models.CASCADE)