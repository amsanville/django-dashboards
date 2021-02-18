from django.urls import path

from apps.core import views

urlpatterns = [
    path('', views.home, name='home'),
    # Dashboards
    path('dashboards/', views.all_dashboards, name='all_dashboards'),
    path('dashboards/<dashboard_id>/', views.view_dashboard, name='view_dashboard'),
    path('dashboard/create/', views.create_dashboard, name='create_dashboard'),
    path('dashboard/<dashboard_id>/edit/', views.edit_dashboard, name='edit_dashboard'),
    path('dashboard/<dashboard_id>/delete/', views.delete_dashboard, name='delete_dashboard'),

    # Individual panels
    path('panel/create/', views.create_panel, name='create_panel'),
    path('panel/<panel_id>/add/', views.add_panel, name='add_panel'),
    path('panel/<panel_id>/edit/', views.edit_panel, name='edit_panel'),
    path('panel/<panel_id>/delete/', views.delete_panel, name='delete_panel'),

    # Dashboard methods
    path('panel/<dashboard_id>/<panel_id>/remove/', views.remove_panel, name='remove_panel'),
]