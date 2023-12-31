"""
URL configuration for HG_Observa project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from tareas import views
from django.urls import path
from django.contrib.auth import views as auth_view
from django.urls import path, include
import django_sql_dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'), #This sets the home page to load up when you just have the standard addres example: PE_GE.com/
    path('add_lluvia/', views.add_lluvia, name='add_lluvia'),
    # path('add_tarea_done/', views.create_tarea, name='create_tarea'),
    # path('add_tarea_done/<int:theme_id>/', views.create_tarea, name='add_tarea_done'),
    path('add_tarea_planned/', views.planned_add_tarea, name='add_tarea'),
    path('tareas_list_planned/', views.tareas_list_planned, name='tareas_list_planned'),
    path('tareas_list_done/', views.tareas_list_done, name='tareas_list_done'),
    path('home/', views.home, name='home'), #This sets the home page to load up when you just have the standard addres example: PE_GE.com/
    path('graph-lluvias/', views.graph_lluvias, name='graph_lluvias'),
    path('show-graph/', views.show_graph, name='show_graph'),
    path('create-receta/', views.create_receta, name='create-receta'),
    path('select-theme/', views.select_theme, name='select_theme'),
    path('document_activity/', views.document_activity, name='document_activity'),
    path('add_tarea_done/', views.done_add_tarea, name='add_tarea_done'),
    # path('dashboard/', views.lluvias_chart, name='dashboard'),
    path('dashboards/', views.tareas_dashboard, name='dashboards'),
    # path("cosecha_dash/", views.cosecha_dash, name="cosecha-dash"),
    path('tareas_calendar_feed/', views.tareas_calendar_feed, name='tareas_calendar_feed'),
    path('update_tarea/<int:tarea_id>/', views.update_tarea, name='update_tarea'),
    path('show_task/', views.show_task, name='show_task'),
    path('tarea/<int:tarea_id>/', views.show_task, name='show_task'),


    ]

