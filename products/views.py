from django.db.models import Q
from django.contrib import messages

from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Product, Category


def all_products(request):
    """ A view to show all products, including sorting and search queries """
    products = Product.objects.all()

    query = None
    categories = None
    skin_type = None

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                    messages.error(request, "You didnt enter any search criteria!")
                    return redirect(reverse('product_list'))
                
            # i before contains makes it not case sensitive, double underscore used here
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)


    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
    }

    return render(request, 'products/products_list.html', context)


def product_detail(request, product_id):
    """ A view to show individual product detail """
    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)
