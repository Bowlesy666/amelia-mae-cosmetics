from django.db.models import Q
from django.contrib import messages
from django.db.models.functions import Lower

from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Product, Category, SkinType
from .forms import ProductForm


def all_products(request):
    """ A view to show all products, including sorting and search queries """
    products = Product.objects.all()

    query = None
    categories = None
    skin_types = None
    best_seller_list = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                # avoid losing original field name, use lower_name in place of sortkey
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'skin_type' in request.GET:
            has_skin_type = request.GET['skin_type']
            if has_skin_type:
                skin_types = request.GET['skin_type'].split(',')
                products = products.filter(skin_type__name__in=skin_types)
                skin_types = SkinType.objects.filter(name__in=skin_types)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'is_best_seller' in request.GET:
            best_sellers = request.GET['is_best_seller']
            if best_sellers:
                products = products.filter(is_best_seller=True)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                    messages.error(request, "You didnt enter any search criteria!")
                    return redirect(reverse('product_list'))
                
            # i before contains makes it not case sensitive, double underscore used here
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products_list.html', context)


def product_detail(request, product_id):
    """ A view to show individual product detail """
    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)


def product_admin(request):
    """ Choose the admin type for your store """
    return render(request, 'products/product_admin.html')


def add_product(request):
    """ Add a product to the store """
    form = ProductForm()
    template = 'products/add_product.html'

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('add_product'))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()

    context = {
        'form': form,
    }

    return render(request, template, context)


def edit_product(request, product_id):
    """ Edit a product in the store """
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)
