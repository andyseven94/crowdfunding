from django.db import models
from django.contrib.auth.models import User

from crowdfundingweb.models import Campania
    
class Contribucion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    campania_id =models.ForeignKey(Campania, on_delete = models.CASCADE, related_name = 'campanias')
    transaccion = models.CharField(default = 'A')
    monto_contribuido = models.DecimalField(max_digits=10, decimal_places=2, null = False)
    fecha_contribucion = models.DateField()
    comentario_contribucion =  models.TextField()
    inserted_at = models.DateTimeField(auto_now_add = True)
    
    def __str__(self) -> str:
        return f'{self.campania_id}: {self.monto_contribuido}'
   
    class Meta:
            db_table = 'pr_contribucion'
            verbose_name = 'Contribución'
            verbose_name_plural = 'Contribuciones'