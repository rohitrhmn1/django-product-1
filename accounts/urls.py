from django.urls import path

from accounts import views

app_name = 'auth'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('details/<unique_id>/', views.UserInformationView.as_view(), name='details'),
    path('update/<unique_id>/', views.UserUpdateView.as_view(), name='update'),
    path('logout/', views.logout_view, name='logout'),

]
