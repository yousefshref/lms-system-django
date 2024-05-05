from django.contrib import admin
from . import models


admin.site.register(models.CustomUser)
admin.site.register(models.Level)
admin.site.register(models.Subject)
admin.site.register(models.WebSite)
admin.site.register(models.School)
admin.site.register(models.Teacher)
admin.site.register(models.Student)
admin.site.register(models.Post)
admin.site.register(models.Product)
admin.site.register(models.Cart)
admin.site.register(models.Order)
