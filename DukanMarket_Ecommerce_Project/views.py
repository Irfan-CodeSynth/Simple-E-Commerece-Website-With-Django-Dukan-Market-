
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect, render
from app.models import Slider , banner_area , Main_Category , Product , Category , Color , Brand , Coupon_Code ,banner_area_2
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Max, Min , Sum
from cart.cart import Cart
import random

import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views import View




def BASE(request):
    return render(request, 'base.html')

def About(request):
    return render(request, 'Main/about.html')

def Contact(request):
    return render(request, 'Main/contact.html')



def HOME(request):
    sliders = Slider.objects.all().order_by('-id')[0:3]
    banners = banner_area.objects.all().order_by('-id')[0:3]
    banners_2 = banner_area_2.objects.all().order_by('-id')[0:3]
    
    main_category = Main_Category.objects.all().order_by('-id')
    product = Product.objects.filter(section__name="Top Deals Of The Day")
    product_2 = Product.objects.filter(section__name="Top Featured Products")

    # Define the IDs of the top selling products for 1
    top_selling_ids_1 = [1]  
    top_selling_products_1 = list(Product.objects.filter(id__in=top_selling_ids_1))
    top_selling_products_1 = random.sample(top_selling_products_1, 1)


    # Define the IDs of the top selling products for 1
    top_selling_ids_2 = [14,8]  
    top_selling_products_2 = list(Product.objects.filter(id__in=top_selling_ids_2))
    top_selling_products_2 = random.sample(top_selling_products_2, 2)

    # Define the IDs of the top selling products for 1
    top_selling_ids_3 = [7,11]  
    top_selling_products_3 = list(Product.objects.filter(id__in=top_selling_ids_3))
    top_selling_products_3 = random.sample(top_selling_products_3, 2)

    context = {
        'sliders': sliders,
        'banners': banners,
        'main_category': main_category,
        'product': product,
        'product_2': product_2,
        'banners_2': banners_2,
        'top_selling_products_1': top_selling_products_1,
        'top_selling_products_2': top_selling_products_2,
        'top_selling_products_3': top_selling_products_3,
    }
    return render(request, 'Main/home.html', context)



def Product_details(request, slug):
    product = Product.objects.filter(slug=slug)
    
    if product.exists():
        product = Product.objects.get(slug=slug)
    else:
        return redirect('404')
    
    context = {
        'product': product,
    }
    
    return render(request, 'product/product-detail.html', context)




def Error404(request, exception=None):
    return render(request, 'Errors-Pages/404.html')



def My_Account(request):
    return render(request,'account/my-account.html')



def Register(request):
    
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            messages.error(request,'Username Already Exists!')
            return redirect('login')
        
        if User.objects.filter(email=email).exists():
            messages.error(request,'Email Is Already Exists!')
            return redirect('login')
        
        user =  User(
            username =username,
            email = email,
            
        )
        user.set_password(password)
        user.save()
        return redirect('login')
        
  



def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to a success page.
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')  
    
    return render(request,'registeration/login.html')




@login_required(login_url='/accounts/login/')
def Profile(request):
    
    return render(request,'profile/profile.html')




@login_required(login_url='/accounts/login/')
def profile_update(request):
    user = request.user

    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email

        if password:
            user.set_password(password)
            update_session_auth_hash(request, user)  

        user.save()
        messages.success(request, 'Your profile has been updated successfully.')
        
        return redirect('profile')


def custom_logout(request):
    logout(request)
    return redirect('/')


def filter_data(request):
    categories = request.GET.getlist('category[]')
    print(categories)
    brands = request.GET.getlist('brand[]')
    product_num = request.GET.getlist('product_num[]')
    brand = request.GET.getlist('brand[]')
    print(brand)
    print(product_num)
    
    allProducts = Product.objects.all().order_by('-id').distinct()
    
    if len(categories) > 0:
        allProducts = allProducts.filter(Categories__id__in=categories).distinct()
        
    if len(product_num) > 0:
         allProducts = allProducts.all().order_by('-id')[0:1]
         
         
    if len(brands) > 0:
        allProducts = allProducts.filter(Brand__id__in=brands).distinct()
    
    t = render_to_string('ajax/product.html', {'product':allProducts})
        

    return JsonResponse({'data': t})



