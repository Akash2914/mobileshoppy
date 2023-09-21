from django.contrib import admin
from .models import *

class catagoryadmin(admin.ModelAdmin):
    list_display = ('name','image','description')
admin.site.register(Catagory,catagoryadmin)
admin.site.register(Product)
# Register your models here.
