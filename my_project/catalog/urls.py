from django.urls import path
from . import views, api_views

app_name = 'catalog'

urlpatterns = [
    path('', views.home_page, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    path('product/<int:product_id>/add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:product_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('toggle-theme/', views.toggle_theme, name='toggle_theme'),
    path('api/categoties', api_views.CategoryListAPIView.as_view(), name='api_categories'),
    path('api/categoties/<int:pk>', api_views.CategoryDetailAPIView.as_view(), name='api_category_detail'),
    path('api/products', api_views.ProductListAPIView.as_view(), name='api_products'),
    path('api/products/<int:pk>', api_views.ProductDetailAPIView.as_view(), name='api_product_detail'),
    path('chat/<str:room_name>/', views.chat_room, name='chat_room'),
]
