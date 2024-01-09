from django.db import models
from crowdfundingweb.models import Categoria
from django.contrib.auth.models import User
from django.db.models.functions import Concat
from django.db.models import Value
import django.utils.timezone 
    
class Campania(models.Model):
    categorias = models.ManyToManyField(Categoria, related_name = 'campanias') 
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre_campania = models.CharField(max_length=255, unique =True)
    slug = models.SlugField()
    descripcion_campania = models.TextField(blank = True) 
    imagen_campania = models.ImageField(upload_to='imagenes/', default='')
    video_campania = models.FileField(upload_to='videos_campania/', blank=True)
    monto_objetivo = models.DecimalField(max_digits=10, decimal_places=2, blank = False)
    fecha_inicio = models.DateField(null = False, default=django.utils.timezone.now)
    fecha_fin= models.DateField(blank = False)
    activa = models.BooleanField( null = False)
    inserted_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now = True)
    
    @property
    def categoriasCampanias(self):
        categorias = self.categorias.filter()
        return categorias
    
    @property
    def usuarioCampania(self):
        usuario = User.objects.annotate(fullname = Concat('first_name',Value(' '),'last_name')).get(username=self.usuario)
        return usuario.fullname
    
    @property
    def recaudacionCampania(self):
        contribuciones = self.campanias.all()
        total = sum([contribucion.monto_contribuido for contribucion in contribuciones])
        return total
    
    @property
    def porcentajeRecaudacion(self):
        total = sum ([contribucion.monto_contribuido for contribucion in self.campanias.all()])
        porcentajeRecaudacion = total/self.monto_objetivo * 100
        return round(porcentajeRecaudacion)
        
    @property
    def diasRestantes(self):
        dias = self.fecha_fin - self.fecha_inicio
        return f'{dias.days} dias restantes'      
    
    @property
    def conteoContribuyentes(self):
        contribuyentes = self.campanias.distinct('usuario').count()
        return contribuyentes
    
    def __str__(self) -> str:
        return f'{self.nombre_campania}'
    
    class Meta:
        db_table = 'pr_campania'
        verbose_name = 'Campaña'
        verbose_name_plural = 'Campañas'
