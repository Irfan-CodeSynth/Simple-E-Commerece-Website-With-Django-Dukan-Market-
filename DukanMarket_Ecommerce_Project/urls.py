from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', views.BASE, name='base'),
    path('', views.HOME, name='home'),
    path('about/', views.About, name='about'),
    path('contact/', views.Contact, name='contact'),
    path('product/<slug:slug>/', views.Product_details, name='product_detail'),
    path('products-page/', views.product_page, name='products-page'),
    path('filter-data/', views.filter_data, name='filter_data'),
    path('404/', views.Error404, name='404'),
    path('account/register/', views.Register, name='handle-register'),
    path('accounts/login/', views.Login, name='handle-login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('account/profile', views.Profile, name='profile'),
    path('account/profile/update', views.profile_update, name='profile-update'),
    path('logout/', views.custom_logout, name='logout'),
    
    
    
    # cart urls 
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),
    path('checkout/checkout/',views.Checkout,name='checkout'),
    
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)