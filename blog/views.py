from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
#from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm


# Create your views here.
# def post_list(request):
#    objects_list = Post.objects.all()  # Get all posts
#    paginator = Paginator(objects_list, 3) # 3 Posts in each page
#    page = request.GET.get('page')
#    try:
#        posts = paginator.page(page)
#    except PageNotAnInteger:
#        # if page is not an integer deliver the first page
#        posts = paginator.page(1)
#    except EmptyPage:
#        # if page is out of page deliver the last page of results
#        posts = paginator.page(paginator.num_pages)
#    return render(request,
#                 'blog/post/list.html',
#                {'page': page,
#                'posts': posts})


# Class based views
class PostListView(ListView):
    queryset = Post.objects.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


# A view to display a single post
# add comment form logic
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             # status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # List of active comments on this blog
    comments = post.comments.filter(active=True)

    if request.method == 'Post':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create a comment object but don't save to the database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # save the comment ot the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'comment_form': comment_form})


# Handling the email form in our view
def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'Post':
        # form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # form fields passed validation
            cd = form.cleaned_data
            # .. send email
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form})

