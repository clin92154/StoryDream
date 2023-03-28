from . import views
from django.urls import path
from gallery import settings
from django.conf.urls.static import static


urlpatterns = [
    path('register/',views.registerPage,name='register'),
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutUser,name='logout'),
    #path('accountCenter/',views.accountCenter,name='accountCenter'),
    path('<uid>/',views.accountCenter,name='accountCenter'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)