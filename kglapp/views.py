from django.shortcuts import render,redirect
from .forms import ProcurementForm
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import SaleForm
from .models import Sale
from django.shortcuts import render, redirect
from .forms import CreditSaleForm
from .models import CreditSale
from django.shortcuts import render,redirect
from .models import Sale
from django.utils.timezone import now
from datetime import datetime
from django.shortcuts import render,redirect
from .models import Produce
from django.shortcuts import render
from .models import Procurement
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.shortcuts import render
from .models import CreditSale
from django.shortcuts import render
from django.shortcuts import render
from .models import CreditList



def index(request):
    return render(request, "index.html")

def home(request):
    return render(request,"home.html")
 
def add_procurement(request):
    if request.method == 'POST':
        # If the form is submitted (POST request)
        form = ProcurementForm(request.POST)
        
        if form.is_valid():
            # If the form is valid, save the procurement record
            form.save()
            # Optionally, add a success message
            messages.success(request, "Procurement record added successfully!")
            return redirect('home')  # Redirect to procurement list view or another page
        else:
            # If the form is not valid, send an error message
            messages.error(request, "There was an error with your submission. Please check the form.")
    else:
        # If it's a GET request, just show the empty form
        form = ProcurementForm()

    # Render the form in the template
    return render(request, 'procurement.html', {'form': form})

# View to record a new sale
def record_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('daily_sales')
    else:
        form = SaleForm()
    
    return render(request, 'record_sale.html', {'form': form})

# View to show a success message
def sale_success(request):
    return render(request, 'sale_success.html')

# (Optional) View to list all sales records
def sales_list(request):
    sales = Sale.objects.all()
    return render(request, 'sales_list.html', {'sales': sales})






def record_credit_sale(request):
    if request.method == 'POST':
        form = CreditSaleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("credit_list")
    else:
        form = CreditSaleForm()
    return render(request, 'record_credit_sale.html', {'form': form})

# def list_credit_sales_(request):
#     credits = CreditSale.objects.all()
#     return render(request, 'list_credit_sales.html', {'credits': credits})



def daily_sales_report(request):
   sales = Sale.objects.all()
   return render(request,'daily_sales_report.html',{'sales':sales})


""""
def stock_page(request):
    # Fetch all produce items that are in stock
    stock_items = Produce.objects.all()  # You can apply filters if you want to show only certain stock
    return render(request, 'stock_page.html', {'stock_items': stock_items})

def stock_page(request):
    search_query = request.GET.get('search', '')
    if search_query:
        stock_items = Produce.objects.filter(name__icontains=search_query)
    else:
        stock_items = Produce.objects.all()

    return render(request, 'stock_page.html', {'stock_items': stock_items, 'search_query': search_query})
"""


def stock_page(request):
    search_query = request.GET.get('search', '')
    
    if search_query:
        stock_items = Procurement.objects.filter(produce_name__icontains=search_query)
    else:
        stock_items = Procurement.objects.all()

    return render(request, 'stock_page.html', {
        'stock_items': stock_items,
        'search_query': search_query
    })

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the new user automatically
            return redirect("home")  # Change to your actual home route
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form})


def credit_list(request):
    credits = CreditList.objects.all()  # Query all items
    print(CreditList.objects.all())  # Should return a QuerySet with records

    return render(request, 'credit_list.html', {'credits': credits})



