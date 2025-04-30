from django.db import models
from django.utils import timezone
from django.db import models
from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

#models for salesagent
from django.conf import settings
from django.db import models

class SalesAgent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    name = models.CharField(max_length=255)
    date_joined = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def total_sales(self):
        
        return Sale.objects.filter(agent=self).aggregate(total_sales=models.Sum('quantity'))['total_sales'] or 0

    def total_commission(self, commission_rate=0.05):
       
        total_sales_value = sum([sale.quantity * sale.product.price_per_unit for sale in Sale.objects.filter(agent=self)])
        return total_sales_value * commission_rate


#models for procurement
class Procurement(models.Model):
    PRODUCE_TYPE_CHOICES = [
        ('beans', 'Beans'),
        ('maize', 'Grain Maize'),
        ('cowpeas', 'Cowpeas'),
        ('gnuts', 'G-nuts'),
        ('rice', 'Rice'),
        ('soybeans', 'Soybeans'),
    ]
    
    CATEGORY_CHOICES = [
        ('Fruits', 'Fruits'),
        ('Vegetables', 'Vegetables'),
        ('Cereals', 'Cereals'),
        ('Legumes', 'Legumes'),
        ('Roots', 'Roots'),
    ]

    produce_name = models.CharField(max_length=100, blank=False, null=False)
    produce_type = models.CharField(max_length=50, choices=PRODUCE_TYPE_CHOICES)
    date = models.DateField()
    time = models.TimeField()
    tonnage_kg = models.PositiveIntegerField(null=False, blank=False)
    cost_ugx = models.PositiveIntegerField(null=False, blank=False)
    dealer_name = models.CharField(max_length=100, null=False, blank=False)
    branch_name = models.CharField(
        max_length=50,
        choices=[('Matugga', 'Matugga'), ('Maganjo', 'Maganjo')],
        null=False,
        blank=False
    )
    contact = models.CharField(max_length=15, null=False, blank=False)
    selling_price_ugx = models.PositiveIntegerField(null=False, blank=False)
    source = models.CharField(
        max_length=100,
        choices=[
            ('Dealer', 'Individual Dealer'),
            ('Company', 'Company'),
            ('Maganjo Farm', 'Maganjo Farm'),
            ('Matugga Farm', 'Matugga Farm')
        ],
        default='Dealer',
        null=False,
        blank=False
    )
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.produce_name} - {self.dealer_name} - {self.branch_name}"



class Sale(models.Model):
    BRANCH_CHOICES = [
        ('Maganjo', 'Maganjo'),
        ('Matugga', 'Matugga'),
    ]

    produce_name = models.CharField(max_length=100)
    tonnage_kg = models.PositiveIntegerField()
    amount_paid = models.PositiveIntegerField()
    buyer_name = models.CharField(max_length=100)
    sales_agent = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)  
    time = models.TimeField(default=timezone.now) 
    branch_name = models.CharField(max_length=50, choices=BRANCH_CHOICES, default='Matugga') 

    def __str__(self):
        return f"{self.produce_name} sold to {self.buyer_name}"




class CreditSale(models.Model):
    BRANCH_CHOICES = [
    ('Maganjo', 'Maganjo'),
    ('Matugga', 'Matugga'),
]
    buyer_name = models.CharField(max_length=100)
    national_id = models.CharField(max_length=14)  
    location = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    amount_due = models.PositiveIntegerField()
    sales_agent = models.CharField(max_length=100)
    due_date = models.DateField()
    produce_name = models.CharField(max_length=100)
    produce_type = models.CharField(max_length=100)
    tonnage_kg = models.CharField(max_length=225)
    dispatch_date = models.DateField(default=timezone.now)
    branch_name = models.CharField(max_length=100, choices=BRANCH_CHOICES)

    def __str__(self):
        return f"{self.buyer_name} - {self.produce_name}"


class Produce(models.Model):
    produce_name = models.CharField(max_length=100, blank=False, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    produce_type = models.CharField(max_length=255)
    dealer = models.CharField(max_length=255)
    quantity_in_kg = models.DecimalField(max_digits=10, decimal_places=2) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CreditList(models.Model):
    buyer_name = models.CharField(max_length=100)
    national_id = models.CharField(max_length=14)
    location = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    amount_due = models.PositiveIntegerField()
    sales_agent = models.CharField(max_length=100)
    due_date = models.DateField()
    produce_name = models.CharField(max_length=100)
    produce_type = models.CharField(max_length=100)
    tonnage_kg = models.CharField(max_length=225)
    dispatch_date = models.DateField(default=timezone.now)
    branch_name = models.CharField(max_length=100)


from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserprofileManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        """
        Creates and returns a regular user with an email and password.
        """
        if not email:
            raise ValueError("Users must have an email")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        Creates and returns a superuser with the given email, username, and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, email, password, **extra_fields)


# class UserProfile(AbstractBaseUser, PermissionsMixin):
#     username = models.CharField(max_length=150, unique=True)
#     email = models.EmailField(unique=True)
#     address = models.TextField(blank=True)
#     phonenumber = models.CharField(max_length=20, blank=True)
#     gender = models.CharField(max_length=10, blank=True)

#     is_salesagent = models.BooleanField(default=False)
#     is_manager = models.BooleanField(default=False)
#     is_director = models.BooleanField(default=False)

#     # Only managers and sales agents will be linked to a branch
#     branch = models.ForeignKey('Branch', on_delete=models.SET_NULL, null=True, blank=True)

#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)

#     # The user manager
#     objects = UserprofileManager()

#     # Authentication details
#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['email']

#     def __str__(self):
#         return self.username

#     class Meta:
#         db_table = 'userProfile'
#         verbose_name = 'User'
#         verbose_name_plural = 'Users'

#     def clean(self):
#         # If the user is not a manager or sales agent, make sure they have no branch assigned
#         if not self.is_manager and not self.is_salesagent:
#             self.branch = None


    
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Fruits', 'Fruits'),
        ('Vegetables', 'Vegetables'),
        ('Cereals', 'Cereals'),
        ('Legumes', 'Legumes'),
        ('Roots', 'Roots'),
    ]
    produce_name = models.CharField(max_length=100, blank=True, null=True)
    produce_type = models.CharField(max_length=100)
    unit_price = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    date_added = models.DateTimeField(auto_now_add=True)
    stock = models.PositiveIntegerField(default=0)
    minimum_stock_level = models.PositiveIntegerField(default=10) 

    def is_low_stock(self):
        return self.stock <= self.minimum_stock_level

    def __str__(self):
        return self.name

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_answered = models.BooleanField(default=False)

    def __str__(self):
        return self.question



class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Branch(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    manager_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name


class Receipt(models.Model):
    sale = models.OneToOneField(Sale, on_delete=models.CASCADE)
    receipt_number = models.CharField(max_length=100, unique=True)
    receipt_date = models.DateField(default=timezone.now)
    issued_by = models.CharField(max_length=100)

    def __str__(self):
        return f"Receipt for {self.sale.produce_name} sold to {self.sale.buyer_name}"


# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return self.username
