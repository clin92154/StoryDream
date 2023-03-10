from django.urls import path
from . import views  #引用這個資料夾中的views檔案
from gallery import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name = "MakerSpace"),#第二個參數需設定views.py中的檢視函式(View Function)名稱(index)
    path('generate/', views.generate),
    path('insert/',views.insert),
    path('book_create/', views.book_create),
    path('style_choose/', views.style_choose),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)