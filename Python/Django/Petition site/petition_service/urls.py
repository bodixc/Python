from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.Home, name='home'),
    path('all/', views.Petition_list, name='petition_list'),
    path('category/<str:category>/', views.Petition_list, name='petition_list'),
    path('category/random/', views.Petition_list, name='petition_list'),
    path('search/', views.Search, name='search'),
    path('overdue/', views.Petition_list, name='petition_list'),
    path('my-petitions/', views.Petition_list, name='petition_list'),
    path('petition/<int:id>/', views.PetitionDetail, name='petition_detail'),
    path('petition/<int:id>/sign/', views.Sign, name='sign'),
    path('petition/<int:id>/delete/', views.Delete, name='delete'),
    path('petition/create/', views.CreatePetition, name='create'),
    path('login/', views.Login),
    path('logout/', views.Logout),
    path('registration/', views.Registration),
    path('profile/', views.Profile, name='profile'),

]