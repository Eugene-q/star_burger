from django.db import models
from django.db.models import Q, F, Sum, Case, When
from django.core.validators import MinValueValidator

from phonenumber_field.modelfields import PhoneNumberField

class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class OrderQuerySet(models.QuerySet):
    def get_price(self):
        return Order.objects.annotate(
            price=Sum(F('order_items__price') * F('order_items__quantity'))
            )
        

class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=400,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


class Order(models.Model):
    datetime = models.DateTimeField(
        auto_now_add=True,
        null=True,
        db_index=True,
        verbose_name='Время заказа'
    )
    firstname = models.CharField(
        'имя',
        max_length=50,
        db_index=True,
    )
    lastname = models.CharField(
        'фамилия', 
        max_length=50,
        db_index=True,
    )
    phonenumber = PhoneNumberField(
        'телефон',
        db_index=True,
    )
    address = models.CharField(
        'адрес доставки',
        max_length=100,
        db_index=True,
    )
    
    objects = OrderQuerySet.as_manager()
    
    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'
        
    def __str__(self):
        return f'{self.firstname} {self.lastname} - {self.address}'
        
        
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='order_items',
        verbose_name='заказ',
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        related_name='order_items',
        verbose_name='продукт',
        on_delete=models.CASCADE,
    )
    price = models.DecimalField(
        blank=True,
        decimal_places=2,
        max_digits=6,
        verbose_name='цена',
        validators=[MinValueValidator(0)],
    )   
    quantity = models.IntegerField(
        verbose_name='количество',
        default=1,
        validators=[MinValueValidator(1)]
    )
    
    class Meta:
        verbose_name = 'элемент заказа'
        verbose_name_plural = 'элементы заказа'
        unique_together = [
            ['order', 'product']
        ]
    
    def set_price(self):
        self.price = self.product.price
        return self

    def __str__(self):
        return f"{self.order.address} - {self.product.name}"