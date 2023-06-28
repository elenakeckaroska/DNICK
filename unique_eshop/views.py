from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from datetime import datetime

# Create your views here.
from djangoProject.forms import ModelNameForm, AccessoryForm
from unique_eshop.models import *

# views.py

from django.shortcuts import render
from django.http import HttpResponse
from djangoProject.forms import CreditCardForm

def process_payment(request):
    if request.method == 'POST':
        form = CreditCardForm(request.POST)
        last_sale = Sale.objects.filter(shoppingCart__user=request.user).last()

        history_sale = Payment()
        history_sale.accessory = last_sale.accessory
        history_sale.numOfPieces = last_sale.numOfPieces
        history_sale.shoppingCart = last_sale.shoppingCart
        history_sale.successfully_paid = True
        history_sale.save()

        last_sale.accessory = None
        last_sale.totalPrice = 0
        last_sale.numOfPieces = 0
        last_sale.save()
        return redirect(sale)
    else:
        form = CreditCardForm()

    return render(request, 'payment.html', {'form': form})

def register(request):
    form = ModelNameForm(request.POST)

    if form.is_valid():
        user = form.save()
        login(request, user)
        qs = Accessory.objects.all()
        return render(request, 'home.html', {'accessories': qs})

    else:
        form = ModelNameForm()
        args = {'form': form}
    return render(request, 'register.html', args)


def search_products(request):
    query = request.POST.get('query').upper()
    accessories = Accessory.objects.filter(
        name__contains=query).all()
    return render(request, 'home.html', {'accessories': accessories})


# def logout_view(request):
#     logout(request)
#     qs = Accessory.objects.all()
#     return render(request, 'home.html', {'accessories': qs})


def home(request):
    if request.method == 'POST':
        if request.POST.get('selectCategory') == 'Изберете категорија' and request.POST.get(
                'min_price') == 0 and request.POST.get('max_price') == 1000:
            accessories = Accessory.objects.all()
        elif request.POST.get('selectCategory') == 'Изберете категорија' and (
                request.POST.get('min_price') != 0 or request.POST.get('max_price') != 1000):
            min_price = request.POST.get('min_price')
            max_price = request.POST.get('max_price')
            accessories = Accessory.objects.filter(price__gte=min_price, price__lte=max_price)
        else:
            min_price = request.POST.get('min_price')
            max_price = request.POST.get('max_price')

            accessories = Accessory.objects.filter(price__gte=min_price, price__lte=max_price,
                                                   category__exact=request.POST.get('selectCategory'))
    else:
        if request.GET.get('accessories') is not None:
            accessories = request.GET.gte('accessories').all()
        else:
            accessories = Accessory.objects.all()

    return render(request, 'home.html', {'accessories': accessories})


@login_required(login_url='login')
def sale(request):
    if request.method == "POST":
        sale_new = Sale()
        sale_new.shoppingCart = ShoppingCart.objects.filter(user=request.user).last()

        accessory_name = request.POST.get('name')
        accessory = Accessory.objects.filter(name__exact=accessory_name).last()
        sale_new.accessory = accessory
        accessory.quantity = accessory.quantity - 1
        accessory_price = accessory.price
        total = 0
        if Sale.objects.filter(shoppingCart__user=request.user) is not None:
            old_sale = Sale.objects.filter(shoppingCart__user=request.user).last()
            total_price = old_sale.totalPrice or 0
            total = accessory_price + total_price

        sale_new.totalPrice = total
        sale_new.numOfPieces = 1
        sale_new.save()
        qs = Sale.objects.filter(shoppingCart__user=request.user)
        accessory.save()
        context = {"accessories": qs, "total": total, "user": request.user}
        return render(request, "sale.html", context)

    total_price = 0
    if Sale.objects.filter(shoppingCart__user=request.user) is not None:
        old_sale = Sale.objects.filter(shoppingCart__user=request.user).last()
        total_price = old_sale.totalPrice
    qs = Sale.objects.filter(shoppingCart__user=request.user)
    if not qs.exists():
        total_price = 0
    context = {"accessories": qs, "total": total_price, "user": request.user}
    return render(request, "sale.html", context)


