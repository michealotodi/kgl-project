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
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum, Count
from .models import Procurement, Sale, CreditSale
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Procurement, Sale, CreditSale
from django.db.models import Sum
from django.shortcuts import render
from .models import Sale
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import UserProfile
from django.shortcuts import render
from django.db.models import Sum
from .models import Sale, Procurement, CreditList
from django.shortcuts import render, redirect
from .forms import ProductForm
from django.shortcuts import render
from .models import Product
def index(request):
    return render(request, "index.html")

def home(request):
    return render(request,"home.html")
 
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Procurement
from .forms import ProcurementForm  # Assuming you have a form for the model

# View for listing procurements (Procurement List)
def procurement_list(request):
    procurements = Procurement.objects.all()  # This gets all procurement records
    return render(request, 'procurement_list.html', {'procurements': procurements})

# View for adding a new procurement
def add_procurement(request):
    if request.method == 'POST':
        form = ProcurementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('procurement_list')
        else:
            print("Form errors:", form.errors)  # 🔍 This helps you debug!
    else:
        form = ProcurementForm()
    return render(request, 'procurement.html', {'form': form})

def record_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('daily_sales')
    else:
        form = SaleForm()
    
    return render(request, 'record_sale.html', {'form': form})


def sale_success(request):
    return render(request, 'sale_success.html')


def sales_list(request):
    sales = Sale.objects.all()
    return render(request, 'sales_list.html', {'sales': sales})






def record_credit_sale(request):
    if request.method == 'POST':
        form = CreditSaleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("credit_list")  # redirect after saving
        else:
            print(form.errors)  # <-- add this for debugging
    else:
        form = CreditSaleForm()
    return render(request, 'record_credit_sale.html', {'form': form})







def daily_sales_report(request):
    # Get today's date
    today = timezone.now().date()
    
    # Filter sales by today's date and group by branch
    branches = Sale.objects.filter(date=today).values('branch_name').distinct()
    
    # Prepare a dictionary to store sales per branch
    branch_sales = {}
    for branch in branches:
        sales = Sale.objects.filter(date=today, branch_name=branch['branch_name'])
        branch_sales[branch['branch_name']] = sales

    return render(request, 'daily_sales_report.html', {'branch_sales': branch_sales, 'today': today})



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



def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect("home")  
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form})


def credit_list(request):
    credits = CreditSale.objects.all()
    return render(request, 'credit_list.html', {'credits': credits})



def is_director(user):
    return user.is_superuser  # Only superusers can access the director dashboard

@user_passes_test(is_director)
def director_dashboard(request):
    total_procurement = Procurement.objects.aggregate(total_kg=Sum('tonnage_kg'))['total_kg'] or 0
    total_sales = Sale.objects.aggregate(total_kg=Sum('tonnage_kg'), total_amount=Sum('amount_paid'))
    total_credit = CreditSale.objects.aggregate(total_due=Sum('amount_due'), total_kg=Sum('tonnage_kg'))

    context = {
        'total_procurement_kg': total_procurement,
        'total_sales_kg': total_sales['total_kg'] or 0,
        'total_sales_amount': total_sales['total_amount'] or 0,
        'total_credit_due': total_credit['total_due'] or 0,
        'total_credit_kg': total_credit['total_kg'] or 0,
        'sales_count': Sale.objects.count(),
        'credit_count': CreditSale.objects.count(),
    }

    return render(request, 'director_dashboard.html', context)


@login_required
def manager_dashboard(request):
    # Let's assume the branch is stored in the manager's profile, for now hardcode for example
    manager_branch = "Maganjo"  # you can later link this to the logged-in user's profile

    # Filter data by branch
    procurements = Procurement.objects.filter(branch_name=manager_branch)
    sales = Sale.objects.filter(sales_agent__icontains=manager_branch)  # Update logic as needed
    credit_sales = CreditSale.objects.filter(sales_agent__icontains=manager_branch)

    context = {
        'branch': manager_branch,
        'total_procured': procurements.aggregate(total=Sum('tonnage_kg'))['total'] or 0,
        'total_sales': sales.aggregate(total=Sum('tonnage_kg'))['total'] or 0,
        'total_credit_sales': credit_sales.aggregate(total=Sum('tonnage_kg'))['total'] or 0,
        'total_due': credit_sales.aggregate(due=Sum('amount_due'))['due'] or 0,
        'procurement_count': procurements.count(),
        'sales_count': sales.count(),
        'credit_count': credit_sales.count(),
    }

    return render(request, 'manager_dashboard.html', context)


