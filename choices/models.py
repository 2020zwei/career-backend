from django.db import models
from users.models import Student

# Create your models here.

class Choice(models.Model):
    user=models.ForeignKey(Student, on_delete=models.CASCADE)
    level6= models.BooleanField(default=False)
    Level5= models.BooleanField(default=False)
    level8= models.BooleanField(default=False)
    other=models.BooleanField(default=False)
    apprentice= models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.full_name
    
    class Meta:
        app_label = 'choices'

    
class Level6(models.Model):
    choice=models.ForeignKey(Choice,related_name="lvl6", on_delete=models.CASCADE)
    code=models.CharField(max_length=50,null=True,blank=True)
    title=models.CharField(max_length=50,null=True,blank=True)
    point=models.CharField(max_length=50,null=True,blank=True)
    college=models.CharField(max_length=50,null=True,blank=True)
    order_number = models.PositiveIntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.choice.user.full_name
    
    class Meta:
        app_label = 'choices'

    def save(self, *args, **kwargs):
        if not self.id:
            # Calculate the next order number only for new records
            max_order = Level6.objects.aggregate(models.Max('order_number'))['order_number__max'] or 0
            self.order_number = max_order + 1
        super(Level6, self).save(*args, **kwargs)

class Level8(models.Model):
    choice=models.ForeignKey(Choice,related_name="lvl8", on_delete=models.CASCADE)
    code=models.CharField(max_length=50,null=True,blank=True)
    title=models.CharField(max_length=50,null=True,blank=True)
    point=models.CharField(max_length=50,null=True,blank=True)
    college=models.CharField(max_length=50,null=True,blank=True)
    order_number = models.PositiveIntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.choice.user.full_name
    
    class Meta:
        app_label = 'choices'

    def save(self, *args, **kwargs):
        if not self.id:
            # Calculate the next order number only for new records
            max_order = Level8.objects.aggregate(models.Max('order_number'))['order_number__max'] or 0
            self.order_number = max_order + 1
        super(Level8, self).save(*args, **kwargs)

class Apprentice(models.Model):
    choice=models.ForeignKey(Choice,related_name="app", on_delete=models.CASCADE)
    name=models.CharField(max_length=50,null=True,blank=True)
    level=models.CharField(max_length=50,null=True,blank=True)
    company=models.CharField(max_length=50,null=True,blank=True)
    order_number = models.PositiveIntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.choice.user.full_name
    
    class Meta:
        app_label = 'choices'

    def save(self, *args, **kwargs):
        if not self.id:
            # Calculate the next order number only for new records
            max_order = Apprentice.objects.aggregate(models.Max('order_number'))['order_number__max'] or 0
            self.order_number = max_order + 1
        super(Apprentice, self).save(*args, **kwargs)

class Level5(models.Model):
    choice=models.ForeignKey(Choice,related_name="lvl5", on_delete=models.CASCADE)
    code=models.CharField(max_length=50,null=True,blank=True)
    title=models.CharField(max_length=50,null=True,blank=True)
    college=models.CharField(max_length=50,null=True,blank=True) 
    order_number = models.PositiveIntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.choice.user.full_name
    
    class Meta:
        app_label = 'choices'

    def save(self, *args, **kwargs):
        if not self.id:
            # Calculate the next order number only for new records
            max_order = Level5.objects.aggregate(models.Max('order_number'))['order_number__max'] or 0
            self.order_number = max_order + 1
        super(Level5, self).save(*args, **kwargs)

class Other(models.Model):
    choice=models.ForeignKey(Choice,related_name="othr", on_delete=models.CASCADE)
    idea=models.CharField(max_length=50,null=True,blank=True)
    order_number = models.PositiveIntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.choice.user.full_name
    
    class Meta:
        app_label = 'choices'

    def save(self, *args, **kwargs):
        if not self.id:
            # Calculate the next order number only for new records
            max_order = Other.objects.aggregate(models.Max('order_number'))['order_number__max'] or 0
            self.order_number = max_order + 1
        super(Other, self).save(*args, **kwargs)
