from django.shortcuts import render, redirect, get_object_or_404
from booksale_app.models import Supplier
from booksale_app.forms import SupplierForm
from django.core.paginator import Paginator
from django.contrib import messages


# Danh sách nhà cung cấp
def supplier_list(request):
    suppliers = Supplier.objects.all().order_by('-id')
    paginator = Paginator(suppliers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'employee/inventory/supplier_list.html', {
        'suppliers': page_obj,
        'page': 'supplier_list'
    })

# Thêm nhà cung cấp
def supplier_add(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Thêm nhà cung cấp thành công!")
            return redirect('supplier_list')
    else:
        form = SupplierForm()
    return render(request, 'employee/inventory/supplier_form.html', {'form': form, 'title': 'Thêm nhà cung cấp'})

# Chỉnh sửa nhà cung cấp
def supplier_edit(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'employee/inventory/supplier_form.html', {'form': form, 'title': 'Chỉnh sửa nhà cung cấp'})

# Xóa nhà cung cấp
def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    supplier.delete()
    return redirect('supplier_list')
