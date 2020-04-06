from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from .models import Article, Vote, Comment


# list of articles
def index(request):
    latest_articles_list = Article.objects.order_by('-article_date')[:5]
    template = loader.get_template('newsfeed/index.html')
    recent_articles = Article.objects.order_by('-article_date')[:4]
    popular_articles = Article.objects.order_by('-article_positive_votes')[:4]
    context = {'recent_articles': recent_articles, 'popular_articles': popular_articles}
    return HttpResponse(template.render(context, request))


# article and rating detail
def detail(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        raise Http404("Question does not exist")
    # provide the current voting state for that user to properly display the buttons
    if request.user.is_authenticated:
        vote = Vote.objects.filter(vote_article_id=article_id).filter(vote_user=request.user)
    else:
        vote = False
    # convention here, 0 if no vote yet, -1 if disliked, 1 if liked
    vote_value = vote[0].vote_value if vote else 0
    # provide also 3 most liked and 3 most recent articles
    recent_articles = Article.objects.order_by('-article_date')[:3]
    popular_articles = Article.objects.order_by('-article_positive_votes')[:3]
    # and the comments from this article
    comments = article.article_comments.all()
    print(comments)
    return render(request, 'newsfeed/detail.html', {'article': article, 'vote_value': vote_value,
                                        'recent_articles': recent_articles, 'popular_articles': popular_articles,
                                                    'comments': comments})


def vote(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.user.is_authenticated:
        vote = Vote.objects.filter(vote_article_id=article_id).filter(vote_user=request.user)
    else:
        # TODO: display and error message saying user should log-in to vote
        return HttpResponseRedirect(reverse('newsfeed:detail', args=(article.id,)))
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
                article.article_positive_votes += 1
            elif vote_value == 1:
                vote[0].delete()
                article.article_positive_votes -= 1
            elif vote_value == -1:
                vote[0].vote_value = 1
                vote[0].save()
                article.article_positive_votes += 1
                article.article_negative_votes -= 1
        elif selected_choice == 'dislike':
            if vote_value == 0:
                vote = Vote(vote_article=article, vote_value=-1, vote_user=request.user)
                vote.save()
                article.article_negative_votes += 1
            elif vote_value == 1:
                vote[0].vote_value = -1
                vote[0].save()
                article.article_positive_votes -= 1
                article.article_negative_votes += 1
            elif vote_value == -1:
                vote[0].delete()
                article.article_negative_votes -= 1
        article.save()
    # redirect the user immediately to the details page
    return HttpResponseRedirect(reverse('newsfeed:detail', args=(article.id,)))


def comment(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.user.is_authenticated:
        vote = Vote.objects.filter(vote_article_id=article_id).filter(vote_user=request.user)
    else:
        # TODO: display and error message saying user should log-in to comment
        return HttpResponseRedirect(reverse('newsfeed:detail', args=(article.id,)))
    vote_value = vote[0].vote_value if vote else 0
    try:
        comment_text = request.POST['comment']
    # handle a possible error
    except (KeyError, comment_text.DoesNotExist):
        # Redisplay the question voting form.

        return render(request, 'newsfeed/detail.html', {
            'article': Article.objects.get(pk=article_id),
            'vote_value': vote_value,
        })
    else:
        # add a comment to the article
        comment = Comment.objects.create(comment_text=comment_text,
                                         comment_user=request.user,
                                         comment_date=timezone.now())
        comment.save()
        article.article_comments.add(comment)
        article.save()
    return HttpResponseRedirect(reverse('newsfeed:detail', args=(article.id,)))