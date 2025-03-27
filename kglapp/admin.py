from django.contrib import admin

# Register your models here.
from .models import Procurement,Sale,CreditSale
admin.site.register(Procurement)
admin.site.register(Sale)
admin.site.register(CreditSale)
