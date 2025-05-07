from datetime import date, datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.mail import send_mail
from django.db.models import Count, F, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import (
    BranchForm,
    ContactForm,
    CreditSaleForm,
    FAQForm,
    ProcurementForm,
    SaleForm,
    SupplierForm,
)
from .models import (
    Branch,
    CreditList,
    CreditSale,
    FAQ,
    Procurement,
    Product,
    Receipt,
    Sale,
    Supplier,
)


def index(request):
    return render(request, "index.html")


def home(request):
    return render(request, "home.html")


# View for listing procurements (Procurement List)
def procurement_list(request):
    procurements = Procurement.objects.all()
    print(procurements)  # Debugging: Check if data is retrieved
    return render(request, "procurement_list.html", {"procurements": procurements})


# View for adding a new procurement
def add_procurement(request):
    if request.method == "POST":
        form = ProcurementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("procurement_list")
        else:
            print("Form errors:", form.errors)
    else:
        form = ProcurementForm()
    return render(request, "procurement.html", {"form": form})

# Edit (Update) View
def edit_procurement(request, pk):
    procurement = get_object_or_404(Procurement, pk=pk)
    if request.method == "POST":
        form = ProcurementForm(request.POST, instance=procurement)
        if form.is_valid():
            form.save()
            messages.success(request, "Procurement record updated successfully.")
            return redirect('procurement_list')  # Change to your actual list view name
    else:
        form = ProcurementForm(instance=procurement)
    return render(request, 'edit_procurement.html', {'form': form})

# Delete View
def delete_procurement(request, pk):
    procurement = get_object_or_404(Procurement, pk=pk)
    if request.method == "POST":
        procurement.delete()
        messages.success(request, "Procurement record deleted successfully.")
        return redirect('procurement_list')
    return render(request, 'delete_procurement.html', {'procurement': procurement})



def record_sale(request):
    if request.method == "POST":
        form = SaleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("daily_sales")
    else:
        form = SaleForm()

    return render(request, "record_sale.html", {"form": form})


def sale_success(request):
    return render(request, "sale_success.html")


def daily_sales(request):
    sales = Sale.objects.all()
    return render(request, "daily_sales.html", {"sales": sales})

