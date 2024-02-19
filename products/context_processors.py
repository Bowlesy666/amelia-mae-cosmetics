from .models import Product, Favourite


def user_favourites(request):
    favourited_by_user = []
    if request.user.is_authenticated:
        favourited_by_user = Favourite.objects.filter(
            user=request.user).values_list('product', flat=True)
        favourite_products = Product.objects.filter(id__in=favourited_by_user)
    else:
        favourite_products = favourited_by_user
    

    context = {
        'favourite_products': favourite_products,
    }

    return context