from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower
from django.contrib.auth.models import AnonymousUser

from .models import Product, Category, SkinType, Reviews, Favourite
from inventory.models import InventoryItem
from .forms import ProductForm, ReviewsForm


def get_products_and_sorting(request, template_name):
    """
    function to show all products, including sorting and search queries
    must pass the template name from view
    """
    products = Product.objects.all()
    inventory_item_list = InventoryItem.objects.all()

    query = None
    categories = None
    skin_types = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                # avoid losing original field name
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

            # i before contains makes it not case sensitive
            queries = (
                Q(name__icontains=query) | Q(description__icontains=query)
            )
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
        'inventory_item_list': inventory_item_list,
    }

    return render(request, template_name, context)


def all_products(request):
    """ View for consumer to see all products, includes sorting function """
    return get_products_and_sorting(request, 'products/products_list.html')


@login_required
def admin_products_list(request):
    """ View for consumer to see all products, includes sorting function """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, this action is reserved \
            for store owners only')
        return redirect(reverse('home'))
    return get_products_and_sorting(
        request,
        'products/product_admin_product_list.html'
    )


def product_detail(request, product_id):
    """ A view to show individual product detail """
    product = get_object_or_404(Product, pk=product_id)
    reviews = Reviews.objects.filter(product_id=product_id)

    ratings_count = {
        'five_stars': reviews.filter(rating=5).count(),
        'four_stars': reviews.filter(rating=4).count(),
        'three_stars': reviews.filter(rating=3).count(),
        'two_stars': reviews.filter(rating=2).count(),
        'one_stars': reviews.filter(rating=1).count(),
    }

    def star_progress_method(ratings_value, reviews):
        if reviews.count() != 0:
            percentage = (
                ratings_count[ratings_value] / reviews.count()
                ) * 100

            return f'style="width: { percentage }%;"'

    five_stars_progress = star_progress_method(
        'five_stars', reviews)
    four_stars_progress = star_progress_method(
        'four_stars', reviews)
    three_stars_progress = star_progress_method(
        'three_stars', reviews)
    two_stars_progress = star_progress_method(
        'two_stars', reviews)
    one_stars_progress = star_progress_method(
        'one_stars', reviews)

    if isinstance(request.user, AnonymousUser):
        is_favourite = False
    else:
        is_favourite = Favourite.objects.filter(
            product_id=product_id, user=request.user
        ).exists()

    context = {
        'reviews': reviews,
        'ratings_count': ratings_count,
        'five_stars_progress': five_stars_progress,
        'four_stars_progress': four_stars_progress,
        'three_stars_progress': three_stars_progress,
        'two_stars_progress': two_stars_progress,
        'one_stars_progress': one_stars_progress,
        'product': product,
        'is_favourite': is_favourite,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def reviews_form(request, product_id):
    """ Handle form submission for adding reviews """
    if not request.user.is_authenticated:
        messages.error(request, 'You are not authorized to add a review.\
            Please login for access to this function.')
        return redirect(reverse('product_detail', args=[product_id]))
    if request.method == 'POST':
        form = ReviewsForm(request.POST)
        if form.is_valid():
            # Process the form data
            rating = form.cleaned_data['rating']
            comment = form.cleaned_data['comment']
            user_id = request.user.pk
            product_id = product_id

            # Save the review to the database
            Reviews.objects.create(
                rating=rating,
                comment=comment,
                user_id=user_id,
                product_id=product_id
            )

            messages.success(request, "Successfully added your review!")
            return redirect(reverse('product_detail', args=[product_id]))
    else:
        messages.error(request, "Oops, your review was unsuccessful!")
        return redirect(reverse('product_detail', args=[product_id]))

    return redirect(reverse('product_detail', args=[product_id]))


@login_required
def delete_review(request, product_id, review_id):
    """ Delete a review """
    review = get_object_or_404(Reviews, pk=review_id)
    if request.user != review.user:
        messages.error(request, 'You are not authorized to delete this review.\
            Please login for access to this function.')
        return redirect(reverse('product_detail', args=[product_id]))

    review.delete()
    messages.success(request, 'Review successfully deleted!')

    return redirect(reverse('product_detail', args=[product_id]))


@login_required
def product_admin(request):
    """ Choose the admin type for your store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, this action is reserved \
            for store owners only')
        return redirect(reverse('home'))
    return render(request, 'products/product_admin.html')


@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, this action is reserved \
            for store owners only')
        return redirect(reverse('home'))
    form = ProductForm()
    template = 'products/add_product.html'

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_admin'))
        else:
            messages.error(
                request,
                'Failed to add product. Please ensure the form is valid.'
            )
    else:
        form = ProductForm()

    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, this action is reserved \
            for store owners only')
        return redirect(reverse('home'))
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(
                request,
                'Failed to update product. Please ensure the form is valid.'
            )
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, this action is reserved \
            for store owners only')
        return redirect(reverse('home'))
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product successfully deleted!')
        return redirect('admin_products_list')

    context = {
        'product': product
    }

    return render(request, 'products/confirm_to_delete_product.html', context)


# @login_required
def add_favourite(request, product_id):
    """ Add a product to favourites """
    redirect_url = request.GET.get('redirect', reverse('product_list'))
    if not request.user.is_authenticated:
        messages.error(request, 'Login or Register to save your favourites \
            to your profile')
        return redirect(redirect_url)

    product = Product.objects.get(pk=product_id)
    Favourite.objects.get_or_create(
        user=request.user, product=product
    )

    messages.success(request, 'Product added to favourites')

    return redirect(redirect_url)


# @login_required
def delete_favourite(request, product_id):
    """ Delete a product from favourites """
    redirect_url = request.GET.get('redirect', reverse('product_list'))
    if not request.user.is_authenticated:
        messages.error(request, 'Login or Register to edit your favourites \
            on your profile')
        return redirect(redirect_url)

    product = Product.objects.get(pk=product_id)
    Favourite.objects.filter(user=request.user, product=product).delete()

    messages.success(request, 'Product removed from favourites')

    return redirect(redirect_url)


@login_required
def favourites_list(request):
    """ View for users to see their favourites """
    if not request.user.is_authenticated:
        messages.error(request, 'Login or Register to view your favourites \
            on your profile')
        return redirect('product_list')
    return render(request, 'products/favourites_list.html')
