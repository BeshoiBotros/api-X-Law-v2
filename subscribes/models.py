from django.db import models
from django.core.validators import MinValueValidator
from datetime import date
from users.models import Lawyer
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

def get_current_date():
    return date.today()

class Limit(models.Model):
    
    number_of_object = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete = models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        desc = ''
        if len(self.description) < 20:
            return f"{self.title}: {self.description}"
        return f"{self.title}: {self.description}...."
 
class Subscribe(models.Model):

    currency_choices = (('USD', 'United States dollar'), ('EUR', 'the Euro'), ('EGP', 'Egyptian pound'))
    name = models.CharField(max_length=255)
    limits = models.ManyToManyField(Limit, null=True, blank=True)
    start_deuration = models.DateField(default=get_current_date)
    end_deuration = models.DateField(null = False, blank = False)
    is_free = models.BooleanField(default=False)
    price = models.FloatField()
    currency = models.CharField(choices=currency_choices, max_length=3)
    is_active = models.BooleanField(default=False)
    description = models.TextField(blank=False, null=True)
    subscribe_Type = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.name}'

class SubscribeOrder(models.Model):

    requestStatusChoices = (('underProcess', 'تحت الاجراء'), ('accepted', 'مقبول'), ('rejected', 'مرفوض'), ('canceled', 'ملغي'), ('other', 'اخرى'))
    subscribe = models.ForeignKey(Subscribe, on_delete=models.CASCADE)
    companyuser = models.OneToOneField(Lawyer, on_delete=models.CASCADE,null=True, blank=True)
    companyName = models.CharField(max_length=255)
    companyAddres = models.TextField(null=False, blank=False)
    companyNo = models.CharField(max_length=200, blank=True,default='')
    companyID = models.FileField(upload_to='companyID/')
    companyURL = models.URLField(null=True, blank=True)
    companyEmail = models.EmailField(null=True, blank=True)
    responsibleName = models.CharField(max_length=255)
    responsiblePhone = models.CharField(max_length=15)
    responsibleEmail = models.EmailField(null=True, blank=True)
    requestStatus = models.CharField(choices=requestStatusChoices, max_length=30, default='underProcess')
    statusDiscription = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.companyuser.username} Order, company: {self.companyName}'

class SubscribeContract(models.Model):

    subscribe_order = models.OneToOneField(SubscribeOrder, models.CASCADE)
    subscribeContractStatusChoices = (('underProcess', 'جاري التعاقد'), ('paied', 'مدفوع'), ('unpaied', 'غير مدفوع'), ('canceled', 'ملغي'), ('rejected', 'مرفوض'), ('other', 'اخرى'))
    status_discription = models.TextField(null=True, blank=True)
    subscribe_contract_status = models.CharField(choices=subscribeContractStatusChoices, max_length=30, default='underProcess')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    nums_of_users = models.IntegerField(null=True, blank=True)
    reciept_file = models.FileField(upload_to='recipet_files/', blank=True, null=True)
    paied_amount = models.FloatField(null=True, blank=True)
    contract_file = models.FileField(upload_to='contractDiscription/', null=True, blank=True)
    contract_discription = models.TextField(null=True, blank=True)
    contract_aproval = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.subscribe_order.companyuser.username} Contract, Company: {self.subscribe_order.companyName}'

