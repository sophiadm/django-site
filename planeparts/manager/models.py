from django.db import models

class PartType(models.Model):
    number = models.CharField(max_length=20)
    description = models.CharField(max_length=50)
    
    price = models.CharField(max_length=20)
    condition = models.CharField(max_length=50)
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return self.description

