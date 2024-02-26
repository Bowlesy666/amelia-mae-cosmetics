from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Article
from .forms import ArticleForm


def get_articles_and_sorting(request, template_name):
    """
    function to show all articles, including sorting
    and search queries,
    must pass the template name from view
    """
    articles = Article.objects.order_by('-created_on')

    query = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            articles = articles.order_by(sortkey)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didnt enter any search criteria!")
                return redirect(reverse('view_inventory'))

            # i before contains makes it not case sensitive
            queries = Q(title__icontains=query) | Q(content__icontains=query)
            articles = articles.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'search_term': query,
        'current_sorting': current_sorting,
        'articles': articles,
    }

    return render(request, template_name, context)


def articles_list(request):
    """ Display all articles """
    return get_articles_and_sorting(request, 'articles/articles_list.html')


@login_required
def add_article(request):
    """ view to add articles to the store """
    if not request.user.is_superuser:
        messages.error(request, 'This activity is reserved for store owners')
        redirect(reverse('home'))
    form = ArticleForm()
    template = 'articles/add_article.html'

    context = {
        'form': form,
    }

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added article!')
            return redirect(reverse('articles_list'))
        else:
            messages.error(
                request,
                'Failed to add article. Please ensure the form is valid.'
            )
            form = ArticleForm()
    else:
        form = ArticleForm()

    return render(request, template, context)


def article_detail(request, article_id):
    """ View to show article detail to user """
    article = get_object_or_404(Article, pk=article_id)

    context = {
        'article': article,
    }

    return render(request, 'articles/article_detail.html', context)


@login_required
def edit_article(request, article_id):
    """ Edit an article """
    if not request.user.is_superuser:
        messages.error(request, 'This activity is reserved for store owners')
        redirect(reverse('home'))
    article = get_object_or_404(Article, pk=article_id)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated article!')
            return redirect(reverse('article_detail', args=[article.id]))
        else:
            messages.error(
                request,
                'Failed to update article. Please ensure the form is valid.'
            )
    else:
        form = ArticleForm(instance=article)
        messages.info(request, f'You are editing {article.title}')

    template = 'articles/edit_article.html'
    context = {
        'form': form,
        'article': article,
    }

    return render(request, template, context)


@login_required
def delete_article(request, article_id):
    """ Delete an article """
    if not request.user.is_superuser:
        messages.error(request, 'This activity is reserved for store owners')
        redirect(reverse('home'))
    article = get_object_or_404(Article, pk=article_id)
    if request.method == 'POST':
        article.delete()
        messages.success(request, 'Article successfully deleted!')
        return redirect('articles_list')

    context = {
        'article': article,
    }

    return render(request, 'articles/confirm_to_delete_article.html', context)
