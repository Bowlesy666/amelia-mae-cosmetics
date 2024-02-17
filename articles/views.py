from django.shortcuts import render


def articles_list(request):
    """ Display all articles """
    return render(request, 'articles/articles_list.html')
