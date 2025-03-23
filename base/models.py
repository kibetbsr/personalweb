from django.db import models

# Create your models here.


class GuestEntry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # Ensure this field exists
    is_read = models.BooleanField(default=False) #this tracks the read and unread vmessages

    def __str__(self):
        return f"{self.name} - {self.message[:20]}"  # Preview message
    


    

#class Country(models.Model):
 #  name = models.CharField(max_length=255)
  # capital = models.CharField(max_length= 255)
#   population= models.IntegerField()
 #  currency = models.CharField(max_length=60)
 #  flag_url = models.URLField()


 #   def __str__(self):
  #      return self.name # thius returns the name of the country in django-admin


#class Law(models.Model):
  #its_number = models.PositiveIntegerField(unique=True)
  #its_law = models.TextField(max_length=255)

  #def __str__(self):
    # return f"Law {self.number}"
  
