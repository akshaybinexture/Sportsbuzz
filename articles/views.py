from django.shortcuts import render, get_object_or_404, reverse, redirect
# from .scrape_main import main
from .models import Article, Article_detail, Comment
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import (
    DetailView,
    ListView
   )
from .form import CommentForm
from django.http import HttpResponseRedirect
# Create your views here.


def home(request):
    topic = request.GET.get('sports')
    object_list = Article.objects.all()
    if topic == "All":
        object_list = Article.objects.all()

    elif topic:
        object_list = Article.objects.filter(category=topic)

    # main()
    # context = {
    #     'articles': Article.objects.all()
    # }
    paginator = Paginator(object_list, 10)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        post_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        post_list = paginator.page(paginator.num_pages)
    return render(request,
                  'articles/home.html',
                  {'page': page,
                   'post_list': post_list,
                   'topic': topic,
                   'nbar': 'home'},
                  )


def article_details(request, **kwargs):
    article_id = get_object_or_404(Article_detail, article_detail_id=kwargs.get('pk'))
    total_likes = article_id.total_likes()
    liked = False
    if article_id.likes.filter(id=request.user.id).exists():
        liked = True

    x = article_id.description
    body = eval(x)
    print(f'{article_id} = article_id')
    context = {
        'article_id': article_id,
        'body': body['description'],
        'total_likes': total_likes,
        'liked': liked,
        'form': CommentForm()
    }
    return render(request, 'articles/article_detail.html', context)


def likeview(request, article_id):
    print("hellllllo")
    article = get_object_or_404(Article_detail, article_detail_id=request.POST.get('post_id'))
    liked = False
    if article.likes.filter(id=request.user.id).exists():
        article.likes.remove(request.user)
        liked = False
    else:
        article.likes.add(request.user)
        liked = True
    print(f'article{article}')
    return redirect('article-detail', article_id)


def add_comment(request, **kwargs):
    a_id = kwargs.get('pk')
    print(f'a_id {a_id}')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.instance.article_id = a_id
            form.instance.name = request.user
            form.save()
            return redirect('article-detail', a_id)
    else:
        form = CommentForm(request.POST)
    return redirect('article-detail', a_id)

def contact(request):
    return render(request, 'articles/contact.html')


# def article_detail(request):
#     return render(request, 'articles/article_detail.html')