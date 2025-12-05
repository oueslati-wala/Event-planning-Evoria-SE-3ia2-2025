from django.db import models
  # This fetches the custom user model

 # This fetches the actual User model used in the project

class Event(models.Model):
    id_evenement = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=200)
    date_evenement = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('UserApp.User', on_delete=models.CASCADE, related_name="events")  # ForeignKey for User

    class Meta:
        ordering = ["-date_evenement", "nom"]

    def __str__(self):
        return f"{self.nom} ({self.date_evenement}) - User: {self.user.username}"
# Create your models here.