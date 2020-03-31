from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField( max_digits=20, decimal_places=2, default=39.99)
    image = models.FileField(upload_to='main-products/', null=True, blank=True)
    def __str__(self):
        return self.title

        