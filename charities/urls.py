from django.urls import path
from .views import select_person, BenefactorCreate, CharityCreate, CreateProfile, CreateTask, show_tasks
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('select/', select_person, name='select'),
    path('benefactor/', BenefactorCreate.as_view(), name='benefactor'),
    path('charity/', CharityCreate.as_view(), name='charity'),
    path('profile/', CreateProfile.as_view(), name='profile'),
    path('task/', CreateTask.as_view(), name='tasks'),
    path('show_taskes/', show_tasks, name='list_taskes'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
