from django.contrib import admin
from django.urls import path
from django.urls import include
from carsdb.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('carsdb.urls')),
    path('users/', include('users.urls', namespace='users')),
]

# Обработчики ошибок
handler403 = 'carsdb.views.error_403'
handler404 = 'carsdb.views.error_404'
handler500 = 'carsdb.views.error_500'