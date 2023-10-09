from django.urls import path
from .views import FileFieldFormView
from . import views

urlpatterns = [
    path('upload/', FileFieldFormView.as_view(), name='upload_view_name'),
    path('success/', views.success, name='success_view_name'),  # Ajoutez votre vue de succès ici.
]  