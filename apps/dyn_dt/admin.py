from django.contrib import admin
from .models import PageItems, HideShowFilter, ModelFilter

# Register your models here.

admin.site.register(PageItems)
admin.site.register(HideShowFilter)
admin.site.register(ModelFilter)
