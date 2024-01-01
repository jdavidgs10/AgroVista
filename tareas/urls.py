from django.urls import path
from . import views

#URLConf Module (URL Configuration)
urlpatterns = [
    path('home/', views.home)




]


handler404 = 'tareas.views.error_404'

handler500 = 'tareas.views.error_500'

handler403 = 'tareas.views.error_403'

handler400 = 'tareas.views.error_400'