from django import forms
from .models import Procurement
from django import forms
from .models import Sale
from django import forms
from .models import CreditSale

# from django import forms
# from .models import Produce

class ProcurementForm(forms.ModelForm):
    class Meta:
        model = Procurement
        fields = [
            'produce_name', 
            'produce_type', 
            'date', 
            'time', 
            'tonnage_kg', 
            'cost_ugx', 
            'dealer_name', 
            'branch_name', 
            'contact', 
            'selling_price_ugx', 
            'source'
        ]
        



class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = '__all__'

        




class CreditSaleForm(forms.ModelForm):
    class Meta:
        model = CreditSale
        fields = '__all__'
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'dispatch_date': forms.DateInput(attrs={'type': 'date'}),
        }







