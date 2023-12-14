from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('rent-book/<str:pk>/', views.rent_book, name='rent-book'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-book/', views.add_book, name='add-book'),
    path('edit-book/<str:pk>/', views.edit_book, name='edit-book'),
    path('delete-book/<str:pk>/', views.delete_book, name='delete-book'),
    path('return-book/<str:pk>/', views.return_book, name='return-book'),

    path('make-staff/<str:pk>/', views.make_staff, name='make-staff'),
    path('demote-staff/<str:pk>/', views.demote_staff, name='demote-staff'),

    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
]