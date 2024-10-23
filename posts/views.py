from django.shortcuts import render, redirect
from .models import Premise, Comment, ReplyOnComment
from django.http import JsonResponse

def comment_list(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login-user")

    premises = Premise.objects.all()
    for premise in premises:
        premise.comments = Comment.objects.filter(premise=premise)

    context = {
        'premises': premises
    }
    return render(request, "posts/post_detail.html", context)

def get_comments(request, premise_id):
    comments = Comment.objects.filter(premise_id=premise_id).prefetch_related('replies')  # Assuming a reverse relation
    data = []

    for comment in comments:
        replies = ReplyOnComment.objects.filter(reply_id=comment.id)
        replies_data = [{'user': reply.user.username, 'message': reply.text} for reply in replies]
        data.append({
            'id': comment.id,
            'user': comment.user.username,
            'message': comment.text,
            'replies': replies_data
        })

    return JsonResponse(data, safe=False)
