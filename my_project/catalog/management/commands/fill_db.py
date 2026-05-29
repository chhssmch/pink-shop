from random import randint, choice
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from catalog.models import Category, Product
from orders.models import Order, OrderItem
from reviews.models import Review
from users.models import Profile

class Command(BaseCommand):
    def _create_users(self):
        User = get_user_model()
        users = []

        admin, admin_created = User.objects.get_or_create(
            username="admin",
            defaults={"email": "admin@example.com", "is_superuser": True, "is_staff": True}
        )
        
        if admin_created:
            admin.set_password("qwerty123")
            admin.save()
            self.stdout.write("Это мы создали суперпользователя :)")
        
        Profile.objects.get_or_create(user=admin)
        users.append(admin)

        for i in range(1, 4):
            user, created = User.objects.get_or_create(
                username=f"user{i}",
                defaults={"email": f"user{i}@example.com"}
            )

            if created:
                user.set_password("qwerty123")
                user.save()
                Profile.objects.get_or_create(user=user)
                self.stdout.write(f"Это мы создали юзера {user.username}")
            else:
                Profile.objects.get_or_create(user=user)
            
            users.append(user)

        return users

    def _create_categories(self):
        names = ["Сумка", "Одежда", "Обувь"]
        categories = []

        for name in names:
            cat, _ = Category.objects.get_or_create(
                name=name,
                defaults={"slug": name.lower()}
            )
            categories.append(cat)
            self.stdout.write("Создана категория")

        return categories

    def _create_products(self, categories):
        titles = ["Розовый товар 1", "Розовый товар 2", "Розовый товар 3"]
        products = []

        for i in range(10):
            cat = choice(categories)
            prod, _ = Product.objects.get_or_create(
                title=f"{choice(titles)} {i+1}",
                defaults={
                    "category": cat,
                    "description": "Супер пупер классный товар!",
                    "price": randint(1000, 5000),
                    "stock": randint(5, 20)
                }
            )
            products.append(prod)
            self.stdout.write("Создан товар")

        return products

    def _create_orders(self, users, products):
        for i in range(3):
            user = choice(users)
            order = Order.objects.create(user=user)
            OrderItem.objects.create(
                order=order,
                product=choice(products),
                price=1000,
                quantity=1
            )
            self.stdout.write("Создаём заказы")

    def _create_reviews(self, users, products):
        for i in range(5):
            Review.objects.get_or_create(
                user=choice(users),
                product=choice(products),
                defaults={"text": "Всё куплю", "rating": 5}
            )
            self.stdout.write("Отзывы тоже созданы...")

    def handle(self, *args, **options):
        self.stdout.write("Начинаем создание тестовых данных...")

        users = self._create_users()
        categories = self._create_categories()
        products = self._create_products(categories)
        self._create_orders(users, products)
        self._create_reviews(users, products)

        self.stdout.write(self.style.SUCCESS("Все данные успешно созданы!"))