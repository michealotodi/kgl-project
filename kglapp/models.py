from django.db import models
from django.utils import timezone
from django.db import models
from django.db import models
from django.db import models
from django.contrib.auth.models import User

class SalesAgent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='sales_agent')
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

    produce_name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
    )

    produce_type = models.CharField(
        max_length=50,
        choices=PRODUCE_TYPE_CHOICES
    )

    date = models.DateField()
    time = models.TimeField()

    tonnage_kg = models.PositiveIntegerField(null=False, blank=False)


    cost_ugx = models.PositiveIntegerField(
        null=False,
        blank=False
    )

    dealer_name = models.CharField(
        max_length=100,
        null=False,
        blank=False
    )

    branch_name = models.CharField(
        max_length=50,
        choices=[('Matugga', 'Matugga'), ('Maganjo', 'Maganjo')],
        null=False,
        blank=False
    )

    contact = models.CharField(
        max_length=15,
        null=False,
        blank=False
    )

    selling_price_ugx = models.PositiveIntegerField(
        null=False,
        blank=False
    )

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

    description = models.TextField(blank=True, null=True)  # Add description field
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, blank=True, null=True)  # Add category field

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
    date = models.DateField(default=timezone.now)  # Optional, for auto today
    time = models.TimeField(default=timezone.now)  # ✅ auto time now
    branch_name = models.CharField(max_length=50, choices=BRANCH_CHOICES, default='Matugga')  # ✅ Add this

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




# class Sale(models.Model):
#     produce_name = models.CharField(max_length=100)
#     tonnage_kg = models.PositiveIntegerField()
#     amount_paid = models.PositiveIntegerField()
#     buyer_name = models.CharField(max_length=100)
#     sales_agent = models.CharField(max_length=100)
#     date = models.DateField(auto_now_add=True)
#     time = models.TimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.produce_name} - {self.buyer_name} on {self.date}"



    # class Produce(models.Model):
    #  name = models.CharField(max_length=255)
    #  price = models.DecimalField(max_digits=10, decimal_places=2)
    #  type = models.CharField(max_length=255)
    #  dealer = models.CharField(max_length=255)
    #  created_at = models.DateTimeField(auto_now_add=True)

    #  def __str__(self):
    #      return self.name



class Produce(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=255)
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

    # models.py


# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     branch = models.CharField(max_length=100, choices=[('Matugga', 'Matugga'), ('Maganjo', 'Maganjo')])
#     role = models.CharField(max_length=50, choices=[('Director', 'Director'), ('Manager', 'Manager'), ('Sales Agent', 'Sales Agent')])

#     def __str__(self):
#         return self.user.username



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add other fields to store user profile data
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

    
# models.py
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Fruits', 'Fruits'),
        ('Vegetables', 'Vegetables'),
        ('Cereals', 'Cereals'),
        ('Legumes', 'Legumes'),
        ('Roots', 'Roots'),
        # You can add more categories as needed
    ]

    name = models.CharField(max_length=100)
    produce_type = models.CharField(max_length=100)
    unit_price = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)  # Ensure description field is here
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    date_added = models.DateTimeField(auto_now_add=True)
    stock = models.PositiveIntegerField(default=0)
    minimum_stock_level = models.PositiveIntegerField(default=10)  # threshold

    def is_low_stock(self):
        return self.stock <= self.minimum_stock_level
    def __str__(self):
        return self.name

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_answered = models.BooleanField(default=False)  # Optional for filtering

    def __str__(self):
        return self.question

# models.py

from django.db import models

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
