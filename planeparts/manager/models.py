from django.db import models

class PartType(models.Model):
    number = models.CharField(max_length=30)
    description = models.CharField(max_length=50)
    
    price = models.CharField(max_length=30)
    condition = models.CharField(max_length=50)
    quantity = models.IntegerField(default=1)
    location = models.CharField(max_length=30)
    
    def __str__(self):
        return self.number

    def my_str(self):
        not_ok = [' ', '?', '%', '<', '>', '[', ']', '{', '}', '|', '\\', '^']
        s = self.description + self.price + self.condition + '---' + self.location
        return "".join([char for char in s if char not in not_ok])
