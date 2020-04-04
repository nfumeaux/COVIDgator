from django.http import HttpResponse, Http404
from django.template import loader
from django.shortcuts import render
from .models import Article


# list of articles
def index(request):
    latest_articles_list = Article.objects.order_by('-article_date')[:5]
    template = loader.get_template('newsfeed/index.html')
    context = {'latest_articles_list': latest_articles_list}
    return HttpResponse(template.render(context, request))


# article and rating detail
def detail(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'newsfeed/detail.html', {'article': article})


