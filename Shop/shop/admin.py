from models import *
from django.contrib import admin
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'price_in_dollars',)
    list_filter = ('manufacturer',)
    search_fields = ('name',)
    
class CatalogAdmin(admin.ModelAdmin):
    list_display = ('name', 'publisher', 'pub_date',)
    list_filter = ('publisher','pub_date')
    search_fields = ('name',)
    
class CatalogCategoryAdmin(admin.ModelAdmin):
    list_display = ('catalog', 'name',)
    list_filter = ('name',)
    search_fields = ('name',)

class ProductDetailAdmin(admin.ModelAdmin):
    list_display = ('product', 'attribute','value')
    
    

    
admin.site.register(Catalog, CatalogAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(CatalogCategory, CatalogCategoryAdmin)
admin.site.register(ProductDetail, ProductDetailAdmin)
admin.site.register(ProductAttribute)
admin.site.register(Order)
admin.site.register(ProductInOrder)
admin.site.register(StatusCode)
admin.site.register(AmazonTransaction)
admin.site.register(Rating)
admin.site.register(TokenReference)
admin.site.register(Customer)
admin.site.register(CustomerAddress)