def product_page(request):
    categories = Category.objects.all()
    color = Color.objects.all()
    brand = Brand.objects.all()
    min_price = Product.objects.aggregate(Min('price'))['price__min']
    max_price = Product.objects.aggregate(Max('price'))['price__max']
    
    FilterPrice = request.GET.get('FilterPrice')
    
    if FilterPrice:
        try:
            Int_FilterPrice = int(FilterPrice)
            products = Product.objects.filter(price__lte=Int_FilterPrice)
        except ValueError:
            # Handle the case where FilterPrice is not a valid integer
            products = Product.objects.all()
    else:
        products = Product.objects.all()
        
    ColorID = request.GET.get('colorID')
    if ColorID:
        products = products.filter(color_id=ColorID)  # Filter by color
    
    context = {
        'category': categories,
        'product': products,  #
        'min_price': min_price,
        'max_price': max_price,
        'color': color,
        'brand': brand,
    }
    
    return render(request, 'product/products-page.html', context)




# CART Views 

@login_required(login_url="/accounts/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")




@login_required(login_url="/accounts/login/")
def cart_detail(request):
    # Retrieve the cart from the session, defaulting to an empty dictionary if not found
    cart = request.session.get('cart', {})

   
    packing_cost = sum(item.get('packing_cost', 0) for item in cart.values())
    tax = sum(item.get('tax', 0) for item in cart.values())

    
    coupon = None
    valid_coupon = None
    invalid_coupon = None

   
    coupon_code = request.GET.get('coupon_code', None)
    if coupon_code:
        try:
            coupon = Coupon_Code.objects.get(code=coupon_code)
            valid_coupon = "Coupon is applicable on the current order!"
        except Coupon_Code.DoesNotExist:
            invalid_coupon = "Invalid coupon code!"

   
    context = {
        'packing_cost': packing_cost,
        'tax': tax,
        'coupon': coupon,
        'valid_coupon': valid_coupon,
        'invalid_coupon': invalid_coupon,
    }

    return render(request, 'cart/cart.html', context)




# views.py


def cart(request):
    cart = request.session.get('cart', {})
    cart_total_amount = sum(item['price'] * item['quantity'] for item in cart.values())
    packing_cost = 10  # Example fixed packing cost
    tax = 5  # Example fixed tax

    # Store packing cost and tax in session
    request.session['packing_cost'] = packing_cost
    request.session['tax'] = tax

    # Check for delivery charge
    delivery_charge = 0 if cart_total_amount > 500 else 10  # Free delivery if cart_total_amount > 500

    # Store other necessary variables in session if needed
    request.session['delivery_charge'] = delivery_charge

    context = {
        'cart': cart,
        'cart_total_amount': cart_total_amount,
        'packing_cost': packing_cost,
        'tax': tax,
        'delivery_charge': delivery_charge,
        # Add more context variables if needed
    }

    return render(request, 'cart/cart.html', context)






def Checkout(request):
    # Retrieve necessary data from the session
    cart = request.session.get('cart', {})
    cart_total_amount = sum(item['price'] * item['quantity'] for item in cart.values())
    packing_cost = request.session.get('packing_cost', 10)  # Default value in case session data is missing
    tax = request.session.get('tax', 5)  # Default value in case session data is missing
    delivery_charge = request.session.get('delivery_charge', 10)  # Retrieve delivery charge from session

    # Check if a coupon was applied
    valid_coupon = request.session.get('valid_coupon', False)
    coupon_discount = request.session.get('coupon_discount', 0)

    # Calculate the total bill considering discounts, tax, packing cost, etc.
    total_bill = cart_total_amount + packing_cost + tax + delivery_charge
    if valid_coupon:
        total_bill *= (1 - coupon_discount / 100)

    context = {
        'cart': cart,
        'cart_total_amount': cart_total_amount,
        'packing_cost': packing_cost,
        'tax': tax,
        'delivery_charge': delivery_charge,
        'total_bill': total_bill,
        'valid_coupon': valid_coupon,
        'coupon_discount': coupon_discount,
    }

    return render(request, 'checkout/checkout.html', context)


def apply_coupon(request):
    # Logic to validate and apply the coupon
    if coupon_is_valid:
        request.session['valid_coupon'] = True
        request.session['coupon_discount'] = coupon_discount_percentage
    else:
        request.session['valid_coupon'] = False
        request.session['coupon_discount'] = 0

    # Redirect back to the cart page or handle it via AJAX
    return redirect('cart')










