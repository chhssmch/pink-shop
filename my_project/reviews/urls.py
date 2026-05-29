from django.urls import path
from . import views, api_views

app_name = 'reviews'

urlpatterns = [
    path('all/', views.review_list, name='review_list'),
    path('product/<int:product_id>/add/', views.add_review, name='add_review'),
    path('<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('api/reviews/', api_views.ReviewListAPIView.as_view(), name='api_review_list'),
    path('api/reviews/<int:pk>/', api_views.ReviewDetailAPIView.as_view(), name='api_review_detail'),

]