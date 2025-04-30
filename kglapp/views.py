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
# from .models import UserProfile
from django.shortcuts import render
from django.db.models import Sum
from .models import Sale, Procurement, CreditList
from django.shortcuts import render, redirect
from .forms import ProductForm
from django.shortcuts import render
from .models import Product
from django.shortcuts import render, redirect
from .models import Branch
from .forms import BranchForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Procurement
from .forms import ProcurementForm  
def index(request):
    return render(request, "index.html")

def home(request):
    return render(request,"home.html")
 


# View for listing procurements (Procurement List)
def procurement_list(request):
    procurements = Procurement.objects.all()
    print(procurements)  # Debugging: Check if data is retrieved
    return render(request, 'procurement_list.html', {'procurements': procurements})

# View for adding a new procurement
def add_procurement(request):
    if request.method == 'POST':
        form = ProcurementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('procurement_list')
        else:
            print("Form errors:", form.errors) 
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
            return redirect("credit_list")  
        else:
            print(form.errors) 
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


from django.shortcuts import render, redirect
# from .forms import CustomSignupForm

def signup(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # redirect to your login page
    else:
        form = CustomSignupForm()
    return render(request, 'signup.html', {'form': form})


def credit_list(request):
    credits = CreditSale.objects.all()
    return render(request, 'credit_list.html', {'credits': credits})

def is_director(user):
    return user.is_superuser  # Only superusers can access the director dashboard

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from .models import Branch, Procurement, Sale, CreditSale
from django.db.models import Sum

@login_required
def director_dashboard(request):
    # Fetch all branches
    branches = Branch.objects.all()

    # Calculate totals across all branches
    total_procurement_kg = Procurement.objects.aggregate(total_kg=Sum('tonnage_kg'))['total_kg'] or 0
    total_sales_kg = Sale.objects.aggregate(total_kg=Sum('tonnage_kg'))['total_kg'] or 0
    total_sales_amount = Sale.objects.aggregate(total_amount=Sum('amount_paid'))['total_amount'] or 0
    total_credit_due = CreditSale.objects.aggregate(total_due=Sum('amount_due'))['total_due'] or 0

    # Prepare branch data
    branch_data = []
    for branch in branches:
        total_procurement = Procurement.objects.filter(branch_name__iexact=branch.name).aggregate(
            total_kg=Sum('tonnage_kg')
        )['total_kg'] or 0

        total_sales = Sale.objects.filter(branch_name__iexact=branch.name).aggregate(
            total_kg=Sum('tonnage_kg'),
            total_amount=Sum('amount_paid')
        )

        total_credit = CreditSale.objects.filter(branch_name__iexact=branch.name).aggregate(
            total_due=Sum('amount_due'),
            total_kg=Sum('tonnage_kg')
        )

        branch_data.append({
            'branch': branch,
            'total_procurement': total_procurement,
            'total_sales_kg': total_sales['total_kg'] or 0,
            'total_sales_amount': total_sales['total_amount'] or 0,
            'total_credit_due': total_credit['total_due'] or 0,
            'total_credit_kg': total_credit['total_kg'] or 0,
            'sales_count': Sale.objects.filter(branch_name__iexact=branch.name).count(),
            'credit_count': CreditSale.objects.filter(branch_name__iexact=branch.name).count(),
        })

    # Context to pass to the template
    context = {
        'branches': branches,
        'total_procurement_kg': total_procurement_kg,
        'total_sales_kg': total_sales_kg,
        'total_sales_amount': total_sales_amount,
        'total_credit_due': total_credit_due,
        'branch_data': branch_data,
    }

    return render(request, 'director_dashboard.html', context)
@login_required
def manager_dashboard_maganjo(request):
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

    return render(request, 'manager_dashboard_maganjo.html', context)


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



# def company_rules(request):
#     return render(request, 'company_rules.html')


# views.py

# def user_profile(request):
#     profile = UserProfile.objects.get(user=request.user)
#     return render(request, 'user_profile.html', {'profile': profile})



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



def credit_recovery_report(request):
    credit_records = CreditList.objects.all().order_by('-due_date')
    return render(request, 'credit_recovery_report.html', {'credit_records': credit_records})




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




def branch_list(request):
    branches = Branch.objects.all()
    return render(request, 'branch_list.html', {'branches': branches})

def add_branch(request):
    if request.method == 'POST':
        form = BranchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('branch_list')
    else:
        form = BranchForm()
    return render(request, 'add_branch.html', {'form': form})




from .models import Sale  # Import the Sale model
from datetime import date  # Import date from datetime

def sales_agent_dashboard_matugga(request):
    today = date.today()  # Get today's date
    
    # Example logic to calculate today's sales for Matugga branch
    todays_sales = Sale.objects.filter(branch_name='Matugga', date=today)
    todays_sales_kg = sum(sale.tonnage_kg for sale in todays_sales)
    todays_sales_amount = sum(sale.amount_paid for sale in todays_sales)
    
    # Example logic for monthly sales calculation
    first_day_of_month = today.replace(day=1)
    monthly_sales = Sale.objects.filter(branch_name='Matugga', date__gte=first_day_of_month)
    monthly_sales_amount = sum(sale.amount_paid for sale in monthly_sales)

    # Render the template with the context
    context = {
        'todays_sales_kg': todays_sales_kg,
        'todays_sales_amount': todays_sales_amount,
        'monthly_sales_amount': monthly_sales_amount,
    }
    return render(request, 'sales_agent_dashboard_matugga.html', context)



from .models import Sale  # Import the Sale model
from datetime import date  # Import date from datetime

def sales_agent_dashboard_maganjo(request):
    today = date.today()  # Get today's date
    
    # Example logic to calculate today's sales for Maganjo branch
    todays_sales = Sale.objects.filter(branch_name='Maganjo', date=today)
    todays_sales_kg = sum(sale.tonnage_kg for sale in todays_sales)
    todays_sales_amount = sum(sale.amount_paid for sale in todays_sales)
    
    # Example logic for monthly sales calculation
    first_day_of_month = today.replace(day=1)
    monthly_sales = Sale.objects.filter(branch_name='Maganjo', date__gte=first_day_of_month)
    monthly_sales_amount = sum(sale.amount_paid for sale in monthly_sales)

    # Render the template with the context
    context = {
        'todays_sales_kg': todays_sales_kg,
        'todays_sales_amount': todays_sales_amount,
        'monthly_sales_amount': monthly_sales_amount,
    }
    return render(request, 'sales_agent_dashboard_maganjo.html', context)



from django.shortcuts import render, get_object_or_404
from .models import Sale

def sale_detail(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    return render(request, 'sale_detail.html', {'sale': sale})


from django.shortcuts import render, get_object_or_404
from .models import Sale, Receipt
from django.http import HttpResponse

def generate_receipt(request, sale_id):
    # Get the sale object by ID
    sale = get_object_or_404(Sale, pk=sale_id)
    
    # Check if receipt already exists for the sale
    try:
        receipt = Receipt.objects.get(sale=sale)
    except Receipt.DoesNotExist:
        # If no receipt, create one
        receipt = Receipt.objects.create(
            sale=sale,
            receipt_number=f"R{sale.id}",
            issued_by=request.user.username
        )

    # Render the receipt template
    return render(request, 'receipt.html', {'sale': sale, 'receipt': receipt})


# views.py
from django.shortcuts import render
from .models import Sale

def sales_by_branch(request, branch_name):
    sales = Sale.objects.filter(branch_name=branch_name)
    return render(request, 'sales_by_branch.html', {
        'sales': sales,
        'branch_name': branch_name
    })


from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.contrib import messages

def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Check for the user's group and redirect based on role
            if user.groups.filter(name='director').exists():
                return redirect('director_dashboard')  # Redirect to Director Dashboard

            elif user.groups.filter(name='manager').exists():
                # Ensure the manager has a branch assigned
                if hasattr(user, 'branch'):
                    if user.branch.lower() == 'matugga':
                        return redirect('manager_dashboard_matugga')
                    elif user.branch.lower() == 'maganjo':
                        return redirect('manager_dashboard_maganjo')
                else:
                    messages.error(request, 'Manager branch not specified.')
                    return redirect('login')

            elif user.groups.filter(name='sales_agent').exists():
                # Ensure the sales agent has a branch assigned
                if hasattr(user, 'branch'):
                    if user.branch.lower() == 'matugga':
                        return redirect('sales_agent_dashboard_matugga')
                    elif user.branch.lower() == 'maganjo':
                        return redirect('sales_agent_dashboard_maganjo')
                else:
                    messages.error(request, 'Sales Agent branch not specified.')
                    return redirect('login')

            else:
                messages.error(request, 'Unauthorized role.')
                return redirect('login')
        
        else:
            messages.error(request, 'Invalid username or password.')

    # Handle GET request (form rendering)
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form, 'title': 'Login'})


