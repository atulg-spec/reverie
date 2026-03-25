from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    SIZE_CHOICES = [
        ('5', 'UK 5'), ('6', 'UK 6'), ('7', 'UK 7'), ('8', 'UK 8'), ('9', 'UK 9'),
        ('0-6M', '0-6 Months'), ('6-12M', '6-12 Months'), ('1-2Y', '1-2 Years'),
        ('2-3Y', '2-3 Years'), ('3-4Y', '3-4 Years'), ('4-5Y', '4-5 Years'),
        ('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Extra Large'),
    ]

    name = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                          help_text='Original MRP for showing discount')
    description = models.TextField()
    sizes = models.CharField(max_length=500, blank=True,
                             help_text='Comma-separated sizes, e.g. 5,6,7,8 or 1-2Y,2-3Y,3-4Y')
    featured = models.BooleanField(default=False)
    in_stock = models.BooleanField(default=True)
    is_meesho_product = models.BooleanField(default=False, help_text='If true, product redirected to Meesho')
    meesho_url = models.URLField(blank=True, null=True, help_text='Meesho product link')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def primary_image(self):
        img = self.images.filter(is_primary=True).first()
        if not img:
            img = self.images.first()
        return img

    @property
    def size_list(self):
        if self.sizes:
            return [s.strip() for s in self.sizes.split(',')]
        return []

    @property
    def discount_percent(self):
        if self.original_price and self.original_price > self.price:
            return int(((self.original_price - self.price) / self.original_price) * 100)
        return 0


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=300, blank=True)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.name} - Image"
