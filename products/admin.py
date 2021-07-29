from django.contrib import admin
from products.models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'added_by', 'image', 'quantity'
    )
    search_fields = ('name', 'added_by')


admin.site.register(Product, ProductAdmin)
