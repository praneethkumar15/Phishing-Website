from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from PhisingDetection.views import login, registration, logout, search, addPost, getposts, 
deletepost, updateprofile, \
 viewprofile, activateAccount, testurlaction
urlpatterns = [
 path('admin/', admin.site.urls),
 path('', TemplateView.as_view(template_name='index.html'), name='login'),
 path('index/', TemplateView.as_view(template_name='index.html'), name='login'),
 path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
 path('loginaction/', login, name='loginaction'),
 path('registration/', TemplateView.as_view(template_name='registration.html'), 
name='registration'),
 path('regaction/', registration, name='regaction'),
 # path('addpost/',TemplateView.as_view(template_name = 'post.html'),name='post'),
 path('postaction/', addPost, name='post action'),
 path('getposts/', getposts, name='posts'),
 path('search/', search, name='searchposts'),
 path('deletepost/', deletepost, name='deletepost'),
 path('viewprofile/', viewprofile, name='transactions'),
 path('updateprofile/', updateprofile, name='transactions'),
 path('activateaction/', activateAccount, name='activateaction'),
 path('testurl/', TemplateView.as_view(template_name='testurl.html'), name='testurl'),
 path('testurlaction/', testurlaction, name='testurlaction'),
 path('logout/', logout, name='logout'),
]
