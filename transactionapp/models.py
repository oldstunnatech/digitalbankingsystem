from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

# Create your models here.

class Account_table(models.Model):
    acc_type = [
        ("Savings", "Savings"),
        ("Current", "Current"),
        ("Fixed Deposit", "Fixed Deposit"),
        
    ]

    status = [
        ("Active", "Active"),
        ("Retired", "Retired"),
        ("Suspended", "Suspended"),
        ("Freeze", "Freeze"),
        ("On Leave", "On Leave"),
        ("Dormant", "Dormant"),
    ]

    account_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_balance = models.BigIntegerField(unique=False, default=0)
    account_type = models.CharField(choices=acc_type, unique=False, max_length=20)
    account_number = models.CharField(unique=True, max_length=10, default="0000000000")
    account_pin = models.CharField(default="0000", unique=False, max_length=128)

    account_status = models.CharField(choices=status, default="Active", unique=False, max_length=10)

    # ddef save(self, *args, **kwargs):
    #     if self.account_pin and not self.account_pin.startswith('pbkdf2_'):
    #         self.account_pin = make_password(self.account_pin)
    #     super().save(*args, **kwargs)
    

    def save(self, *args, **kwargs):
        if self.pk:
            # Existing account: check if PIN changed
            old_pin = Account_table.objects.get(pk=self.pk).account_pin
            if self.account_pin != old_pin and not self.account_pin.startswith('pbkdf2_'):
                self.account_pin = make_password(self.account_pin)
        else:
            # New account
            if self.account_pin and not self.account_pin.startswith('pbkdf2_'):
                self.account_pin = make_password(self.account_pin)
        
        super().save(*args, **kwargs)

        
    def __str__(self):
        return f"{self.account_number}"
        return f"{self.account_type}"
        return f"₦{self.account_balance}"



    
class Bill_payment(models.Model):
    
    BILL_TYPE_CHOICES = [
        ("Electricity", "Electricity"),
        ("Cable", "Cable"),
        ("Water", "Water"),
    ]
    REQUEST_TYPE_CHOICES = [
        ("New Request", "New Request"),
        ("Renewal", "Renewal"),
    ]

    MONTHS_OF_SUB_CHOICES = [
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
        ("6", "6"),
        ("7", "7"),
        ("8", "8"),
        ("9", "9"),
        ("10", "10"),
        ("11", "11"),
        ("12", "12"),
    ]

    ELECT_CHOICES =[
        ("PHCN", "PHCN"),
        ("IKEJA Electricity", "IKEJA Electricity"),
        ("Abuja Electricity", "Abuja Electricity"),
    ]

    CABLES_CHOICES =[
        ("DSTV", "DSTV"),
        ("GOTV", "GOTV"),
        ("Startimes", "Startimes"),
    ]

    WATER_CHOICES =[
        ("Nigeria Water Cooperation", "Nigeria Water Cooperation"),
        ("General Waters", "General Waters"),
        ("Lagos Inc", "Lagos Inc"),
    ]

    account_number = models.ForeignKey(Account_table, on_delete=models.CASCADE, related_name='bill_payments_by_account', null=True)
    account_type = models.CharField(max_length=20, unique=False, null=True)
    account_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    bill_type = models.CharField(max_length=20, choices=BILL_TYPE_CHOICES, null=False)
    amount = models.BigIntegerField(unique=False, null=False)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    transaction_date = models.DateTimeField(auto_now_add=True)
    reference = models.CharField(max_length=50, unique=True)
    meter_number = models.CharField(max_length=20, unique=False, null=True, blank=True)
    request_type = models.CharField(choices=REQUEST_TYPE_CHOICES, null=True, max_length=20, blank=True)
    months_of_sub = models.CharField(choices=MONTHS_OF_SUB_CHOICES, null=True, max_length=5, blank=True)
    decoder_number = models.CharField(max_length=20, unique=False, null=True, blank=True)
    water_service_number = models.CharField(max_length=20, unique=False, null=True)
    electricity_type = models.CharField(choices=ELECT_CHOICES, null=True, max_length=20, blank=True)
    cable_type = models.CharField(choices=CABLES_CHOICES, null=True, max_length=20, blank=True)
    water_bill_type = models.CharField(choices=WATER_CHOICES, null=True, max_length=50, blank=True)


   
    

    def __str__(self):
        return f"{self.account_number}" # return account number field on form
        return f"{self.account_type}"
        return f"₦{self.account_balance}"


class Transaction_table(models.Model):

    networks = [
        ("MTN", "MTN"),
        ("GLO", "GLO"),
        ("AIRTEL", "AIRTEL"),
        ("ETISALAT", "ETISALAT"),
    ] 


    bill_choices = [
        ("Electricity", "Electricity"),
        ("Cable", "Cable"),
        ("Water Bill", "Water Bill"),
        
    ] 

    transaction_id = models.AutoField(primary_key=True)
    account_type_fk = models.ForeignKey(Account_table, on_delete=models.CASCADE, related_name='transaction_account_type', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account_table, on_delete=models.CASCADE)
    transaction_type = models.CharField(unique=False, max_length=20)
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_amount = models.BigIntegerField(unique=False)
    recepient_phone_number = models.CharField(max_length=11, null=True)
    recepient_bank_name = models.CharField(max_length=20, null=True)
    recepient_account_number = models.CharField(max_length=10, null=True)
    sender_bank_name = models.CharField(max_length=10, null=True)
    sender_account_number = models.ForeignKey(Account_table, related_name='sender', on_delete=models.CASCADE, unique=False, null=True)
    bill_type = models.ForeignKey(Bill_payment, on_delete=models.CASCADE, related_name='transaction_bill_type', null=True)
    mobile_networks = models.CharField(choices=networks, max_length=20, null=True)


    def __str__(self):
        return f"{self.reference} - {self.transaction_type} - ₦{self.amount} by {self.user.username}"



