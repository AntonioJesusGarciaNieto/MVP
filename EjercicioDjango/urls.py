from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from main import views
from main import recomendations

urlpatterns = [
    path('',views.index),
    path('index.html/', views.index),
    path('readme/', views.readme),
    path('login/', views.login),
    path('registro/', views.registro),
    path('logout/', views.logout),
    path('dossieres/', views.dossieres),
    path('show_dossier/', views.show_dossier),
    path('analyze/', views.analyze),  
    path('new_dossier/', views.new_dossier),
    path('new_skin_lesion/', views.new_skin_lesion),      
    path('admin/',admin.site.urls),
    ]

if settings.DEBUG:
    
    urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)