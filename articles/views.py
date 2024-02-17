from django.shortcuts import render, reverse, redirect
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


