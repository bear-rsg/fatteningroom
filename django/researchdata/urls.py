from django.urls import path
from . import views, apps

app_name = apps.app_name

urlpatterns = [
    # Interact
    path('interact/', views.ArtObjectListView.as_view(), name='artobjects-list'),
    path('interact/<pk>/', views.ArtObjectDetailView.as_view(), name='artobjects-detail'),
    # Explore
    path('explore/', views.ExploreItemListView.as_view(), name='exploreitems-list'),
    path('explore/<pk>/', views.ExploreItemDetailView.as_view(), name='exploreitems-detail'),
    # Share
    path('share/', views.QuestionnaireCreateView.as_view(), name='questionnaire-create'),
    path('share/success/', views.QuestionnaireCreateSuccessTemplateView.as_view(), name='questionnaire-create-success'),
    # Export data
    path('exportdata/questionnaire/', views.questionnaire_exportdata, name='questionnaire-export'),
]
