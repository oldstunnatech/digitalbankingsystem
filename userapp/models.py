from django.db import models
from django.contrib.auth.models import User 
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    countries=[
        ("Nigeria", "Nigeria"),
        ("Ghana", "Ghana"),
        ("UK", "UK"),
        ("USA", "USA"),
    ]

    states=[
        ("Abia", "Abia"),
        ("Adamawa", "Adamawa"),
        ("Akwa Ibom", "Akwa Ibom"),
        ("Anambra", "Anambra"),
        ("Bauchi", "Bauchi"),
        ("Bayelsa", "Bayelsa"),
        ("Benue", "Benue"),
        ("Borno", "Borno"),
        ("Cross River", "Cross River"),
        ("Delta", "Delta"),
        ("Ebonyi", "Ebonyi"),
        ("Edo", "Edo"),
        ("Ekiti", "Ekiti"),
        ("Enugu", "Enugu"),
        ("Gombe", "Gombe"),
        ("Imo", "Imo"),
        ("Jigawa", "Jigawa"),
        ("Kaduna", "Kaduna"),
        ("Kano", "Kano"),
        ("Katsina", "Katsina"),
        ("Kebbi", "Kebbi"),
        ("Kogi", "Kogi"),
        ("Kwara", "Kwara"),
        ("Lagos", "Lagos"),
        ("Nasarawa", "Nasarawa"),
        ("Niger", "Niger"),
        ("Ogun", "Ogun"),
        ("Ondo", "Ondo"),
        ("Osun", "Osun"),
        ("Oyo", "Oyo"),
        ("Plateau", "Plateau"),
        ("Rivers", "Rivers"),
        ("Sokoto", "Sokoto"),
        ("Taraba", "Taraba"),
        ("Yobe", "Yobe"),
        ("Zamfara", "Zamfara"),
        ("FCT Abuja", "FCT Abuja"),
    ]
    position = [
        ("CEO", "CEO"),
        ("GMD", "GMD"),
        ("CTO", "CTO"),
        ("Supervisor", "Supervisor"),
        ("Accountant", "Accountant"),
        ("Marketer", "Marketer"),
        ("Cashier", "Cashier"),
        ("Driver", "Driver"),
        ("Customer care", "Customer care")
    
    ]

    marital_status = [
        ("Single", "Single"),
        ("Engaged", "Engaged"),
        ("Married", "Married"),
        ("Divorce", "Divorce"),
        ("Complicated", "Complicated"),
        ("Widow", "Widow"),
    ]

    user_status = [
        ("Active", "Active"),
        ("Retired", "Retired"),
        ("Suspended", "Suspended"),
        ("Freeze", "Freeze"),
        ("On Leave", "On Leave"),
    ]

    sex = [
        ("Male", "Male"),
        ("Female", "Female"),
    ]



    profile = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    middle_name = models.CharField(unique=False, null=True, max_length=20)
    email = models.EmailField(unique=True, null=True, max_length=50)
    date_of_birth = models.DateField(unique=False, null=True, max_length=20, blank=True)
    phone_number = models.CharField(unique=True, max_length=11, null=True)
    sex = models.CharField(choices=sex, max_length=20, null=True, unique=False)
    nationality = models.CharField(choices=countries, unique=False, max_length = 50, null=True)
    state = models.CharField(choices=states, unique=False, max_length=50, null=True)
    city = models.CharField(unique=False, max_length=50, null=True)
    address = models.CharField(unique=False, max_length=100, null=True)
    occupation = models.CharField(unique=False, null=True, max_length=50)
    means_of_identity = models.ImageField(upload_to='identityImage/', unique=False, null=True)
    BVN = models.CharField(unique=True, null=True, max_length=11)
    NIN = models.CharField(unique=True, null=True, max_length=11)
    electricity_bills = models.FileField(upload_to='particularsImage/', unique=False, null=True)
    profile_passport = models.ImageField(upload_to='userimage/', unique=False, null=True)
    position = models.CharField(choices=position, unique=False, max_length=20, null=True)
    marital_status = models.CharField(choices=marital_status, unique=False, max_length=20, null=True)
    staff = models.BooleanField(default=False, unique=False, null=True)
    user_status = models.CharField(choices=user_status, unique=False, max_length=20, null=True)




    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    
    





