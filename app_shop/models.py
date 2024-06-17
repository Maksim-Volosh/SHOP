import random
import string

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


def random_slug():
    """
    Generate a random slug consisting of lowercase letters and digits.

    Returns:
        str: A random slug with a length of 3 characters.
    """
    
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(3))


class Category(models.Model):
    """
    Represents a category in the system.

    """
    
    name = models.CharField(
        max_length=100, db_index=True, verbose_name='Category name'
    )    
    
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name='Parent category'
    )
    
    slug = models.SlugField(
        max_length=255, unique=True, null=False, editable=True, verbose_name='Slug'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Created at'
    )
    
    
    class Meta:
        unique_together = (['slug', 'parent'])
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        """
        Return a string representation of the category.

        """
        
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' > '.join(full_path[::-1])
    
    def save(self, *args, **kwargs):
        """
        Save the instance.

        If the instance's slug is not set, it is set to a random slug based on the name of the category.
        The parent method is called to save the instance.

        """
        
        if not self.slug:
            self.slug = slugify(random_slug() + '-' + self.name)
        super(Category, self).save(*args, **kwargs)
        
    def get_absolute_url(self):
        """
        Return the absolute URL of the category.

        """
        
        return reverse('shop:category_list', args=[str(self.slug)])
    
    def get_all_subcategories(self):
        """
        Return all the subcategories of the category.

        """
        subcategories = list(self.children.all())
        for subcategory in subcategories:
            subcategories.extend(subcategory.get_all_subcategories())
        return subcategories
        
        
class Product(models.Model):
    """
    Represents a product in the system.

    """
    
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products', verbose_name='Category'
    )
    
    name = models.CharField(
        max_length=100, db_index=True, verbose_name='Product name'
    )
    
    brand = models.CharField(
        max_length=100, db_index=True, verbose_name='Brand name'
    )
    
    description = models.TextField(
        blank=True, verbose_name='Description'
    )
    
    slug = models.SlugField(
        max_length=255, verbose_name='Slug'
    )
    
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=99.99, verbose_name='Price'
    )
    
    image = models.ImageField(
        upload_to='products/products/%Y/%m/%d', blank=True, verbose_name='Image'
    )
    
    available = models.BooleanField(
        default=True, verbose_name='Available'
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Created at'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Updated at'
    )
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        """
        Return the absolute URL of the product.
        
        """
        return reverse('shop:product_detail', args=[str(self.slug)])
    
   

class ProductManager(models.Manager):
    def get_queryset(self):
        """
        Returns a queryset of available products.

        This method overrides the `get_queryset` method of the `ProductManager` class. It calls the parent's `get_queryset` method and filters the resulting queryset to only include products that are available.

        """
        
        return super(ProductManager, self).get_queryset().filter(available=True)
    
    
class ProductProxy(Product):
    
    objects = ProductManager()
    
    class Meta:
        proxy = True 