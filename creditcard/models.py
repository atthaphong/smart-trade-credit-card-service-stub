from django.db import models

# Create your models here.
class Account(models.Model):
    number = models.CharField(max_length=16,unique=True)
    ccv = models.CharField(max_length=3)
    balance = models.FloatField()

    def is_paid(self,amount):
        if  self.balance >= amount:
            self.balance -= amount
            self.save()
            print('*** %s %s ***' % (self.balance,amount))
            return True
        else:
            return False

    def is_verified(self,amount):
        if  self.balance >= amount:
            return True
        else:
            return False
    def __unicode__(self):
        return '%s %s %s' % (self.number,self.ccv,self.balance)

