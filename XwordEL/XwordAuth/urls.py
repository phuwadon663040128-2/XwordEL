from django.urls import path

from . import views, views2

urlpatterns = [
    path('login/', views.XwordEL_login, name='login'),
    path('logout/', views.XwordEL_logout, name='logout'),
    path('signup/', views.XwordEL_signup, name='signup'),

    path('profile/', views2.XwordEL_profile, name='profile'),

    path('download/thaiplayedwords/', views2.XwordEL_download_thaiplayedwords, name='download_played_thai'),
    path('download/engplayedwords/', views2.XwordEL_download_engplayedwords, name='download_played_eng'),


]
