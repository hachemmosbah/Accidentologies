
from django.contrib import admin
from .models import *



class FormDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'year', 'departement', 'age1', 'age2', 'unhurt', 'dead', 'hospitalized', 'hurt_light', 'men', 'women')
admin.site.register(DataForm, FormDataAdmin)

class FormDataPredAdmin(admin.ModelAdmin):
    list_display = ('id', 'year', 'departement', 'age', 'gender', 'location', 'intersection', 'light')
admin.site.register(DataPred, FormDataPredAdmin)