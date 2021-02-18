from django.urls import path

from apps.accounts import views

urlpatterns = [
    path('', views.account_page, name='account_page'),
    path('users/', views.all_users, name='all_users'),
    path('sign-up/', views.sign_up, name='sign_up'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('users/<user_id>/', views.view_profile, name='view_profile'),
    path('users/<user_id>/edit/', views.edit_profile, name='edit_profile'),

]