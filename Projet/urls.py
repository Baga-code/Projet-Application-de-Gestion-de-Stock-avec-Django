from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('produit/', include('produits.urls')),
    path('', include('users.urls')),  # L'app d'authentification (connexion, inscription, etc.)
]

# Gérer les fichiers média (photos de produit, photos de profil, etc.)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Gérer les fichiers statiques (images, CSS, JS)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

