from django.urls import path
from products import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='index'),
    path('add/', views.ProductAddView.as_view(), name='add'),
    path('details/<id>/', views.ProductDetailView.as_view(), name='detail'),
    path('edit/<id>/', views.ProductDetailsUpdateView.as_view(), name='edit'),
    path('delete/<id>/', views.ProductDeleteView.as_view(), name='delete'),
]
