from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('store/', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
	path('signup/', views.sign_up, name='signup'),
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

]