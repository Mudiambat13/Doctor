from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from core.views import home  # Importez la vue home

urlpatterns = [
    path('', home, name='home'),  # Page d'accueil sans préfixe
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),  # Autres URLs de l'application avec préfixe
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
