from django.urls import path
from . import views

urlpatterns = [
    path('<int:User_Id>',views.Index,name='Index_page'),
    path('Main/<int:User_Id>',views.Main,name='Main_Page'),
    path('Leaderboard/<int:User_Id>', views.Leaderboard, name='Leaderboard_Page'),
    path('Friends/<int:User_Id>',views.Friends,name='Friends_Page'),
    path('Crafts/<int:User_Id>',views.Crafts,name='Crafts_Page'),
    path('Add_coins_SM/<int:amount>/<int:User_Id>/<str:SM>',views.Add_coins_SM,name='Add_coins_SM'),
]
