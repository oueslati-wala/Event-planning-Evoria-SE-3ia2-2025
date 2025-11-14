from django.db import models

# Create your models here.

class Event(models.Model):
    # PK custom (si tu préfères l'id par défaut, supprime cette ligne)
    id_evenement = models.AutoField(primary_key=True)

    nom = models.CharField(max_length=200)
    date_evenement = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_evenement", "nom"]  # tri admin par défaut

    def __str__(self):
        return f"{self.nom} ({self.date_evenement})"
