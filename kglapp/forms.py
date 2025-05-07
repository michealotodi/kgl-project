from django import forms
from .models import Procurement
from django import forms
from .models import Sale
from django import forms
from .models import CreditSale, CreditList
from django import forms
from .models import Product


from django import forms
from django.core.exceptions import ValidationError
from .models import Procurement
import re

class ProcurementForm(forms.ModelForm):
    class Meta:
        model = Procurement
        fields = [
            "produce_name",
            "produce_type",
            "date",
            "time",
            "tonnage_kg",
            "cost_ugx",
            "dealer_name",
            "branch_name",
            "contact",
            "selling_price_ugx",
            "source",
            "description",
            "category",
        ]
        widgets = {
            "date": forms.SelectDateWidget(),  # Date picker for the date field
            "time": forms.TimeInput(attrs={"type": "time"}),  # Time picker
        }

    def clean(self):
        cleaned_data = super().clean()
        produce_name = cleaned_data.get("produce_name")
        produce_type = cleaned_data.get("produce_type")
        tonnage_kg = cleaned_data.get("tonnage_kg")
        cost_ugx = cleaned_data.get("cost_ugx")
        dealer_name = cleaned_data.get("dealer_name")
        contact = cleaned_data.get("contact")
        source = cleaned_data.get("source")

        # Produce name: alphanumeric check
        if produce_name and not re.match(r'^[\w\s-]+$', produce_name):
            self.add_error("produce_name", "Produce name must be alphanumeric.")

        # Produce type: alphabetic and at least 2 characters
        if produce_type and (not produce_type.isalpha() or len(produce_type) < 2):
            self.add_error("produce_type", "Produce type must be at least 2 letters and contain only alphabets.")

        # Tonnage: numeric, at least 3 characters (i.e., >= 100)
        if tonnage_kg and tonnage_kg < 100:
            self.add_error("tonnage_kg", "Tonnage must be at least 100 kg.")

        # Tonnage validation for individual dealers
        if source == "Dealer" and tonnage_kg and tonnage_kg < 1000:
            self.add_error("tonnage_kg", "Individual dealers must supply at least 1000 kg.")

        # Cost: numeric, at least 5 digits (i.e., >= 10000)
        if cost_ugx and cost_ugx < 10000:
            self.add_error("cost_ugx", "Cost must be at least 5 digits (e.g. 10000 UgX).")

        # Dealer name: alphanumeric and at least 2 characters
        if dealer_name and (not re.match(r'^[\w\s-]+$', dealer_name) or len(dealer_name) < 2):
            self.add_error("dealer_name", "Dealer name must be alphanumeric and at least 2 characters.")

        # Contact: phone number format
        if contact and not re.match(r'^(\+256|0)\d{9}$', contact):
            self.add_error("contact", "Enter a valid Ugandan phone number (e.g. 07XXXXXXXX or +2567XXXXXXXX).")


from django import forms
from django.core.exceptions import ValidationError
from .models import Sale

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = "__all__"  # Includes all fields now (including branch_name)
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),  # Date input widget
            "time": forms.TimeInput(attrs={"type": "time"}),  # Time input widget
        }

    def clean(self):
        cleaned_data = super().clean()
        amount_paid = cleaned_data.get("amount_paid")
        buyer_name = cleaned_data.get("buyer_name")
        sales_agent = cleaned_data.get("sales_agent")

        # Amount paid validation (at least 5 digits)
        if amount_paid is None or amount_paid < 10000:  # At least 5 digits (10000 UgX)
            self.add_error("amount_paid", "Amount paid must be at least 5 digits (e.g., 10000 UgX).")

        # Buyer name validation (at least 2 characters)
        if not buyer_name or len(buyer_name.strip()) < 2:
            self.add_error("buyer_name", "Buyer's name must be at least 2 characters.")

        # Sales agent name validation (at least 2 characters)
        if not sales_agent or len(sales_agent.strip()) < 2:
            self.add_error("sales_agent", "Sales agent name must be at least 2 characters.")


class CreditSaleForm(forms.ModelForm):
    class Meta:
        model = CreditSale
        fields = "__all__"  # Includes all fields
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),  # Date input for due date
            "dispatch_date": forms.DateInput(attrs={"type": "date"}),  # Date input for dispatch date
        }

    def clean(self):
        cleaned_data = super().clean()
        
        # Get all the data from the form
        national_id = cleaned_data.get("national_id")
        contact = cleaned_data.get("contact")
        amount_due = cleaned_data.get("amount_due")
        buyer_name = cleaned_data.get("buyer_name")
        sales_agent = cleaned_data.get("sales_agent")
        tonnage_kg = cleaned_data.get("tonnage_kg")
        produce_name = cleaned_data.get("produce_name")
        
        # Validate National ID (14 characters)
        if not re.match(r"^[A-Z0-9]{14}$", national_id):
            self.add_error("national_id", "National ID must be in the valid format (e.g., 12345678901234).")
        
        # Validate Contact (valid phone format)
        if not re.match(r"^\+?(\d{10}|\d{12})$", contact):
            self.add_error("contact", "Contact number must be a valid phone number (e.g., +256701234567).")
        
        # Validate Amount Due (at least 5 digits)
        if amount_due and amount_due < 10000:
            self.add_error("amount_due", "Amount due must be at least 5 digits (e.g., 10000 UgX).")
        
        # Validate Buyer's Name (at least 2 characters)
        if len(buyer_name.strip()) < 2:
            self.add_error("buyer_name", "Buyer's name must be at least 2 characters.")
        
        # Validate Sales Agent's Name (at least 2 characters)
        if len(sales_agent.strip()) < 2:
            self.add_error("sales_agent", "Sales agent name must be at least 2 characters.")
        
        # Validate Tonnage (should be numeric and greater than 0)
        if tonnage_kg <= 0:
            self.add_error("tonnage_kg", "Tonnage must be a positive number.")
        
        # Validate Produce Name (at least 2 characters)
        if len(produce_name.strip()) < 2:
            self.add_error("produce_name", "Produce name must be at least 2 characters.")

# forms.py


# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = [
#             "produce_name",
#             "produce_type",
#             "unit_price",
#             "description",
#             "category",
#             "stock",
#             "minimum_stock_level",
#         ]


# forms.py
from django import forms
from .models import FAQ


class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ["question"]
        widgets = {
            "question": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Ask your question..."}
            ),
        }


from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label="Your Name")
    email = forms.EmailField(required=True, label="Your Email Address")
    message = forms.CharField(
        widget=forms.Textarea, required=True, label="Your Message"
    )


# forms.py

from django import forms
from .models import Supplier


from django import forms
from .models import Supplier

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'


from django import forms
from .models import Branch


class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ["name", "location", "manager_name", "phone", "email"]


# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from .models import UserProfile, Branch

# class CustomSignupForm(UserCreationForm):
#     branch = forms.ModelChoiceField(queryset=Branch.objects.none(), required=False, empty_label="No branch assigned")

#     class Meta:
#         model = UserProfile
#         fields = ['username', 'email', 'address', 'phonenumber', 'gender', 'is_salesagent', 'is_manager', 'is_director', 'branch']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['branch'].queryset = Branch.objects.all()

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.is_active = True
#         if commit:
#             user.save()
#         return user

# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "password1",
            "password2",
            "groups",
            "user_permissions",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "POST"
        self.helper.add_input(Submit("submit", "Create Account"))
