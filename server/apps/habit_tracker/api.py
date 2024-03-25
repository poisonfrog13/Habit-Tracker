from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from server.apps.habit_tracker import views


URL_NAME__HABITS_LIST = 'habitlist'
URL_NAME__HABITS_ONE = 'onehabit'
URL_NAME__HABIT_RECORDS = 'allrecords'
URL_NAME__RECORD_ONE = 'onerecord'

app_url_patterns = [
    path('habits/', views.HabitsList.as_view(), name=URL_NAME__HABITS_LIST),
    path('habits/<int:habit_pk>/', views.HabitDetail.as_view(), name=URL_NAME__HABITS_ONE),
    path('habits/<int:habit_pk>/records/', views.RecordsList.as_view(), name=URL_NAME__HABIT_RECORDS),
    path('habits/<int:habit_pk>/records/<int:record_pk>/', views.RecordDetail.as_view(), name=URL_NAME__RECORD_ONE),
]

urlpatterns = format_suffix_patterns(app_url_patterns)
