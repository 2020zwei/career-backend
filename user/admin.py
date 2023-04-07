from django.contrib import admin
from .models  import Student, School
class StudentAdminDisplay(admin.ModelAdmin):
    
    def firstname_and_lastname(obj,obj1):
     return "%s %s" % (obj1.first_name, obj1.last_name)
    
   
    list_display=['__str__','firstname_and_lastname','school','dob','profile_image']
    

    



admin.site.register(Student,StudentAdminDisplay)
admin.site.register(School)

