from django.shortcuts import render

from booksale_app.models import Customer

def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'admin_temp/customer/customer_list.html', {"customers": customers})