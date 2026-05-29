from django.urls import path
from . import views, api_views

app_name = 'orders'

urlpatterns = [
    path('list/', views.order_list, name='order_list'),
    path('api/orders/', api_views.OrderListAPIView.as_view(), name='api_order_list'),
    path('api/orders/<int:pk>/', api_views.OrderDetailAPIView.as_view(), name='api_order_detail'),
    path('api/orders/<int:order_id>/items/', api_views.OrderItemListAPIView.as_view(), name='api_order_items'),
    path('api/orders/<int:order_id>/items/<int:pk>/', api_views.OrderItemDetailAPIView.as_view(), name='api_order_item_detail'),
]