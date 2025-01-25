from django.db import models
        
class Users(models.Model):
        nom = models.CharField(max_length=255)
        email = models.EmailField(unique=True)
        password = models.CharField(max_length=255, blank=True)
        role = models.CharField(max_length=255, blank=True)

    
        def __str__(self):
            return self.nom

        class Meta:
            db_table = "Users"

from django.utils.timezone import now

class Books(models.Model):
    titre = models.CharField(max_length=255)
    auteur = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    annee_publication = models.IntegerField()
    exemplaires_disponibles = models.PositiveIntegerField()

    def __str__(self):
        return self.titre

class Emprunt(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    date_emprunt = models.DateTimeField(default=now)
    date_retour_prevue = models.DateTimeField()
    date_retour_reelle = models.DateTimeField(null=True, blank=True)


    def is_overdue(self):
        return self.date_retour_reelle is None and self.date_retour_prevue < now()
