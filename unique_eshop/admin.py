from django.contrib import admin
from .models import *

class AccessoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', ]

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_view_permission(self, request, obj=None):
        return True


class PaymentAdmin(admin.ModelAdmin):
    exclude = []

    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

    # def get_queryset(self, request):
    #     queryset = super().get_queryset(request)
    #     print("QUERYYYYYYYYYYYYYYYYYYYYYYYYY", queryset)
    #     return queryset

    # def has_view_permission(self, request, obj=None):
    #     return True
    # def has_view_permission(self, request, obj=None):
    #     if obj and request.user == obj.shoppingCart.user:
    #         print('****************', request.user == obj.shoppingCart.user)
    #         return True
    #     return False

    def save_model(self, request, obj, form, change):
        if obj:
            obj.shoppingCart = ShoppingCart.objects.filter(user=request.user).first()
            print(form)
            print(obj.accessory)
            obj.save()
            if obj.accessory is not None:
                accessory_price = obj.accessory.price
                sale = Sale.objects.filter(shoppingCart__user=request.user).first()
                total_price = sale.totalPrice or 0
                total = accessory_price + total_price
                sales = Sale.objects.filter(shoppingCart__user=request.user).all()
                sales.update(totalPrice=total)


admin.site.register(Accessory, AccessoryAdmin)
admin.site.register(Payment, PaymentAdmin)
