from django.db import models
from django.utils import timezone
from django.db import models
from django.db import models


class Procurement(models.Model):
    PRODUCE_TYPE_CHOICES = [
        ('beans', 'Beans'),
        ('maize', 'Grain Maize'),
        ('cowpeas', 'Cowpeas'),
        ('gnuts', 'G-nuts'),
        ('rice', 'Rice'),
        ('soybeans', 'Soybeans'),
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

    tonnage_kg = models.PositiveIntegerField(
       max_length=10,
       null=False,
       blank=False
    )

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

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.produce_name} - {self.dealer_name} - {self.branch_name}"





class Sale(models.Model):
    produce_name = models.CharField(max_length=100)
    tonnage_kg = models.PositiveIntegerField()
    amount_paid = models.PositiveIntegerField()
    buyer_name = models.CharField(max_length=100)
    sales_agent = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.produce_name} sold to {self.buyer_name}"
    



class CreditSale(models.Model):
    buyer_name = models.CharField(max_length=100)
    national_id = models.CharField(max_length=14)  # NIN format
    location = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    amount_due = models.PositiveIntegerField()
    sales_agent = models.CharField(max_length=100)
    due_date = models.DateField()
    produce_name = models.CharField(max_length=100)
    produce_type = models.CharField(max_length=100)
    tonnage = models.PositiveIntegerField()
    dispatch_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.buyer_name} - {self.produce_name}"




class Sale(models.Model):
    produce_name = models.CharField(max_length=100)
    tonnage_kg = models.PositiveIntegerField()
    amount_paid = models.PositiveIntegerField()
    buyer_name = models.CharField(max_length=100)
    sales_agent = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.produce_name} - {self.buyer_name} on {self.date}"



    class Produce(models.Model):
     name = models.CharField(max_length=255)
     price = models.DecimalField(max_digits=10, decimal_places=2)
     type = models.CharField(max_length=255)
     dealer = models.CharField(max_length=255)
     created_at = models.DateTimeField(auto_now_add=True)

     def __str__(self):
         return self.name



class Produce(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=255)
    dealer = models.CharField(max_length=255)
    quantity_in_kg = models.DecimalField(max_digits=10, decimal_places=2)  # For tracking stock
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


