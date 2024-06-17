from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import Category, Product, ProductProxy


class ProductViewTests(TestCase):
    def test_get_products(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        
        uploaded = SimpleUploadedFile(name='small.gif', content=small_gif, content_type='image/gif')
        category = Category.objects.create(name='Django')
        product_1 = Product.objects.create(
            category=category,
            name='Django Book',
            slug='django-book',
            image=uploaded,
        )
        product_2 = Product.objects.create(
            category=category,
            name='Django Book2',
            slug='django-book2',
            image=uploaded,
        )
        responce = self.client.get(reverse('shop:products'))
        self.assertEqual(responce.status_code, 200)
        self.assertEqual(responce.context['products'].count(), 2)
        self.assertEqual(list(responce.context['products']), [product_1, product_2])
        self.assertContains(responce, product_1)
        self.assertContains(responce, product_2)
        

class ProductDetailViewTest(TestCase):
    def test_get_product_by_slug(self):
        # Create a product
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        uploaded = SimpleUploadedFile(
            'small.gif', small_gif, content_type='image/gif'
        )
        category = Category.objects.create(name='Category 1')
        
        product = Product.objects.create(
            name='Product 1',
            category=category,
            slug='product-1',
            image=uploaded
        )
        
        # Make a request to the product detail view with the product's slug
        response = self.client.get(
            reverse('shop:product_detail', kwargs={'slug': 'product-1'})
        )

        # Check that the response is a success
        self.assertEqual(response.status_code, 200)

        # Check that the product is in the response context
        self.assertEqual(response.context['product'], product)
        self.assertEqual(response.context['product'].slug, product.slug)


class CategoryListViewTest(TestCase):
    def setUp(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        uploaded = SimpleUploadedFile(
            'small.gif', small_gif, content_type='image/gif')
        self.category = Category.objects.create(
            name='Test Category', slug='test-category')
        self.product = ProductProxy.objects.create(
            name='Test Product', slug='test-product', category=self.category, image=uploaded)

    def test_status_code(self):
        response = self.client.get(
            reverse('shop:category_list', args=[self.category.slug]))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(
            reverse('shop:category_list', args=[self.category.slug]))
        self.assertTemplateUsed(response, 'app_shop/category_list.html')

    def test_context_data(self):
        response = self.client.get(
            reverse('shop:category_list', args=[self.category.slug]))
        self.assertEqual(response.context['category'], self.category)
        self.assertEqual(response.context['products'].first(), self.product)