from django.db import models

class Categoria(models.Model):
    nombre_categoria = models.CharField(max_length = 255, unique = True)
    slug = models.SlugField(max_length=50, unique = True)
    descripcion_categoria = models.TextField()
    imagen_categoria = models.ImageField(upload_to='imagenes/', default='')
    activa = models.BooleanField()
    inserted_at = models.DateField(auto_now_add = True)
    updated_at = models.DateField(auto_now =True)
    
    def __str__(self) -> str:
        return f'{self.nombre_categoria}'
    
    class Meta:
        db_table = 'pr_categoria'
        verbose_name = 'Categoria'
        verbose_name_plural='Categorias'