@login_required(login_url='login')
def deleteSale(request):
    if request.method == "POST":
        # sale_new = Sale()
        # sale_new.shoppingCart = ShoppingCart.objects.filter(user=request.user).last()

        accessory_name = request.POST.get('name')
        accessory = Accessory.objects.filter(name__exact=accessory_name).last()
        # sale_new.accessory = accessory

        accessory_price = accessory.price
        total = 0
        if Sale.objects.filter(shoppingCart__user=request.user) is not None:
            old_sale = Sale.objects.filter(shoppingCart__user=request.user).last()
            total_price = old_sale.totalPrice
            total = total_price - old_sale.numOfPieces * accessory_price
            old_sale.delete()

            accessory.quantity = accessory.quantity + old_sale.numOfPieces

            last_sale = Sale.objects.filter(shoppingCart__user=request.user).last()
            last_sale.totalPrice = total
            last_sale.save()
            accessory.save()

        qs = Sale.objects.filter(shoppingCart__user=request.user)
        context = {"accessories": qs, "total": total, "user": request.user}
        return render(request, "sale.html", context)

    total_price = 0
    if Sale.objects.filter(shoppingCart__user=request.user) is not None:
        old_sale = Sale.objects.filter(shoppingCart__user=request.user).last()
        total_price = old_sale.totalPrice
    qs = Sale.objects.filter(shoppingCart__user=request.user)
    if not qs.exists():
        total_price = 0
    context = {"accessories": qs, "total": total_price, "user": request.user}
    return render(request, "sale.html", context)


@login_required(login_url='login')
def quantityDecrease(request):
    if request.method == "POST":
        accessory_name = request.POST.get('name')
        accessory_req = Accessory.objects.filter(name__exact=accessory_name).last()

        sale_refactor = Sale.objects.filter(shoppingCart__user=request.user).last()


        sale_refactor.accessory.quantity += 1

        accessory_price = accessory_req.price
        newNumOfPieces = sale_refactor.numOfPieces - 1

        total_price = sale_refactor.totalPrice or 0
        total = total_price - accessory_price

        sale_refactor.numOfPieces = newNumOfPieces
        sale_refactor.totalPrice = total
        sale_refactor.save()
        sale_refactor.accessory.save()
        qs = Sale.objects.filter(shoppingCart__user=request.user)

        context = {"accessories": qs, "total": total, "user": request.user}
        return render(request, "sale.html", context)

    total_price = 0
    if Sale.objects.filter(shoppingCart__user=request.user) is not None:
        old_sale = Sale.objects.filter(shoppingCart__user=request.user).last()
        total_price = old_sale.totalPrice
    qs = Sale.objects.filter(shoppingCart__user=request.user)
    if not qs.exists():
        total_price = 0
    context = {"accessories": qs, "total": total_price, "user": request.user}
    return render(request, "sale.html", context)


@login_required(login_url='login')
def quantity(request):
    if request.method == "POST":
        accessory_name = request.POST.get('name')
        accessory_req = Accessory.objects.filter(name__exact=accessory_name).last()

        sale_refactor = Sale.objects.filter(shoppingCart__user=request.user).last()

        sale_refactor.accessory.quantity -= 1

        accessory_price = accessory_req.price
        newNumOfPieces = sale_refactor.numOfPieces + 1

        total_price = sale_refactor.totalPrice or 0
        total = total_price + accessory_price

        sale_refactor.numOfPieces = newNumOfPieces
        sale_refactor.totalPrice = total
        sale_refactor.save()
        sale_refactor.accessory.save()

        qs = Sale.objects.filter(shoppingCart__user=request.user)
        context = {"accessories": qs, "total": total, "user": request.user}
        return render(request, "sale.html", context)

    total_price = 0
    if Sale.objects.filter(shoppingCart__user=request.user) is not None:
        old_sale = Sale.objects.filter(shoppingCart__user=request.user).last()
        total_price = old_sale.totalPrice
    qs = Sale.objects.filter(shoppingCart__user=request.user)
    if not qs.exists():
        total_price = 0
    context = {"accessories": qs, "total": total_price, "user": request.user}
    return render(request, "sale.html", context)


def addAccessory(request):
    if request.method == "POST":
        form_data = AccessoryForm(data=request.POST, files=request.FILES)
        if form_data.is_valid():
            accessory = form_data.save(commit=False)
            accessory.datetime = datetime.now()
            accessory.save()
            qs = Accessory.objects.order_by('-datetime').all()
            context = {"accessories": qs, "form": AccessoryForm}
            return render(request, "home.html", context)

    context = {"form": AccessoryForm}
    return render(request, "addAccessory.html", context=context)


def details(request):
    if request.method == "POST":
        accessory_name = request.POST.get('name')
        accessory = Accessory.objects.filter(name__exact=accessory_name).last()
        context = {"a": accessory}
        return render(request, "details.html", context)
    return redirect('home')


def recentAccessories(request):
    qs = Accessory.objects.order_by('-datetime').all()
    context = {"accessories": qs, "form": AccessoryForm}
    return render(request, "recentAccessories.html", context)
