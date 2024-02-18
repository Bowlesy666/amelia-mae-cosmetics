from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib import messages

from .models import Article
from .forms import ArticleForm


def articles_list(request):
    """ Display all articles """
    articles = Article.objects.all()

    context = {
        'articles': articles,
    }

    return render(request, 'articles/articles_list.html', context)


def add_article(request):
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
            messages.error(request, 'Failed to add article. Please ensure the form is valid.')
            form = ArticleForm()
    else:
        form = ArticleForm()

    return render(request, template, context)


def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)

    context = {
        'article': article,
    }

    return render(request, 'articles/article_detail.html', context)


def edit_article(request, article_id):
    """ Edit an article """
    article = get_object_or_404(Article, pk=article_id)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated article!')
            return redirect(reverse('article_detail', args=[article.id]))
        else:
            messages.error(request, 'Failed to update article. Please ensure the form is valid.')
    else:
        form = ArticleForm(instance=article)
        messages.info(request, f'You are editing {article.title}')

    template = 'articles/edit_article.html'
    context = {
        'form': form,
        'article': article,
    }

    return render(request, template, context)


def delete_article(request, article_id):
    """ Delete an article """
    article = get_object_or_404(Article, pk=article_id)
    if request.method == 'POST':
        article.delete()
        messages.success(request, 'Article successfully deleted!')
        return redirect('articles_list')

    context = {
        'article': article,
    }
        
    return render(request, 'articles/confirm_to_delete_article.html', context)
