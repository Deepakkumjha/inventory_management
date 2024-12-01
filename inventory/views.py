from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product,BorrowedProduct
from .forms import ProductForm,BorrowedProductForm,UserCreationForm
from django.contrib.auth.decorators import login_required,user_passes_test
# Create your views here.

# def product_list(request):
#     return render(request,'product_list.html')

def register(request):
    if request.method=="POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form=UserCreationForm()
    return render(request,'register.html',{'form':form})

def is_admin(user):
    print(user)
    return user.is_staff

def is_worker(user):
    print(user)
    return user.username=="deepak"

class CustomLogin(LoginView):
    def get_success_url(self) -> str:
        if self.request.user.is_staff:
            return reverse('admin')
        else:
            return reverse('worker')
        
@user_passes_test(is_admin)
@login_required
def admin(request):
    all_products=Product.objects.all()
    low_products=Product.objects.filter(low_quantity_flag=True)
    all_user=User.objects.all()
    
    return render(request,'admin.html',{'all_products':all_products,'low_products':low_products,'all_user':all_user})

@user_passes_test(is_worker)
@login_required
def worker(request):
    data=BorrowedProduct.objects.all()
    print(data)
    return render(request,'worker.html',{'data':data})


@user_passes_test(is_admin)
@login_required
def add(request):
  
    if request.method=="POST":
        form=ProductForm(request.POST)    
        if form.is_valid():
            product=form.save(commit=False)
            if product.total_quantity<10:
                product.low_quantity_flag=True
            else:
                product.low_quantity_flag=False
            product.save()
        return redirect('login')
    else:
        form=ProductForm()
    return render(request,'add_product.html',{'form':form})

@user_passes_test(is_admin)
@login_required
def edit(request,pk):
    product=get_object_or_404(Product,pk=pk)
    if request.method=="POST":
        form=ProductForm(request.POST,instance=product)
        if form.is_valid():
            form.save()
        return redirect('admin')
    else:
        form=ProductForm(instance=product)
    return render(request,'edit.html',{'form':form})

@user_passes_test(is_admin)
@login_required
def delete(request,pk):
    product=get_object_or_404(Product,pk=pk)
    if request.method=="POST":
        product.delete()
        return redirect('admin')
    return render(request,'delete.html',{'product':product})

@user_passes_test(is_admin)
@login_required
def assign_product(request):
    if request.method=="POST":
        print(request.POST)
        product_id=request.POST.get('product')
        print(product_id)
        quantity=int(request.POST.get('quantity'))
        print(quantity)
        product=Product.objects.filter(id=product_id).first()
        print(product.total_quantity)
        print(product)
        if product.total_quantity>=quantity:
            product.total_quantity=product.total_quantity-quantity
            product.save()
            form=BorrowedProductForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('admin')
    else:
        form=BorrowedProductForm()

    return render(request,'assign_product.html',{'form':form})

def see_details(request,id):
    products=BorrowedProduct.objects.filter(worker__id=id)
    return render(request,'see_details.html',{"products":products})


def return_product(request,id):
    if request.method=="POST":
        borrow_product=BorrowedProduct.objects.filter(id=id).first()
        product=borrow_product.product
        product.total_quantity=product.total_quantity+borrow_product.quantity
        product.save()
        borrow_product.delete()
        return redirect('worker')
    return render(request,'return.html')