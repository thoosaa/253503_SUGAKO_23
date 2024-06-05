from django.contrib import admin
from .models import PromoCode, ToyModal, ToyType, Toy, Sale, User, Staff, Customer, CustomerProfile, StaffProfile, News, FAQ, About, Job

#admin.site.register(PromoCode)
admin.site.register(ToyModal)
admin.site.register(Staff)
admin.site.register(Customer)
admin.site.register(About)

class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')

class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('staff', 'phonenumber', 'email', 'photo', 'profession')

class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('customer','phonenumber', 'city', 'address')

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'type', 'password', 'is_staff', 'is_customer')

class SaleAdmin(admin.ModelAdmin):
    list_display = ('toy', 'quantity', 'order_date', 'completion_date', 'price', 'promo_code', 'customer')
    fields = ['customer', ('toy','quantity'), 'completion_date', 'promo_code']

class ToyAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'price', 'is_manufactured')
    list_filter = ('is_manufactured', 'type', 'price')

class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'expiration')
    list_filter = ('expiration', )

class ToyTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_promocode')

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')

class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'created_at')

admin.site.register(User, UserAdmin)
admin.site.register(CustomerProfile, CustomerProfileAdmin)
admin.site.register(StaffProfile, StaffProfileAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(Toy, ToyAdmin)
admin.site.register(PromoCode, PromoCodeAdmin)
admin.site.register(ToyType, ToyTypeAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(Job, JobAdmin)
# Register your models here.
