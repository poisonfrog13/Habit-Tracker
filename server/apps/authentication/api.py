from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views as auth_views

from server.apps.authentication import views as app_views


URL_NAME__SIGN_UP = 'sign_up'
URL_NAME__LOGIN = 'login'
URL_NAME__LOGOUT = 'logout'
URL_NAME__RESET_PASSWORD = 'reset_password'
URL_NAME__FORGOTTEN_PASSWORD_INIT = 'forgotten_password_init'
URL_NAME__FORGOTTEN_PASSWORD_FIN = 'forgotten_password_fin'

app_url_patterns = [
    path('sign_up/', app_views.sign_up, name=URL_NAME__SIGN_UP),
    path('login/', auth_views.obtain_auth_token, name=URL_NAME__LOGIN),
    path('who_am_I/', app_views.who_am_I),
    path('logout/', app_views.logout, name=URL_NAME__LOGOUT),
    path('reset_password/', app_views.reset_password, name=URL_NAME__RESET_PASSWORD),
    path('forgotten_password/', app_views.forgotten_password_initialize, name=URL_NAME__FORGOTTEN_PASSWORD_INIT),
    path('forgotten_password/<str:token>/', app_views.forgotten_password_finilize, name=URL_NAME__FORGOTTEN_PASSWORD_FIN),
]

urlpatterns = format_suffix_patterns(app_url_patterns, allowed=['json', 'html'])

