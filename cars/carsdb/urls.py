from django.urls import path
from . import views
from users.views import LoginUser, logout_user, ProfileUser, UserPasswordChange

urlpatterns =[
    path('', views.index, name='index'),
    path('parts/', views.parts_f, name='parts'),
    path('cars/', views.cars_f, name='cars'),
    path('addcars/', views.addcars_f.as_view(), name='add_cars'),
    path('addparts/', views.addparts_f.as_view(), name='add_parts'),
    path('parts/<int:pk>/edit/', views.UpdateParts.as_view(), name='edit_parts'),
    path('parts/<int:pk>/delete/', views.DeleteParts.as_view(), name='delete_parts'),
    path('cars/<int:pk>/edit/', views.UpdateCars.as_view(), name='edit_cars'),
    path('cars/<int:pk>/delete/', views.DeleteCars.as_view(), name='delete_cars'),
    path('acessor/', views.acces_f, name='acessor'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('profile/', ProfileUser.as_view(), name='profile'),
    path('password_change/', UserPasswordChange.as_view(), name='password_change'),
    ]
