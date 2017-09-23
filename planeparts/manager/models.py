from django.db import models

class PartType(models.Model):
    number = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    itemtype = models.CharField(max_length=50)
    
    price = models.CharField(max_length=20)
    condition = models.CharField(max_length=50)
    quantity = models.IntegerField(default=1)

    description = models.TextField()   
    def __str__(self):
        return self.name

class Part(models.Model):
    partType = models.ForeignKey('manager.PartType', related_name='Type')

    conditions = (
             (1,'New'),
             (2,'Refurbished'),
             (3,'Used'),
             (4,'For parts/not working'),
            )

    condition = models.IntegerField(choices=conditions)
    price = models.IntegerField()
    
    def __str__(self):
        return self.partType