@login_required
def manager_dashboard_matugga(request):
    branch_name = 'Matugga'

    total_procurement_kg = Procurement.objects.filter(branch_name=branch_name).aggregate(Sum('tonnage_kg'))['tonnage_kg__sum'] or 0
    total_sales_kg = Sale.objects.filter(sales_agent__icontains=branch_name).aggregate(Sum('tonnage_kg'))['tonnage_kg__sum'] or 0
    total_sales_amount = Sale.objects.filter(sales_agent__icontains=branch_name).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    total_credit_kg = CreditList.objects.filter(sales_agent__icontains=branch_name).aggregate(Sum('tonnage_kg'))['tonnage_kg__sum'] or 0
    total_credit_due = CreditList.objects.filter(sales_agent__icontains=branch_name).aggregate(Sum('amount_due'))['amount_due__sum'] or 0

    sales_count = Sale.objects.filter(sales_agent__icontains=branch_name).count()
    credit_count = CreditList.objects.filter(sales_agent__icontains=branch_name).count()

    return render(request, 'manager_dashboard_matugga.html', {
        'branch': branch_name,
        'total_procurement_kg': total_procurement_kg,
        'total_sales_kg': total_sales_kg,
        'total_sales_amount': total_sales_amount,
        'total_credit_kg': total_credit_kg,
        'total_credit_due': total_credit_due,
        'sales_count': sales_count,
        'credit_count': credit_count,
    })

def maganjo_sales_report(request):
    today = timezone.now().date()
    maganjo_sales = Sale.objects.filter(branch_name="Maganjo", date=today)
    return render(request, 'maganjo_sales_report.html', {
        'sales': maganjo_sales,
        'today': today
    })

# kglapp/views.py

from django.shortcuts import render

def company_rules(request):
    return render(request, 'company_rules.html')


# views.py

def user_profile(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'user_profile.html', {'profile': profile})



def branch_comparison_dashboard(request):
    # List of your branches
    branches = ['Matugga', 'Maganjo']

    branch_data = {}
    for branch in branches:
        total_sales_amount = Sale.objects.filter(branch_name=branch).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
        total_sales_kg = Sale.objects.filter(branch_name=branch).aggregate(Sum('tonnage_kg'))['tonnage_kg__sum'] or 0

        total_procurement_kg = Procurement.objects.filter(branch_name=branch).aggregate(Sum('tonnage_kg'))['tonnage_kg__sum'] or 0

        total_credit_kg = CreditList.objects.filter(branch_name=branch).aggregate(Sum('tonnage_kg'))['tonnage_kg__sum'] or 0
        total_credit_due = CreditList.objects.filter(branch_name=branch).aggregate(Sum('amount_due'))['amount_due__sum'] or 0

        branch_data[branch] = {
            'total_sales_amount': total_sales_amount,
            'total_sales_kg': total_sales_kg,
            'total_procurement_kg': total_procurement_kg,
            'total_credit_kg': total_credit_kg,
            'total_credit_due': total_credit_due
        }

    return render(request, 'branch_comparison_dashboard.html', {'branch_data': branch_data})

# views.py


def credit_recovery_report(request):
    credit_records = CreditList.objects.all().order_by('-due_date')
    return render(request, 'credit_recovery_report.html', {'credit_records': credit_records})

# views.py

from django.shortcuts import render
from django.db.models import Sum, Count
from .models import Sale

def sales_agent_performance(request):
    # Aggregate data for each sales agent
    agent_data = Sale.objects.values('sales_agent').annotate(
        total_sales_amount=Sum('amount_paid'),
        total_sales_kg=Sum('tonnage_kg'),
        total_sales_count=Count('id'),  # Number of sales
        avg_sale_value=Sum('amount_paid') / Count('id')  # Average sale value
    ).order_by('-total_sales_amount')  # You can change the ordering

    # Render data to the template
    return render(request, 'sales_agent_performance.html', {'agent_data': agent_data})
# views.py

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Create this view or redirect wherever
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

# views.py


def product_list(request):
    products = Product.objects.all().order_by('-date_added')
    return render(request, 'product_list.html', {'products': products})


# views.py
from .models import FAQ
from .forms import FAQForm

def faq_view(request):
    faqs = FAQ.objects.filter(is_answered=True)  # Show only answered
    if request.method == 'POST':
        form = FAQForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('faq')  # Or show success message
    else:
        form = FAQForm()
    return render(request, 'faq.html', {'faqs': faqs, 'form': form})

from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .forms import ContactForm
from django.conf import settings

def contact_support(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Extract form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Send email to the support team
            send_mail(
                subject=f"Support Request from {name}",
                message=message,
                from_email=email,
                recipient_list=[settings.SUPPORT_EMAIL],  # Email address to receive support requests
            )

            # Optionally, redirect to a "Thank you" page
            return redirect('thank_you')

    else:
        form = ContactForm()

    return render(request, 'contact_support.html', {'form': form})

def thank_you(request):
    return render(request, 'thank_you.html')

# views.py

from django.shortcuts import render
from django.db.models import F
from .models import Product

def low_stock_alerts(request):
    low_stock_products = Product.objects.filter(stock__lte=F('minimum_stock_level'))
    return render(request, 'low_stock_alerts.html', {'low_stock_products': low_stock_products})

# views.py

from django.shortcuts import render, redirect
from .models import Supplier
from .forms import SupplierForm

# View to list all suppliers
def supplier_list(request):
    suppliers = Supplier.objects.all()  # Fetch all suppliers from the database
    return render(request, 'supplier_list.html', {'suppliers': suppliers})

# View to add a new supplier
def add_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')  # Redirect to the supplier list page after saving
    else:
        form = SupplierForm()
    return render(request, 'add_supplier.html', {'form': form})
