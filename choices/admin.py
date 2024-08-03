from django.contrib import admin
from .models import *
from nested_admin import NestedTabularInline, NestedModelAdmin
from django.urls import path
from django.shortcuts import redirect
from django.template.response import TemplateResponse
import pandas as pd
from django import forms

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


class AdminDataAdmin(admin.ModelAdmin):
    change_list_template = "admin/choice_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-spreadsheet/', self.import_spreadsheet),
        ]
        return my_urls + urls

    def import_spreadsheet(self, request):
        if request.method == "POST":
            excel_file = request.FILES["excel_file"]

            # Read the Excel file
            df = pd.read_excel(excel_file)

            # Get all existing codes for each model
            existing_codes = {
                'Level 5': set(AdminLevel5.objects.values_list('code', flat=True)),
                'Level 6': set(AdminLevel6.objects.values_list('code', flat=True)),
                'Level 8': set(AdminLevel8.objects.values_list('code', flat=True)),
            }

            updated_codes = set()

            for _, row in df.iterrows():
                nfq_level = row['NFQ Level']

                # Determine which model to use based on NFQ Level
                if 'Level 5' in nfq_level:
                    model = AdminLevel5
                elif 'Level 6' in nfq_level:
                    model = AdminLevel6
                elif 'Level 8' in nfq_level:
                    model = AdminLevel8
                else:
                    continue  # Skip if not a recognized level

                code = row.get('Course Code', '')
                updated_codes.add(code)

                # Update or create the instance
                instance, created = model.objects.update_or_create(
                    code=code,
                    defaults={
                        'title': row.get('Title', ''),
                        'college': row.get('College', ''),
                        'url': row.get('nid', ''),
                        'is_expired': False  # Set to False as it's in the new sheet
                    }
                )

                # Add point field for Level6 and Level8
                if model in [AdminLevel6, AdminLevel8]:
                    instance.point = row.get('Points', '')
                    instance.save()

            # Mark entries as expired if they're not in the new sheet
            for level, codes in existing_codes.items():
                expired_codes = codes - updated_codes
                if level == 'Level 5':
                    AdminLevel5.objects.filter(code__in=expired_codes).update(is_expired=True)
                elif level == 'Level 6':
                    AdminLevel6.objects.filter(code__in=expired_codes).update(is_expired=True)
                elif level == 'Level 8':
                    AdminLevel8.objects.filter(code__in=expired_codes).update(is_expired=True)

            self.message_user(request, "Spreadsheet imported successfully")
            return redirect("..")

        form = ExcelImportForm()
        payload = {"form": form}
        return TemplateResponse(request, "admin/excel_form.html", payload)


admin.site.register(AdminLevel5, AdminDataAdmin)
admin.site.register(AdminLevel6, AdminDataAdmin)
admin.site.register(AdminLevel8, AdminDataAdmin)

# Register your other models
admin.site.register(Choice)
admin.site.register(Level5)
admin.site.register(Level6)
admin.site.register(Level8)
admin.site.register(Apprentice)
admin.site.register(Other)