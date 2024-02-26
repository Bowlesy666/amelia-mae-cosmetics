from products.models import Product, Category
from articles.models import Article


def display_range_of_queryset(request):
    """
    Retrieve a range of items from different querysets to display on a page.

    Returns a context dictionary containing the best seller products,
    categories, and articles to be displayed on the page.
    """
    best_seller_list = Product.objects.filter(is_best_seller=True)[:3]
    category_list = Category.objects.all()[:3]
    article_list = Article.objects.order_by('-created_on')[:2]

    context = {
        'best_seller_list': best_seller_list,
        'category_list': category_list,
        'article_list': article_list,
    }

    return context
