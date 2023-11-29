from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    first_name = models.CharField( 
        verbose_name='First name', 
        max_length=128 
    ) 
    last_name = models.CharField( 
        verbose_name='Last name', 
        max_length=128 
    ) 
    email = models.EmailField( 
        verbose_name='Email', 
        max_length=128,
        unique=True
    ) 
    password = models.CharField(
        verbose_name='Password',
        max_length=128
    )
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Supporter(models.Model):
    #The first element in each tuple is the actual value to be set on the model, 
    #and the second element is the human-readable name.  
    SUPPORTER_STATUS = [ 
        ("Available", "Available"), 
        ("Processing", "Processing"), 
    ] 
    user = models.OneToOneField( 
        User, 
        on_delete=models.CASCADE, 
        verbose_name='User' 
    ) 
    status = models.CharField( 
        verbose_name='Status', 
        max_length=64, 
        choices=SUPPORTER_STATUS, 
        default = SUPPORTER_STATUS[0][0] 
    ) 

class Tickets(models.Model): 
    TICKET_STATUS = [ 
        ("New", "New"), 
        ("Processing", "Processing"), 
        ("Frozen", "Frozen"), 
        ("Done", "Done"), 
    ] 
    sender = models.ForeignKey( 
        User, 
        on_delete=models.CASCADE, 
        verbose_name='Sender' 
    ) 
    supporter = models.ForeignKey( 
        Supporter, 
        on_delete=models.CASCADE, 
        verbose_name='Supporter', 
        null=True 
    ) 
    description = models.TextField( 
        verbose_name='Problem desciption', 
        max_length=2048 
    ) 
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 
    status = models.CharField( 
        verbose_name='Status', 
        max_length=64, 
        choices=TICKET_STATUS, 
        default = TICKET_STATUS[0][0] 
    ) 