def edit_sale(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == "POST":
        form = SaleForm(request.POST, instance=sale)
        if form.is_valid():
            form.save()
            return redirect("daily_sales")
    else:
        form = SaleForm(instance=sale)
    return render(request, "edit_sale.html", {"form": form})

def delete_sale(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.method == "POST":
        sale.delete()
        return redirect("daily_sales")
    return render(request, "delete_sale.html", {"sale": sale})



def record_credit_sale(request):
    if request.method == "POST":
        form = CreditSaleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("credit_list")
        else:
            print(form.errors)
    else:
        form = CreditSaleForm()
    return render(request, "record_credit_sale.html", {"form": form})


# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import CreditSale
from .forms import CreditSaleForm

# Edit Credit Sale
def edit_credit_sale(request, pk):
    credit_sale = get_object_or_404(CreditSale, pk=pk)
    if request.method == "POST":
        form = CreditSaleForm(request.POST, instance=credit_sale)
        if form.is_valid():
            form.save()
            return redirect("credit_list")
    else:
        form = CreditSaleForm(instance=credit_sale)
    return render(request, "edit_credit_sale.html", {"form": form})

# Delete Credit Sale
def delete_credit_sale(request, pk):
    credit_sale = get_object_or_404(CreditSale, pk=pk)
    if request.method == "POST":
        credit_sale.delete()
        return redirect("credit_list")
    return render(request, "delete_credit_sale.html", {"credit_sale": credit_sale})

from django.shortcuts import get_object_or_404, redirect
from .models import CreditSale

def mark_as_cleared(request, pk):
    credit_sale = get_object_or_404(CreditSale, pk=pk)
    credit_sale.cleared = True  # Mark as cleared
    credit_sale.save()  # Save the changes
    return redirect('credit_list')  # Redirect back to the credit list page



def daily_sales_report(request):
    # Get today's date
    today = timezone.now().date()

    # Filter sales by today's date and group by branch
    branches = Sale.objects.filter(date=today).values("branch_name").distinct()

    # Prepare a dictionary to store sales per branch
    branch_sales = {}
    for branch in branches:
        sales = Sale.objects.filter(date=today, branch_name=branch["branch_name"])
        branch_sales[branch["branch_name"]] = sales

    return render(
        request,
        "daily_sales_report.html",
        {"branch_sales": branch_sales, "today": today},
    )


def stock_page(request):
    search_query = request.GET.get("search", "")
    if search_query:
        stock_items = Procurement.objects.filter(produce_name__icontains=search_query)
    else:
        stock_items = Procurement.objects.all()
    return render(
        request,
        "stock_page.html",
        {"stock_items": stock_items, "search_query": search_query},
    )


from django.shortcuts import render, redirect

# from .forms import CustomSignupForm


def signup(request):
    if request.method == "POST":
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # redirect to your login page
    else:
        form = CustomSignupForm()
    return render(request, "signup.html", {"form": form})


def credit_list(request):
    credits = CreditSale.objects.all()
    return render(request, "credit_list.html", {"credits": credits})


def is_director(user):
    return user.is_superuser  # Only superusers can access the director dashboard




from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
from .models import Sale, CreditSale, Procurement, Stock

@login_required
def director_dashboard(request):
    today = timezone.now().date()
    branches = ["Maganjo", "Matugga"]

    # Prepare flat stats for each branch
    branch_stats = []
    for branch in branches:
        total_sales = Sale.objects.filter(branch_name=branch).aggregate(Sum("tonnage_kg"))["tonnage_kg__sum"] or 0
        sales_amount = Sale.objects.filter(branch_name=branch).aggregate(Sum("amount_paid"))["amount_paid__sum"] or 0
        total_credit_sales = CreditSale.objects.filter(branch_name=branch).aggregate(Sum("tonnage_kg"))["tonnage_kg__sum"] or 0
        credit_due = CreditSale.objects.filter(branch_name=branch).aggregate(Sum("amount_due"))["amount_due__sum"] or 0
        total_procured = Procurement.objects.filter(branch_name=branch).aggregate(Sum("tonnage_kg"))["tonnage_kg__sum"] or 0

        branch_stats.append({
            "branch": branch,
            "total_sales": total_sales,
            "sales_amount": sales_amount,
            "total_credit_sales": total_credit_sales,
            "credit_due": credit_due,
            "total_procured": total_procured,
        })

    # Overall totals
    total_procured = Procurement.objects.aggregate(Sum("tonnage_kg"))["tonnage_kg__sum"] or 0
    total_sales = Sale.objects.aggregate(Sum("tonnage_kg"))["tonnage_kg__sum"] or 0
    total_credit_sales = CreditSale.objects.aggregate(Sum("tonnage_kg"))["tonnage_kg__sum"] or 0
    total_due = CreditSale.objects.aggregate(Sum("amount_due"))["amount_due__sum"] or 0

    low_stock_items = Stock.objects.filter(quantity__lt=100)

    context = {
        "total_procured": total_procured,
        "total_sales": total_sales,
        "total_credit_sales": total_credit_sales,
        "total_due": total_due,
        "branch_stats": branch_stats,
        "low_stock_items": low_stock_items,
    }
    return render(request, "director_dashboard.html", context)


from django.db.models import Sum
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Procurement, Sale, CreditSale, Stock

@login_required
def manager_dashboard_maganjo(request):
    today = timezone.now().date()
    current_month = today.month
    branch = "Maganjo"

    # Aggregates
    total_procured = Procurement.objects.filter(branch_name=branch).aggregate(total=Sum("tonnage_kg"))["total"] or 0
    total_sales = Sale.objects.filter(branch_name=branch).aggregate(total=Sum("tonnage_kg"))["total"] or 0
    total_credit_sales = CreditSale.objects.filter(branch_name=branch).aggregate(total=Sum("tonnage_kg"))["total"] or 0
    total_due = CreditSale.objects.filter(branch_name=branch).aggregate(total=Sum("amount_due"))["total"] or 0

    # Today's stats
    today_procured = Procurement.objects.filter(branch_name=branch, date=today).aggregate(kg=Sum("tonnage_kg"))["kg"] or 0
    today_sales_kg = Sale.objects.filter(branch_name=branch, date=today).aggregate(kg=Sum("tonnage_kg"))["kg"] or 0
    today_sales_amount = Sale.objects.filter(branch_name=branch, date=today).aggregate(amount=Sum("amount_paid"))["amount"] or 0
    today_credit_kg = CreditSale.objects.filter(branch_name=branch, dispatch_date=today).aggregate(kg=Sum("tonnage_kg"))["kg"] or 0
    today_credit_amount = CreditSale.objects.filter(branch_name=branch, dispatch_date=today).aggregate(amount=Sum("amount_due"))["amount"] or 0

    # Monthly stats
    month_procured = Procurement.objects.filter(branch_name=branch, date__month=current_month).aggregate(kg=Sum("tonnage_kg"))["kg"] or 0
    month_sales_kg = Sale.objects.filter(branch_name=branch, date__month=current_month).aggregate(kg=Sum("tonnage_kg"))["kg"] or 0
    month_sales_amount = Sale.objects.filter(branch_name=branch, date__month=current_month).aggregate(amount=Sum("amount_paid"))["amount"] or 0
    month_credit_kg = CreditSale.objects.filter(branch_name=branch, dispatch_date__month=current_month).aggregate(kg=Sum("tonnage_kg"))["kg"] or 0
    month_credit_amount = CreditSale.objects.filter(branch_name=branch, dispatch_date__month=current_month).aggregate(amount=Sum("amount_due"))["amount"] or 0

    # Low Stock
    low_stock_items = Stock.objects.filter(branch_name=branch, quantity__lt=100)

    context = {
        "branch": branch,
        "total_procured": total_procured,
        "total_sales": total_sales,
        "total_credit_sales": total_credit_sales,
        "total_due": total_due,

        "today_procured": today_procured,
        "today_sales_kg": today_sales_kg,
        "today_sales_amount": today_sales_amount,
        "today_credit_kg": today_credit_kg,
        "today_credit_amount": today_credit_amount,

        "month_procured": month_procured,
        "month_sales_kg": month_sales_kg,
        "month_sales_amount": month_sales_amount,
        "month_credit_kg": month_credit_kg,
        "month_credit_amount": month_credit_amount,

        "low_stock_items": low_stock_items,
    }

    return render(request, "manager_dashboard_maganjo.html", context)

from django.db.models import Sum
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Procurement, Sale, CreditSale, Stock

@login_required
def manager_dashboard_matugga(request):
    today = timezone.now().date()
    current_month = today.month
    branch = "Matugga"

    # Aggregates
    total_procured = Procurement.objects.filter(branch_name=branch).aggregate(total=Sum("tonnage_kg"))["total"] or 0
    total_sales = Sale.objects.filter(branch_name=branch).aggregate(total=Sum("tonnage_kg"))["total"] or 0
    total_credit_sales = CreditSale.objects.filter(branch_name=branch).aggregate(total=Sum("tonnage_kg"))["total"] or 0
    total_due = CreditSale.objects.filter(branch_name=branch).aggregate(total=Sum("amount_due"))["total"] or 0

    # Today's stats
    today_procured = Procurement.objects.filter(branch_name=branch, date=today).aggregate(kg=Sum("tonnage_kg"))["kg"] or 0
    today_sales_kg = Sale.objects.filter(branch_name=branch, date=today).aggregate(kg=Sum("tonnage_kg"))["kg"] or 0
    today_sales_amount = Sale.objects.filter(branch_name=branch, date=today).aggregate(amount=Sum("amount_paid"))["amount"] or 0
    today_credit_kg = CreditSale.objects.filter(branch_name=branch, dispatch_date=today).aggregate(kg=Sum("tonnage_kg"))["kg"] or 0
    today_credit_amount = CreditSale.objects.filter(branch_name=branch, dispatch_date=today).aggregate(amount=Sum("amount_due"))["amount"] or 0

    # Monthly stats
    month_procured = Procurement.objects.filter(branch_name=branch, date__month=current_month).aggregate(kg=Sum("tonnage_kg"))["kg"] or 0
    month_sales_kg = Sale.objects.filter(branch_name=branch, date__month=current_month).aggregate(kg=Sum("tonnage_kg"))["kg"] or 0
    month_sales_amount = Sale.objects.filter(branch_name=branch, date__month=current_month).aggregate(amount=Sum("amount_paid"))["amount"] or 0
    month_credit_kg = CreditSale.objects.filter(branch_name=branch, dispatch_date__month=current_month).aggregate(kg=Sum("tonnage_kg"))["kg"] or 0
    month_credit_amount = CreditSale.objects.filter(branch_name=branch, dispatch_date__month=current_month).aggregate(amount=Sum("amount_due"))["amount"] or 0

    # Optional: Low Stock
    low_stock_items = Stock.objects.filter(branch_name=branch, quantity__lt=100)

    context = {
        "branch": branch,
        "total_procured": total_procured,
        "total_sales": total_sales,
        "total_credit_sales": total_credit_sales,
        "total_due": total_due,
        "today_procured": today_procured,
        "today_sales_kg": today_sales_kg,
        "today_sales_amount": today_sales_amount,
        "today_credit_kg": today_credit_kg,
        "today_credit_amount": today_credit_amount,
        "month_procured": month_procured,
        "month_sales_kg": month_sales_kg,
        "month_sales_amount": month_sales_amount,
        "month_credit_kg": month_credit_kg,
        "month_credit_amount": month_credit_amount,
        "low_stock_items": low_stock_items,
    }

    return render(request, "manager_dashboard_matugga.html", context)


def maganjo_sales_report(request):
    today = timezone.now().date()
    maganjo_sales = Sale.objects.filter(branch_name="Maganjo", date=today)
    return render(
        request, "maganjo_sales_report.html", {"sales": maganjo_sales, "today": today}
    )
from django.db.models import Sum
from django.shortcuts import render
from .models import Sale, Procurement, CreditList

def branch_comparison_dashboard(request):
    branches = ["Matugga", "Maganjo"]
    branch_data = {}

    for branch in branches:
        # Fetch all data per branch
        branch_sales = Sale.objects.filter(branch_name=branch)
        branch_procurement = Procurement.objects.filter(branch_name=branch)
        branch_credit = CreditList.objects.filter(branch_name=branch)

        # Calculate totals for each branch
        total_sales_kg = branch_sales.aggregate(total=Sum("tonnage_kg"))["total"] or 0
        total_sales_amount = branch_sales.aggregate(total=Sum("amount_paid"))["total"] or 0
        total_procurement_kg = branch_procurement.aggregate(total=Sum("tonnage_kg"))["total"] or 0
        total_credit_kg = branch_credit.aggregate(total=Sum("tonnage_kg"))["total"] or 0
        total_credit_due = branch_credit.aggregate(total=Sum("amount_due"))["total"] or 0

        # Store data
        branch_data[branch] = {
            "sales": branch_sales,
            "procurements": branch_procurement,
            "credits": branch_credit,
            "total_sales_kg": total_sales_kg,
            "total_sales_amount": total_sales_amount,
            "total_procurement_kg": total_procurement_kg,
            "total_credit_kg": total_credit_kg,
            "total_credit_due": total_credit_due,
        }

    return render(request, "branch_comparison_dashboard.html", {"branch_data": branch_data})

def credit_recovery_report(request):
    credit_records = CreditList.objects.all().order_by("-due_date")
    return render(
        request, "credit_recovery_report.html", {"credit_records": credit_records}
    )
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import CreditList  # Use your actual credit model name

@login_required
def credit_recovery_report_all_branches(request):
    credit_records = CreditList.objects.all().order_by("-due_date")

    return render(
        request,
        "credit_recovery_report_all_branches.html",
        {"credit_records": credit_records}
    )


def sales_agent_performance(request):
    # Aggregate data for each sales agent
    agent_data = (
        Sale.objects.values("sales_agent")
        .annotate(
            total_sales_amount=Sum("amount_paid"),
            total_sales_kg=Sum("tonnage_kg"),
            total_sales_count=Count("id"),  # Number of sales
            avg_sale_value=Sum("amount_paid") / Count("id"),  # Average sale value
        )
        .order_by("-total_sales_amount")
    )  # You can change the ordering

    # Render data to the template
    return render(request, "sales_agent_performance.html", {"agent_data": agent_data})


# views.py


# def add_product(request):
#     if request.method == "POST":
#         form = ProductForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("product_list")  # Create this view or redirect wherever
#     else:
#         form = ProductForm()
#     return render(request, "add_product.html", {"form": form})


# views.py


# def product_list(request):
#     products = Product.objects.all().order_by("-date_added")
#     return render(request, "product_list.html", {"products": products})


# views.py



from django.contrib import messages  # ✅ Add this line

def faq_view(request):
    faqs = FAQ.objects.filter(is_answered=True)
    if request.method == "POST":
        form = FAQForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your question has been submitted successfully!")  # ✅ Added
            return redirect("faq")
    else:
        form = FAQForm()
    return render(request, "faq.html", {"faqs": faqs, "form": form})




from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from .forms import ContactForm  # Make sure you have imported your form

def contact_support(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            try:
                send_mail(
                    subject=f"Support Request from {name}",
                    message=f"From: {email}\n\n{message}",
                    from_email=settings.DEFAULT_FROM_EMAIL,  # Use a verified sender
                    recipient_list=[settings.SUPPORT_EMAIL],
                    fail_silently=False,  # Show errors if email fails
                )
                return redirect("thank_you")

            except Exception as e:
                # Optional: log or show the error during development
                print("Email sending failed:", e)
                form.add_error(None, "Failed to send email. Please try again later.")

    else:
        form = ContactForm()

    return render(request, "contact_support.html", {"form": form})
# views.py

from django.shortcuts import render

def thank_you(request):
    return render(request, "thank_you.html")



# views.py

# views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from .models import Stock

@login_required
def low_stock_alerts(request):
    user = request.user
    threshold = 10
    low_stock_products = []

    # Branch-based filtering based on user group
    if user.groups.filter(name='director').exists():
        low_stock_products = Stock.objects.filter(quantity__lt=threshold)

    elif user.groups.filter(name='manager_matugga').exists() or user.groups.filter(name='sales_agent_matugga').exists():
        low_stock_products = Stock.objects.filter(branch_name='Matugga', quantity__lt=threshold)

    elif user.groups.filter(name='manager_maganjo').exists() or user.groups.filter(name='sales_agent_maganjo').exists():
        low_stock_products = Stock.objects.filter(branch_name='Maganjo', quantity__lt=threshold)

    # Send email only once per session
    if low_stock_products and not request.session.get("low_stock_email_sent", False):
        item_list = "\n".join([
            f"{item.item} ({item.branch_name}) - Remaining: {item.quantity}"
            for item in low_stock_products
        ])

        send_mail(
            subject="🔔 KGL Low Stock Alert",
            message=f"The following items are low in stock:\n\n{item_list}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['director@kgl.com', 'manager@kgl.com'],  # Replace with real emails
            fail_silently=False
        )
        request.session["low_stock_email_sent"] = True

    return render(request, 'low_stock_alerts.html', {
        'low_stock_products': low_stock_products
    })


# View to list all suppliers
from django.shortcuts import render, redirect, get_object_or_404
from .models import Supplier
from .forms import SupplierForm

# View to list all suppliers
def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'supplier_list.html', {'suppliers': suppliers})

# Add new supplier
def add_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm()
    return render(request, 'add_supplier.html', {'form': form, 'title': 'Add Supplier'})

# Edit existing supplier
def edit_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'add_supplier.html', {'form': form, 'title': 'Edit Supplier'})

# Delete supplier
def delete_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        supplier.delete()
        return redirect('supplier_list')
    return render(request, 'confirm_delete.html', {'object': supplier})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Branch
from .forms import BranchForm

# View all branches
def branch_list(request):
    branches = Branch.objects.all()
    return render(request, 'branch_list.html', {'branches': branches})

# Add a new branch
def add_branch(request):
    if request.method == 'POST':
        form = BranchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('branch_list')
    else:
        form = BranchForm()
    return render(request, 'add_branch.html', {'form': form, 'title': 'Add Branch'})

# Edit a branch
def edit_branch(request, pk):
    branch = get_object_or_404(Branch, pk=pk)
    if request.method == 'POST':
        form = BranchForm(request.POST, instance=branch)
        if form.is_valid():
            form.save()
            return redirect('branch_list')
    else:
        form = BranchForm(instance=branch)
    return render(request, 'add_branch.html', {'form': form, 'title': 'Edit Branch'})

# Delete a branch
def delete_branch(request, pk):
    branch = get_object_or_404(Branch, pk=pk)
    if request.method == 'POST':
        branch.delete()
        return redirect('branch_list')
    return render(request, 'confirm_delete_branch.html', {'object': branch})

from django.db.models import Sum
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Sale, CreditSale

@login_required
def sales_agent_dashboard_matugga(request):
    today = timezone.now().date()
    this_month = today.month

    # Today's Cash Sales
    todays_sales = Sale.objects.filter(branch_name="Matugga", date=today)
    todays_sales_kg = todays_sales.aggregate(kg=Sum("tonnage_kg"))["kg"] or 0
    todays_sales_amount = todays_sales.aggregate(amount=Sum("amount_paid"))["amount"] or 0

    # Today's Credit Sales
    todays_credit = CreditSale.objects.filter(branch_name="Matugga", dispatch_date=today)
    todays_credit_kg = todays_credit.aggregate(kg=Sum("tonnage_kg"))["kg"] or 0
    todays_credit_amount = todays_credit.aggregate(amount=Sum("amount_due"))["amount"] or 0

    # Monthly Cash Sales
    monthly_sales = Sale.objects.filter(branch_name="Matugga", date__month=this_month)
    monthly_sales_kg = monthly_sales.aggregate(kg=Sum("tonnage_kg"))["kg"] or 0
    monthly_sales_amount = monthly_sales.aggregate(amount=Sum("amount_paid"))["amount"] or 0

    # Monthly Credit Sales
    monthly_credit = CreditSale.objects.filter(branch_name="Matugga", dispatch_date__month=this_month)
    monthly_credit_kg = monthly_credit.aggregate(kg=Sum("tonnage_kg"))["kg"] or 0
    monthly_credit_amount = monthly_credit.aggregate(amount=Sum("amount_due"))["amount"] or 0

    context = {
        "todays_sales_kg": todays_sales_kg,
        "todays_sales_amount": todays_sales_amount,
        "todays_credit_kg": todays_credit_kg,
        "todays_credit_amount": todays_credit_amount,
        "monthly_sales_kg": monthly_sales_kg,
        "monthly_sales_amount": monthly_sales_amount,
        "monthly_credit_kg": monthly_credit_kg,
        "monthly_credit_amount": monthly_credit_amount,
    }

    return render(request, "sales_agent_dashboard_matugga.html", context)

from django.db.models import Sum
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Sale, CreditSale

@login_required
def sales_agent_dashboard_maganjo(request):
    today = timezone.now().date()
    this_month = today.month

    # Today's Cash Sales for Maganjo
    todays_sales = Sale.objects.filter(branch_name="Maganjo", date=today)
    todays_sales_kg = todays_sales.aggregate(kg=Sum("tonnage_kg"))["kg"] or 0
    todays_sales_amount = todays_sales.aggregate(amount=Sum("amount_paid"))["amount"] or 0

    # Today's Credit Sales for Maganjo
    todays_credit = CreditSale.objects.filter(branch_name="Maganjo", dispatch_date=today)
    todays_credit_kg = todays_credit.aggregate(kg=Sum("tonnage_kg"))["kg"] or 0
    todays_credit_amount = todays_credit.aggregate(amount=Sum("amount_due"))["amount"] or 0

    # Monthly Cash Sales for Maganjo
    monthly_sales = Sale.objects.filter(branch_name="Maganjo", date__month=this_month)
    monthly_sales_kg = monthly_sales.aggregate(kg=Sum("tonnage_kg"))["kg"] or 0
    monthly_sales_amount = monthly_sales.aggregate(amount=Sum("amount_paid"))["amount"] or 0

    # Monthly Credit Sales for Maganjo
    monthly_credit = CreditSale.objects.filter(branch_name="Maganjo", dispatch_date__month=this_month)
    monthly_credit_kg = monthly_credit.aggregate(kg=Sum("tonnage_kg"))["kg"] or 0
    monthly_credit_amount = monthly_credit.aggregate(amount=Sum("amount_due"))["amount"] or 0

    context = {
        "todays_sales_kg": todays_sales_kg,
        "todays_sales_amount": todays_sales_amount,
        "todays_credit_kg": todays_credit_kg,
        "todays_credit_amount": todays_credit_amount,
        "monthly_sales_kg": monthly_sales_kg,
        "monthly_sales_amount": monthly_sales_amount,
        "monthly_credit_kg": monthly_credit_kg,
        "monthly_credit_amount": monthly_credit_amount,
    }

    return render(request, "sales_agent_dashboard_maganjo.html", context)




def sale_detail(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    return render(request, "sale_detail.html", {"sale": sale})



def generate_receipt(request, sale_id):
    # Get the sale object by ID
    sale = get_object_or_404(Sale, pk=sale_id)

    # Check if receipt already exists for the sale
    try:
        receipt = Receipt.objects.get(sale=sale)
    except Receipt.DoesNotExist:
        # If no receipt, create one
        receipt = Receipt.objects.create(
            sale=sale, receipt_number=f"R{sale.id}", issued_by=request.user.username
        )

    # Render the receipt template
    return render(request, "receipt.html", {"sale": sale, "receipt": receipt})




def sales_by_branch(request, branch_name):
    sales = Sale.objects.filter(branch_name=branch_name)
    return render(
        request, "sales_by_branch.html", {"sales": sales, "branch_name": branch_name}
    )




def Login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Redirect based on exact group name
            if user.groups.filter(name="director").exists():
                return redirect("director_dashboard")

            elif user.groups.filter(name="manager_matugga").exists():
                return redirect("manager_dashboard_matugga")

            elif user.groups.filter(name="manager_maganjo").exists():
                return redirect("manager_dashboard_maganjo")

            elif user.groups.filter(name="sales_agent_matugga").exists():
                return redirect("sales_agent_dashboard_matugga")

            elif user.groups.filter(name="sales_agent_maganjo").exists():
                return redirect("sales_agent_dashboard_maganjo")

            else:
                messages.error(request, "Unauthorized role.")
                return redirect("login")
        else:
            messages.error(request, "Invalid username or password.")

    form = AuthenticationForm()
    return render(request, "login.html", {"form": form, "title": "Login"})



# @login_required
# def branch_sales_report(request):
#     today = timezone.now().date()
#     month_start = today.replace(day=1)

#     branches = Branch.objects.all()

#     branch_reports = []

#     for branch in branches:
#         # Daily sales for branch
#         daily_sales = Sale.objects.filter(
#             branch_name=branch.name,
#             date=today,  # ❗ Corrected from created_at__date to date
#         ).aggregate(total_kg=Sum("tonnage_kg"), total_amount=Sum("amount_paid"))

#         # Monthly sales for branch
#         monthly_sales = Sale.objects.filter(
#             branch_name=branch.name,
#             date__gte=month_start,  # ❗ Corrected from created_at__date__gte to date__gte
#             date__lte=today,
#         ).aggregate(total_kg=Sum("tonnage_kg"), total_amount=Sum("amount_paid"))

#         branch_reports.append(
#             {
#                 "branch": branch,
#                 "daily_sales_kg": daily_sales["total_kg"] or 0,
#                 "daily_sales_amount": daily_sales["total_amount"] or 0,
#                 "monthly_sales_kg": monthly_sales["total_kg"] or 0,
#                 "monthly_sales_amount": monthly_sales["total_amount"] or 0,
#             }
#         )

#     context = {
#         "branch_reports": branch_reports,
#         "today": today,
#         "this_month": month_start.strftime("%B %Y"),  # e.g., April 2025
#     }

#     return render(request, "branch_sales_report.html", context)


from .forms import CustomUserCreationForm


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, "signup.html", {"form": form})

from django.db.models import Sum
from django.utils import timezone
from django.shortcuts import render
from .models import Sale

def matugga_daily_sales_report(request):
    today = timezone.now().date()

    # Get cash and credit sales separately
    cash_sales = Sale.objects.filter(branch_name='Matugga', date=today, payment_type='cash')
    credit_sales = Sale.objects.filter(branch_name='Matugga', date=today, payment_type='credit')

    # Calculate totals
    total_cash_kg = cash_sales.aggregate(total=Sum('tonnage_kg'))['total'] or 0
    total_cash_amount = cash_sales.aggregate(total=Sum('amount_paid'))['total'] or 0
    total_credit_kg = credit_sales.aggregate(total=Sum('tonnage_kg'))['total'] or 0
    total_credit_amount = credit_sales.aggregate(total=Sum('amount_due'))['total'] or 0

    # Fix total_sales_kg and total_sales_amount by summing both
    total_sales_kg = total_cash_kg + total_credit_kg
    total_sales_amount = total_cash_amount + total_credit_amount

    # Pass everything to the template
    context = {
        'cash_sales': cash_sales,
        'credit_sales': credit_sales,
        'total_cash_kg': total_cash_kg,
        'total_cash_amount': total_cash_amount,
        'total_credit_kg': total_credit_kg,
        'total_credit_amount': total_credit_amount,
        'total_sales_kg': total_sales_kg,  # Correctly calculated total
        'total_sales_amount': total_sales_amount,  # Correctly calculated total
        'today': today,
    }
    return render(request, 'matugga_daily_sales_report.html', context)
from django.db.models import Sum
from django.utils import timezone
from django.shortcuts import render
from .models import Sale

def maganjo_daily_sales_report(request):
    today = timezone.now().date()

    # Separate cash and credit sales for Maganjo
    cash_sales = Sale.objects.filter(branch_name='Maganjo', date=today, payment_type='cash')
    credit_sales = Sale.objects.filter(branch_name='Maganjo', date=today, payment_type='credit')

    # Debugging: Check if sales exist
    if not credit_sales.exists():
        print("No credit sales found!")

    # Aggregate totals for cash and credit sales
    total_cash_kg = cash_sales.aggregate(total=Sum('tonnage_kg'))['total'] or 0
    total_cash_amount = cash_sales.aggregate(total=Sum('amount_paid'))['total'] or 0
    total_credit_kg = credit_sales.aggregate(total=Sum('tonnage_kg'))['total'] or 0
    total_credit_amount = credit_sales.aggregate(total=Sum('amount_due'))['total'] or 0

    # Compute total sales
    total_sales_kg = total_cash_kg + total_credit_kg
    total_sales_amount = total_cash_amount + total_credit_amount

    # Pass the updated data to the template
    context = {
        'cash_sales': cash_sales,
        'credit_sales': credit_sales,
        'total_cash_kg': total_cash_kg,
        'total_cash_amount': total_cash_amount,
        'total_credit_kg': total_credit_kg,  # Ensure credit kg is passed
        'total_credit_amount': total_credit_amount,
        'total_sales_kg': total_sales_kg,
        'total_sales_amount': total_sales_amount,
        'today': today,
    }
    return render(request, 'maganjo_daily_sales_report.html', context) 

    from django.core.mail import send_mail
from django.http import HttpResponse

def send_test_email(request):
    subject = 'Test Email'
    message = 'This is a test email sent from Django.'
    from_email = 'michealotodi81@gmail.com'  # Your Gmail address
    recipient_list = ['recipient_email@example.com']  # Replace with an actual email

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    return HttpResponse('Test email sent successfully!')

