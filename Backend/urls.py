from django.urls import path
from Backend import views


urlpatterns=[
        path('chatbot/', views.chatbot, name='chatbot'),
        path('index/',views.index,name="index"),
        path('Register/',views.Register,name="Register"),
        path('register/',views.register,name="register"),
        path('logout/',views.logout,name="logout"),
        path('login/',views.login,name="login"),
        path('history/',views.history,name="history")


]