from django.contrib import admin
from . import models


admin.site.register(models.Level)
admin.site.register(models.Student)
admin.site.register(models.StudentImage)

admin.site.register(models.Form)
admin.site.register(models.FormField)
admin.site.register(models.FormAnswerParent)
admin.site.register(models.FormAnswer)
