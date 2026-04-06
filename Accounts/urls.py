from django.urls import path
from Accounts import views

urlpatterns = [
    path('login', views.login_user, name="login"),
    path('signup', views.signup, name='signup'),
    path('save_user', views.save_user, name = 'save_user'),
    path('logout',views.logout_user,name='logout' )
]
