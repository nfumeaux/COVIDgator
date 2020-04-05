from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import Article, Vote


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
    # provide the current voting state for that user to properly display the buttons
    vote = Vote.objects.filter(vote_article_id=article_id).filter(vote_user=request.user)
    # convention here, 0 if no vote yet, -1 if disliked, 1 if liked
    vote_value = vote[0].vote_value if vote else 0
    # provide also 3 most liked and 3 most recent articles
    recent_articles = Article.objects.order_by('-article_date')[:3]
    popular_articles = Article.objects.order_by('-article_positive_votes')[:3]
    return render(request, 'newsfeed/detail.html', {'article': article, 'vote_value': vote_value,
                                        'recent_articles': recent_articles, 'popular_articles': popular_articles})


def vote(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    vote = Vote.objects.filter(vote_article_id=article_id).filter(vote_user=request.user)
    # as before, get the current vote value for the user to assess what to do depending on what button was clicked
    vote_value = vote[0].vote_value if vote else 0
    # get what the user pressed
    try:
        selected_choice = request.POST['choice']
    # handle a possible error
    except (KeyError, selected_choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'newsfeed/detail.html', {
            'article': Article.objects.get(pk=article_id),
            'vote_value': vote_value,
        })
    else:
        if selected_choice == 'like':
            if vote_value == 0:
                vote = Vote(vote_article=article, vote_value=1, vote_user=request.user)
                vote.save()
            elif vote_value == 1:
                vote[0].delete()
            elif vote_value == -1:
                vote[0].vote_value = 1
                vote[0].save()
        elif selected_choice == 'dislike':
            if vote_value == 0:
                vote = Vote(vote_article=article, vote_value=-1, vote_user=request.user)
                vote.save()
            elif vote_value == 1:
                vote[0].vote_value = -1
                vote[0].save()
            elif vote_value == -1:
                vote[0].delete()
            # article.article_negative_votes += 1
            # article.save()
    # redirect the user immediately to the details page
    return HttpResponseRedirect(reverse('newsfeed:detail', args=(article.id,)))