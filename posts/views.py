from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment


def post_list(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login-user")
    context = {}
    return render(request, "posts/post_detail.html", context)

# def post_list(request):
#     posts = Post.objects.all()
#     return render(request, 'posts/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()

    if request.method == 'POST':
        author = request.POST.get('author')
        content = request.POST.get('content')

        print(f"Author: {author}, Content: {content}")

        if author and content:
            Comment.objects.create(post=post, author=author, content=content)
            return redirect('post_detail', pk=post.pk)

    return render(request, 'posts/post_detail.html', {'post': post, 'comments': comments})