from django.utils import timezone
from datetime import datetime
from django.db.models import Sum
from .models import Sale, Branch
from django.contrib.auth.decorators import login_required

@login_required
def branch_sales_report(request):
    today = timezone.now().date()
    month_start = today.replace(day=1)

    branches = Branch.objects.all()

    branch_reports = []

    for branch in branches:
        # Daily sales for branch
        daily_sales = Sale.objects.filter(
            branch_name=branch.name,
            date=today  # ❗ Corrected from created_at__date to date
        ).aggregate(
            total_kg=Sum('tonnage_kg'),
            total_amount=Sum('amount_paid')
        )

        # Monthly sales for branch
        monthly_sales = Sale.objects.filter(
            branch_name=branch.name,
            date__gte=month_start,  # ❗ Corrected from created_at__date__gte to date__gte
            date__lte=today
        ).aggregate(
            total_kg=Sum('tonnage_kg'),
            total_amount=Sum('amount_paid')
        )

        branch_reports.append({
            'branch': branch,
            'daily_sales_kg': daily_sales['total_kg'] or 0,
            'daily_sales_amount': daily_sales['total_amount'] or 0,
            'monthly_sales_kg': monthly_sales['total_kg'] or 0,
            'monthly_sales_amount': monthly_sales['total_amount'] or 0,
        })

    context = {
        'branch_reports': branch_reports,
        'today': today,
        'this_month': month_start.strftime('%B %Y'),  # e.g., April 2025
    }

    return render(request, 'branch_sales_report.html', context)


from .forms import CustomUserCreationForm

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})
