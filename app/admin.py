from django.contrib import admin
from .models import *
# Register your models here.


class Product_images(admin.TabularInline):
    model = Product_image
    


class Addtional_informations(admin.TabularInline):
    model = Aditional_Information
    
class Product_admin(admin.ModelAdmin):
    inlines = (Product_images,Addtional_informations)
    list_display = ('product_name','price','Categories','color','section')
    list_editable = ('Categories','section' , 'color')
    

admin.site.register(Slider)
admin.site.register(banner_area)
admin.site.register(banner_area_2)
admin.site.register(Main_Category)
admin.site.register(Category)
admin.site.register(Sub_category)
admin.site.register(Section)
admin.site.register(Featured_Products_Section)
admin.site.register(Product,Product_admin)
admin.site.register(Product_image)
admin.site.register(Aditional_Information)
admin.site.register(Color)
admin.site.register(Brand)
admin.site.register(Coupon_Code)


