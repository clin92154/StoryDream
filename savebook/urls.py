from django.urls import path
from . import views  #引用這個資料夾中的views檔案
from gallery import settings
from django.conf.urls.static import static


urlpatterns = [
    path('save/<int:book_id>/', views.save, name = "save"),#第二個參數需設定views.py中的檢視函式(View Function)名稱(index)
    path('<int:book_id>/', views.savebook, name = "savebook"),#第二個參數需設定views.py中的檢視函式(View Function)名稱(index)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)