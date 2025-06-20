from django.contrib import admin
from .models import MaritalStatus, Title, CaseType, EmploymentStatus, Gender, Nationality, Job, BeneficiaryType, CourtRoom, CourtType, EmployerType, Language, Party

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(CaseType)
class CaseTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
@admin.register(MaritalStatus)
class MaritalStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(BeneficiaryType)
class BeneficiaryTypeCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(CourtRoom)
class CourtRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'court_type')
    search_fields = ('name',)

@admin.register(CourtType)
class CourtTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(EmploymentStatus)
class EmploymentStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Nationality)
class NationalitiesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(EmployerType)
class EmployerTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)