from django.shortcuts import render, redirect, get_object_or_404
from booksale_app.models import Supplier
from booksale_app.forms import SupplierForm
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from booksale_app.views.authen_view import group_required


# ============================
# DANH SÁCH NHÀ CUNG CẤP
# ============================
@login_required(login_url="/accounts/login/warehouse/")
@group_required("NVTK", login_url="/accounts/login/warehouse/")
def supplier_list(request):
    suppliers = Supplier.objects.all().order_by('-id')
    paginator = Paginator(suppliers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'employee/inventory/supplier_list.html', {
        'suppliers': page_obj,
        'page': 'supplier_list'
    })


# ============================
# THÊM NHÀ CUNG CẤP
# ============================
@login_required(login_url="/accounts/login/warehouse/")
@group_required("NVTK", login_url="/accounts/login/warehouse/")
def supplier_add(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Thêm nhà cung cấp thành công!")
            return redirect('supplier_list')
    else:
        form = SupplierForm()

    return render(request, 'employee/inventory/supplier_form.html', {
        'form': form,
        'title': 'Thêm nhà cung cấp'
    })


# ============================
# CHỈNH SỬA NHÀ CUNG CẤP
# ============================
@login_required(login_url="/accounts/login/warehouse/")
@group_required("NVTK", login_url="/accounts/login/warehouse/")
def supplier_edit(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)

    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, "✔️ Cập nhật thông tin nhà cung cấp thành công!")
            return redirect('supplier_list')
    else:
        form = SupplierForm(instance=supplier)

    return render(request, 'employee/inventory/supplier_form.html', {
        'form': form,
        'title': 'Chỉnh sửa nhà cung cấp'
    })


# ============================
# XÓA NHÀ CUNG CẤP
# ============================
@login_required(login_url="/accounts/login/warehouse/")
@group_required("NVTK", login_url="/accounts/login/warehouse/")
def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    supplier.delete()
    messages.success(request, "🗑️ Đã xóa nhà cung cấp thành công!")
    return redirect('supplier_list')