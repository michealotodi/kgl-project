from django import forms
from .models import Procurement
from django import forms
from .models import Sale
from django import forms
from .models import CreditSale,CreditList
from django import forms
from .models import Product


class ProcurementForm(forms.ModelForm):
    class Meta:
        model = Procurement
        fields = ['produce_name', 'produce_type', 'date', 'time', 'tonnage_kg', 
                  'cost_ugx', 'dealer_name', 'branch_name', 'contact', 
                  'selling_price_ugx', 'source', 'description', 'category']
        widgets = {
            'date': forms.SelectDateWidget(),  # Date picker for the date field
            'time': forms.TimeInput(attrs={'type': 'time'}),  # Time picker for the time field
        }
        



class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = '__all__'  # includes branch_name now
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

        





class CreditSaleForm(forms.ModelForm):
    class Meta:
        model = CreditSale
        fields = '__all__'  # this ensures all model fields are included, including branch_name
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'dispatch_date': forms.DateInput(attrs={'type': 'date'}),
        }

# forms.py



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'produce_type', 'unit_price', 'description', 'category']  # Ensure you include the relevant fields


# forms.py
from django import forms
from .models import FAQ

class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['question']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ask your question...'}),
        }

from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label="Your Name")
    email = forms.EmailField(required=True, label="Your Email Address")
    message = forms.CharField(widget=forms.Textarea, required=True, label="Your Message")

# forms.py

from django import forms
from .models import Supplier

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_name', 'phone_number', 'email', 'address']
