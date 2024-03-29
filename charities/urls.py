from django.urls import path
from .views import (select_person, BenefactorCreate,
                    CharityCreate, CreateProfile, CreateTask, show_tasks, task_request, task_related_charity_benefactor,
                    task_update_or_delete, show_benefactor, done_task)

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('select/', select_person, name='select'),
    path('benefactor/', BenefactorCreate.as_view(), name='benefactor'),
    path('charity/', CharityCreate.as_view(), name='charity'),
    path('profile/', CreateProfile.as_view(), name='profile'),
    path('task/', CreateTask.as_view(), name='tasks'),
    path('show_taskes/', show_tasks, name='list_taskes'),
    path('request/<slug:task_id>/', task_request, name='task_request'),
    path('task_ch_be/', task_related_charity_benefactor, name='task_ch_be'),
    path('update_delete/<str:command>/<slug:task_id>/',
         task_update_or_delete, name='update_delete'),
    path('show_benefactor/<slug:benefactor_id>/<slug:task_id>/', show_benefactor, name='show_be'),
    path('done/<slug:task_id>/', done_task, name='done')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
