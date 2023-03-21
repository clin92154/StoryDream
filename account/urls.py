from . import views
from django.urls import path
from gallery import settings
from django.conf.urls.static import static


urlpatterns = [
    path('register/',views.registerPage,name='register'),
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutUser,name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)