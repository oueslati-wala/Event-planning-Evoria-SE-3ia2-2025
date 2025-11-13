from django.db import models


class Caterer(models.Model):
    name = models.CharField(max_length=120)
    company_name = models.CharField(max_length=160, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    website = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=(('active', 'Actif'), ('inactive', 'Inactif')),
        default='active'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name or self.name


class MenuItem(models.Model):
    title = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    category = models.CharField(
        max_length=40,
        choices=(
            ('entree', 'Entrée'),
            ('main', 'Plat'),
            ('dessert', 'Dessert'),
            ('drink', 'Boisson'),
        ),
        default='main'
    )
    is_available = models.BooleanField(default=True)
    caterer = models.ForeignKey(Caterer, null=True, blank=True, on_delete=models.SET_NULL, related_name='menu_items')

    def __str__(self):
        return self.title
