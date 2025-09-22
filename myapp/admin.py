from django.contrib import admin

from .models import *
# Register your models here.
admin.site.register(question)
admin.site.register(category)
#
# #Developer
admin.site.register(developer)
admin.site.register(domain)
#
# #HR
admin.site.register(hr)