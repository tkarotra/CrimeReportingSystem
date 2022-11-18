from django.contrib import admin
from .models import FIR, User, Wanted, Missing, Feedback
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class FirField(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['No_Of_People_Involved', 'Category', 'S_age', 'S_race', 'S_gen', 'V_age', 'V_race', 'V_gen', 'Address', 'City', 'State', 'Describe', 'Police_Department', 'Is_affected', 'Status']

class MissingField(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['FName', 'LName', 'Gender', 'Race', 'Hair', 'Eye', 'DOB', 'Birthmark', 'Height', 'Weight', 'Last_Date', 'Last_City', 'Last_State', 'Incident_Type', 'Status']

class WantedField(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['Name', 'Age', 'Gender', 'Race', 'No_Of_Victims', 'Male_Victims', 'Female_Victims', 'County', 'State', 'Region', 'MOKilling', 'is_juvenile', 'Status']


admin.site.register(User)
admin.site.register(Feedback)
# admin.site.register(FIR)
# admin.site.register(Missing)
# admin.site.register(Wanted)
admin.site.register(FIR, FirField)
admin.site.register(Missing, MissingField)
admin.site.register(Wanted, WantedField)