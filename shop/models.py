from django.core.mail import send_mail
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_minimum = models.IntegerField(default=5)  # Seuil minimum de stock
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Nouveau champ image
    image = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True)

    def __str__(self):
        return self.name

    def check_stock(self):
        """Vérifie si le stock est inférieur au seuil et envoie une notification si nécessaire."""
        if self.stock <= self.stock_minimum:
            self.send_stock_alert()

    def send_stock_alert(self):
        """Envoie une notification par email si le stock est bas."""
        send_mail(
            subject=f"Stock bas pour le produit : {self.name}",
            message=f"Le stock du produit '{self.name}' est inférieur au seuil minimum.\n"
                    f"Quantité actuelle : {self.stock}\n"
                    f"Merci de réapprovisionner ce produit.",
            from_email='admin@monsite.com',
            recipient_list=['admin@monsite.com'],  # Email de l’administrateur
            fail_silently=False,
        )


class Order(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


class Cart(models.Model):
    user = models.ForeignKey('auth.User' , on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'
