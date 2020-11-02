from django.urls import path

from . import views

urlpatterns = [
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),

	path('login/', views.login_view, name='login'),
	path('logout/', views.logout_view, name='logout'),
	path('register/', views.register_view, name='register'),

	path('create_product/', views.create_product_view, name='create_product'),
	path('edit_product/<int:pk>/', views.edit_product_view, name='edit_product'),
	path('delete_product/<int:pk>/', views.delete_product_view, name='delete_product'),

]