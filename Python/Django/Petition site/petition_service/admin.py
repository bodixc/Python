from django.contrib import admin

from .models import Petition, Category, Status, Signature

admin.site.register(Petition)
admin.site.register(Category)
admin.site.register(Status)
admin.site.register(Signature)

# Register your models here.
