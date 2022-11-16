from django.contrib import admin
from .models  import User
class UserAdminDisplay(admin.ModelAdmin):
    
    def firstname_and_lastname(obj,obj1):
     return "%s %s" % (obj1.first_name, obj1.last_name)
    
   
    list_display=['__str__','firstname_and_lastname','email','school','dob','profile_image']
    

    def get_exclude(self, request, obj=None):
     if obj:
        return ["password"]
     else:
        return []


    



admin.site.register(User,UserAdminDisplay)
