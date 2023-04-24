from django.urls import path
from . import views  #引用這個資料夾中的views檔案
from gallery import settings
from django.conf.urls.static import static


urlpatterns = [
    # path(, views.makerspace, name='book_id'),#第二個參數需設定views.py中的檢視函式(View Function)名稱(index)
    path('<int:book_id>/', views.makerspace , name="md"),#第二個參數需設定views.py中的檢視函式(View Function)名稱(index)
    path('', views.makerspace, name = "MakerSpace"),#第二個參數需設定views.py中的檢視函式(View Function)名稱(index)
    path('generate/', views.generate),
    path('insert/',views.insert),
    path('remove/',views.remove),
    path('showpage/',views.showpage),
    path('book_create/', views.book_create,name="book_create"),
    path('style_choose/<book_id>/', views.style_choose, name='book_id'),
    path('ChangeLocation/', views.ChangeLocation , name='ChangeLocation')
   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)