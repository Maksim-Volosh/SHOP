from django.shortcuts import render, get_object_or_404

from .models import Category, Product, ProductProxy


def products_all(request):
    products = Product.objects.all()
    return render(request, 'app_shop/products.html', {'products': products})


def product_detail(request, slug):
    product = get_object_or_404(ProductProxy, slug=slug)
    return render(request, 'app_shop/product_detail.html', {'product': product})


def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    subcategories = category.get_all_subcategories()
    subcategories_ids = [subcat.id for subcat in subcategories]
    subcategories_ids.append(category.id)
    products = ProductProxy.objects.select_related('category').filter(category_id__in=subcategories_ids)
    context = {
        'category': category,
        'products': products
    }
    return render(request, 'app_shop/category_list.html', context=context)
