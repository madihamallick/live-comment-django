from django.shortcuts import render, redirect


def comment_list(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login-user")
    context = {}
    return render(request, "posts/post_detail.html", context)
