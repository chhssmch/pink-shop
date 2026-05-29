import pytest
from decimal import Decimal
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient


from catalog.models import Category, Product
from orders.models import Order, OrderItem
from reviews.models import Review

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="alice",
        password="pass123",
        email="alice@example.com",
    )


@pytest.fixture
def category(db):
    return Category.objects.create(name="Смартфоны", slug="smartphones")


@pytest.fixture
def product(db, category):
    return Product.objects.create(
        category=category,
        title="iPhone 15",
        description="Крутой телефон",
        price=Decimal("99999.99"),
        stock=10,
        is_available=True,
    )


@pytest.fixture
def order(db, user):
    return Order.objects.create(user=user)


@pytest.fixture
def order_item(db, order, product):
    return OrderItem.objects.create(
        order=order,
        product=product,
        price=Decimal("12345.00"),
        quantity=2,
    )


@pytest.fixture
def review(db, product, user):
    return Review.objects.create(
        product=product,
        user=user,
        text="Отличный товар!",
        rating=5,
    )

@pytest.mark.django_db
def test_products_api_returns_list(api_client, product):
    """API списка товаров должен вернуть 200 и список с товарами"""
    # 1. Получаем URL по имени маршрута
    url = reverse('catalog:api_products')
    # 2. Отправляем GET-запрос к API
    response = api_client.get(url)
    # 3. Проверяем, что эндпоинт вообще работает и вернул 200 OK
    assert response.status_code == 200
    # 4. Разбираем JSON-ответ и проверяем полезные данные
    data = response.json()
    assert len(data) == 1  # мы создали ровно один товар в фикстуре
    assert data[0]['title'] == 'iPhone 15'
    assert data[0]['price'] == '99999.99'

@pytest.mark.django_db
def test_api_me_returns_profile_for_authenticated_user(api_client, user):
    """Авторизованный пользователь должен получить свой профиль"""
    # 1. Говорим клиенту считать все запросы от имени этого пользователя
    api_client.force_authenticate(user=user)
    # 2. Строим URL до эндпоинта /api/me/
    url = reverse('users:api_my_profile')
    # 3. Делаем запрос
    response = api_client.get(url)
    # 4. Проверяем статус — должен быть 200 OK
    assert response.status_code == 200
    # 5. Разбираем JSON и смотрим, что вернулся именно наш пользователь
    data = response.json()
    assert data['user']['username'] == user.username
    assert 'phone' in data
    assert 'address' in data

@pytest.mark.django_db
def test_categories_api_returns_list(api_client, category):
    """API списка категорий должен вернуть 200 и список с категориями"""
    url = reverse('catalog:api_categories')
    response = api_client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['name'] == 'Смартфоны'
    assert data[0]['slug'] == 'smartphones'
    assert 'id' in data[0]


@pytest.mark.django_db
def test_orders_api_returns_list_for_authenticated_user(api_client, user, order):
    """API списка заказов должен возвращать только заказы авторизованного пользователя"""
    api_client.force_authenticate(user=user)
    url = reverse('orders:api_order_list')
    response = api_client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['id'] == order.id
    assert 'user' in data[0]
    assert 'created_at' in data[0]


@pytest.mark.django_db
def test_reviews_api_returns_list(api_client, review):
    """API списка отзывов должен вернуть 200 и список с отзывами"""
    url = reverse('reviews:api_review_list')
    response = api_client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['text'] == 'Отличный товар!'
    assert data[0]['rating'] == 5
    assert 'user' in data[0]
    assert 'product' in data[0]


@pytest.mark.django_db
def test_product_detail_api_returns_nested_category(api_client, product):
    """API детальной информации о товаре должен возвращать вложенную категорию"""
    url = reverse('catalog:api_product_detail', kwargs={'pk': product.id})
    response = api_client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data['title'] == 'iPhone 15'
    assert 'category' in data
    assert data['category']['name'] == 'Смартфоны'
    assert data['category']['slug'] == 'smartphones'
    assert 'id' in data['category']


@pytest.mark.django_db
def test_order_detail_api_returns_nested_user_and_items(api_client, user, order, order_item):
    """API детальной информации о заказе должен возвращать вложенные данные пользователя и позиций"""
    api_client.force_authenticate(user=user)
    url = reverse('orders:api_order_detail', kwargs={'pk': order.id})
    response = api_client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == order.id
    assert 'user' in data
    assert data['user']['username'] == user.username
    assert 'items' in data
    assert len(data['items']) == 1
    assert data['items'][0]['quantity'] == 2
    assert 'product' in data['items'][0]
    assert data['items'][0]['product']['title'] == 'iPhone 15'