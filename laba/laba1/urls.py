from django.contrib import admin
from django.urls import path, re_path
from firstapp import views

urlpatterns = [
    path('', views.main_window, name='home'),
    re_path(r'create/$', views.create),
    re_path(r'delete/$', views.delete),
    re_path(r'download/$', views.download),
    path('admin/', admin.site.urls),
    re_path(r'^', views.show_files),

]
