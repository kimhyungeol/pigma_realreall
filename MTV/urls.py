from django.urls import path
from . import views

app_name = 'MTV'

urlpatterns = [

path('', views.BoardList.as_view(), name= 'index'),
path('upload/', views.Upload.as_view(), name='upload'),
path('delete/<int:pk>/', views.BoardDelete, name='delete'),
path('<int:pk>/',views.Get.as_view(), name='get'),
path('comment/<int:document_id>/', views.document_detail, name="comment"),
path('comment/delete/<int:comment_id>/', views.comment_delete, name="comment_delete"),
path('result/', views.result, name='result')

]
