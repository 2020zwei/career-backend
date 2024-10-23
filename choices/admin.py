from django.contrib import admin
from .models import *
from nested_admin import NestedTabularInline, NestedModelAdmin
from django.urls import path
from django.shortcuts import redirect, HttpResponse
from django.template.response import TemplateResponse
import pandas as pd
from django import forms
from users.models import Counselor
from django.contrib import messages

class ExcelImportForm(forms.Form):
    excel_file = forms.FileField()

class Level6Inline(NestedTabularInline):
    model = Level6

class Level8Inline(NestedTabularInline):
    model = Level8

class Level5Inline(NestedTabularInline):
    model = Level5

class ApprenticeInline(NestedTabularInline):
    model = Apprentice

class OtherInline(NestedTabularInline):
    model = Other

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['user']
    search_fields = ("user__full_name",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_counselor:
            counselor = Counselor.objects.get(user=request.user)
            return qs.filter(user__school=counselor.school)
        return qs

class ApprenticeAdmin(admin.ModelAdmin):
    list_display = ['choice']
    search_fields = ("choice__user__full_name",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_counselor:
            counselor = Counselor.objects.get(user=request.user)
            return qs.filter(choice__user__school=counselor.school)
        return qs


class Level5Admin(admin.ModelAdmin):
    list_display = ['choice']
    search_fields = ("choice__user__full_name",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_counselor:
            counselor = Counselor.objects.get(user=request.user)
            return qs.filter(choice__user__school=counselor.school)
        return qs


class OtherAdmin(admin.ModelAdmin):
    list_display = ['choice']
    search_fields = ("choice__user__full_name",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_counselor:
            counselor = Counselor.objects.get(user=request.user)
            return qs.filter(choice__user__school=counselor.school)
        return qs


class Level6Admin(admin.ModelAdmin):
    list_display = ['choice']
    search_fields = ("choice__user__full_name",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_counselor:
            counselor = Counselor.objects.get(user=request.user)
            return qs.filter(choice__user__school=counselor.school)
        return qs


class Level8Admin(admin.ModelAdmin):
    list_display = ['choice']
    search_fields = ("choice__user__full_name",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_counselor:
            counselor = Counselor.objects.get(user=request.user)
            return qs.filter(choice__user__school=counselor.school)
        return qs


class BaseAdminDataAdmin(admin.ModelAdmin):
    change_list_template = "admin/choice_changelist.html"
    level = None

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-spreadsheet/', self.import_spreadsheet),
        ]
        return my_urls + urls

    def import_spreadsheet(self, request):
        try:
            if request.method == "POST":
                excel_file = request.FILES["courses_file"]
                df = pd.read_excel(excel_file)
                model = self.level
                existing_codes = set(model.objects.values_list('code', flat=True))
                updated_codes = set()

                for index, row in df.iterrows():
                    code = row.get('Course Code', '')

                    if not code or pd.isna(code):
                        print(f"Skipping row {index} due to empty or NaN Course Code")
                        continue

                    code = row.get('Course Code', '').strip()
                    title = row.get('Title', '').strip() if not pd.isna(row.get('Title', '')) else None
                    college = row.get('College', '').strip() if not pd.isna(row.get('College', '')) else None
                    points = row.get('Points', '') if not pd.isna(row.get('Points', '')) else None

                    instance, created = model.objects.update_or_create(
                        code=code,
                        defaults={
                            'title': title,
                            'college': college,
                            'course_information': row.get('nid', '').strip() if not pd.isna(
                                row.get('nid', '')) else None,
                            'is_expired': False
                        }
                    )
                    instance.point = points
                    instance.save()

                expired_codes = existing_codes - updated_codes
                model.objects.filter(code__in=expired_codes).update(is_expired=True)

                self.message_user(request, "Spreadsheet imported successfully", level=messages.SUCCESS)
                duplicate_codes = df[df.duplicated(subset=['Course Code'], keep=False)]
                if not duplicate_codes.empty:
                    self.message_user(request, f"{len(duplicate_codes)} Duplicate Course Codes found!", level=messages.ERROR)
                    for index, row in duplicate_codes.iterrows():
                        print(f"Row {index}: {row['Course Code']} - {row['Title']}")
                return redirect("..")

            form = ExcelImportForm()
            payload = {"form": form}
            return TemplateResponse(request, "admin/excel_form.html", payload)

        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}", status=500)


class AdminLevel5DataAdmin(BaseAdminDataAdmin):
    level = AdminLevel5


class AdminLevel6DataAdmin(BaseAdminDataAdmin):
    level = AdminLevel6


class AdminLevel8DataAdmin(BaseAdminDataAdmin):
    level = AdminLevel8


class AdminApprenticeAdmin(admin.ModelAdmin):
    change_list_template = "admin/choice_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-spreadsheet/', self.import_spreadsheet),
        ]
        return my_urls + urls

    def import_spreadsheet(self, request):
        try:
            if request.method == "POST":
                excel_file = request.FILES["courses_file"]
                df = pd.read_excel(excel_file)
                existing_names = set(AdminApprentice.objects.values_list('name', flat=True))
                updated_names = set()

                for index, row in df.iterrows():
                    name = row.get('Apprenticeship', '').strip()

                    if not name or pd.isna(name):
                        print(f"Skipping row {index} due to empty or NaN Apprenticeship")
                        continue

                    updated_names.add(name)

                    instance, created = AdminApprentice.objects.update_or_create(
                        name=name,
                        defaults={
                            'level': row.get('NFQ Level', '').strip() if not pd.isna(row.get('NFQ Level', '')) else None,
                            'company': row.get('Industry Lead', '').strip() if not pd.isna(row.get('Industry Lead', '')) else None,
                            'is_expired': False
                        }
                    )

                expired_names = existing_names - updated_names
                AdminApprentice.objects.filter(name__in=expired_names).update(is_expired=True)

                self.message_user(request, "Spreadsheet imported successfully", level=messages.SUCCESS)
                duplicate_names = df[df.duplicated(subset=['Apprenticeship'], keep=False)]
                if not duplicate_names.empty:
                    self.message_user(request, f"{len(duplicate_names)} Duplicate Apprenticeship names found!", level=messages.ERROR)
                    for index, row in duplicate_names.iterrows():
                        print(f"Row {index}: {row['Apprenticeship']} - {row['NFQ Level']}")

                return redirect("..")

            form = ExcelImportForm()
            payload = {"form": form}
            return TemplateResponse(request, "admin/excel_form.html", payload)

        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}", status=500)


class AdminOtherAdmin(admin.ModelAdmin):
    change_list_template = "admin/choice_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-spreadsheet/', self.import_spreadsheet),
        ]
        return my_urls + urls

    def import_spreadsheet(self, request):
        try:
            if request.method == "POST":
                excel_file = request.FILES["courses_file"]
                df = pd.read_excel(excel_file, header=None)  # Read without headers

                # Delete all existing ideas
                AdminOther.objects.all().delete()

                new_ideas = []
                for index, row in df.iterrows():
                    # Strip whitespace and ensure no NaN values
                    idea = str(row.iloc[0]).strip()

                    if not idea or pd.isna(idea):
                        print(f"Skipping row {index} due to empty or NaN idea")
                        continue

                    # Collect new ideas to bulk create later
                    new_ideas.append(AdminOther(idea=idea))

                # Bulk create all new ideas
                AdminOther.objects.bulk_create(new_ideas)

                self.message_user(request, "Spreadsheet imported successfully", level=messages.SUCCESS)

                return redirect("..")

            form = ExcelImportForm()
            payload = {"form": form}
            return TemplateResponse(request, "admin/excel_form.html", payload)

        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}", status=500)


# Admin Models for storing data from sheets
admin.site.register(AdminLevel5, AdminLevel5DataAdmin)
admin.site.register(AdminLevel6, AdminLevel6DataAdmin)
admin.site.register(AdminLevel8, AdminLevel8DataAdmin)
admin.site.register(AdminApprentice, AdminApprenticeAdmin)
admin.site.register(AdminOther, AdminOtherAdmin)


# Register your other models
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Level5, Level5Admin)
admin.site.register(Level6, Level6Admin)
admin.site.register(Level8, Level8Admin)
admin.site.register(Apprentice, ApprenticeAdmin)
admin.site.register(Other, OtherAdmin)