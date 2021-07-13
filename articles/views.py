from django.shortcuts import render, get_object_or_404, reverse, redirect
# from .scrape_main import main
from .models import Article, Article_detail, Comment, Category
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages, auth
from django.views.generic import (
    DetailView,
    ListView
   )
from django.contrib.auth.decorators import login_required
from .form import CommentForm
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
# Create your views here.


def home(request):
    # topic = request.GET.get('sports')
    cat_menu = Category.objects.all()
    # if request.method == 'POST':
    #     if 'latest_article' in request.POST:
    #         object_list = Article.objects.order_by('-date_posted')
    # else:
    object_list = Article.objects.all().order_by('article_detail__likes')
    # if topic == "All":
    #     object_list = Article.objects.all()
    #
    # elif topic:
    #     object_list = Article.objects.filter(category=topic)

    # main()
    # context = {
    #     'articles': Article.objects.all()
    # }
    paginator = Paginator(object_list, 20)  # 10 posts in each page
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        post_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        post_list = paginator.page(paginator.num_pages)
    # return render(request,
    #               'articles/home.html',
    #               {'page': page,
    #                'post_list': post_list,
    #                'topic': topic,
    #                'nbar': 'home',
    #                'cat_menu': cat_menu},
    #               )
    return render(request,
                  'articles/home.html',
                  {'page': page,
                   'post_list': post_list,
                   'nbar': 'home',
                   'cat_menu': cat_menu},
                  )

def latest_article( request):
    cat_menu = Category.objects.all()
    object_list = Article.objects.all().order_by('-date_posted')

    paginator = Paginator(object_list, 20)  # 10 posts in each page
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        post_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        post_list = paginator.page(paginator.num_pages)
    # return render(request,
    #               'articles/home.html',
    #               {'page': page,
    #                'post_list': post_list,
    #                'topic': topic,
    #                'nbar': 'home',
    #                'cat_menu': cat_menu},
    #               )
    return render(request,
                  'articles/latest_article.html',
                  {'page': page,
                   'post_list': post_list,
                   'nbar': 'latest',
                   'cat_menu': cat_menu},
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
    y = article_id.tweet_url
    tweets = eval(y)

    print(tweets)
    context = {
        'article_id': article_id,
        'body': body['description'],
        'tweets': tweets['tweets'],
        'len_tweets': len(tweets['tweets']),
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



#
# def add_comment(request, **kwargs):
#     a_id = kwargs.get('pk')
#     print(f'a_id {a_id}')
#     post = get_object_or_404(Article, article_id=a_id)
#     comments = post.comments.filter(parent__isnull=True)
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             parent_obj = None
#             try:
#                 # id integer e.g. 15
#                 parent_id = int(request.POST.get('parent_id'))
#                 print(f'{parent_id} = parent id')
#             except:
#                 parent_id = None
#                 print(f'{parent_id} = parent id')
#
#                 # if parent_id has been submitted get parent_obj id
#             if parent_id:
#                 parent_obj = Comment.objects.get(id=parent_id)
#                 print(f'{parent_obj} parent_obj')
#                 # if parent object exist
#                 if parent_obj:
#                     # create replay comment object
#                     replay_comment = form.save(commit=False)
#                     # assign parent_obj to replay comment
#                     replay_comment.parent = parent_obj
#             form.instance.article_id = a_id
#             form.instance.name = request.user
#             form.save()
#             # normal comment
#             # create comment object but do not save to database
#             new_comment = form.save(commit=False)
#
#             # assign ship to the comment
#             new_comment.post = post
#             # save
#             new_comment.save()
#
#
#             return redirect('article-detail', a_id)
#     else:
#         form = CommentForm(request.POST)
#     return redirect('article-detail', a_id)
#


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


def categoryview(request, cats):

    category_posts = Article.objects.filter(category=cats)
    category_posts = category_posts.order_by('-date_posted')
    cat_menu = Category.objects.all()
    paginator = Paginator(category_posts, 10)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        post_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        post_list = paginator.page(paginator.num_pages)

    return render(request, 'articles/categories.html', {'cats': cats,
                                                        'category_posts': category_posts,
                                                        'page': page,
                                                        'post_list': post_list,
                                                        'cat_menu': cat_menu
                                                        })




def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        contact_number = request.POST['contact-number']
        message = request.POST['message']
        total_message = f'{message}\nEmail: {email}\nContact me at: {contact_number}'
        # print(name,email,contact_number,message)
        send_mail(name, total_message, email, ['bajethaakshay@gmail.com'])
        messages.success(request, f'Thank You For Contacting US. We Will Contact You Soon')

    return render(request, 'articles/contact.html')

def about(request):
    return render(request, 'articles/about.html')



# def article_detail(request):
#     return render(request, 'articles/article_detail.html')