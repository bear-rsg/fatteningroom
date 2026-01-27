from django.urls import path
from . import views, apps

app_name = apps.app_name

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='article-list'),
    path('<pk>/', views.ArticleDetailView.as_view(), name='article-detail'),
]
