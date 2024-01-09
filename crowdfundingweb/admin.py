from django.contrib import admin
from crowdfundingweb.models import Categoria, Campania, Contribucion
 
admin.site.site_header = 'Administracion Crownfunding'

@admin.register (Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id','nombre_categoria' ,'slug','descripcion_categoria' ,
                    'imagen_categoria' ,'activa' ,'inserted_at' ,'updated_at' )


class ContribucionCampaniaTabInline(admin.TabularInline):
    list_display = ('id','campania','monto_contribuido')
    model = Contribucion
    extra = 0
    

@admin.register (Campania)
class CampaniaAdmin(admin.ModelAdmin):
    list_display = ('id','nombre_campania','slug', 'descripcion_campania',
                    'monto_objetivo', 'imagen_campania', 'video_campania',
                    'fecha_inicio','fecha_fin','activa','updated_at',
                    'inserted_at')
    inlines = [ContribucionCampaniaTabInline,]
    
# @admin.register (Contribucion)
# class ContribucionAdmin(admin.ModelAdmin):
#     list_display = ('monto_contribuido','fecha_contribucion', 'comentario_contribucion', 'inserted_at')

