from django.shortcuts import redirect, render
from reviews.forms import CommentForm, ReviewForm
from .models import Comment, Review
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    reviews = Review.objects.order_by('-pk')
    context = {
        'reviews': reviews
    }
    return render(request, 'reviews/index.html', context)

@login_required
def create(request):
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            new_review_form = review_form.save(commit=False)
            new_review_form.user = request.user
            new_review_form.save()
            return redirect('reviews:index')
    else:
        review_form = ReviewForm()
    context = {
        'review_form': review_form
    }
    return render(request, 'reviews/create.html', context=context)

def detail(request, pk):
    review = Review.objects.get(pk=pk)
    comment_form = CommentForm()
    comments = Comment.objects.all()
    context = {
        'review': review,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'reviews/detail.html', context)

@login_required
def update(request, pk):
    review = Review.objects.get(pk=pk)
    if request.method == 'POST':
        review_form = ReviewForm(request.POST, instance=review)
        if review_form.is_valid():
            review_form.save()
            return redirect('reviews:detail', review.pk)
    else:
        review_form = ReviewForm(instance=review)
    context = {
        'review_form': review_form
    }
    return render(request, 'reviews/update.html', context)

@login_required
def delete(request, pk):
    review = Review.objects.get(pk=pk)
    review.delete()
    return redirect('reviews:index')

@login_required
def comment_create(request, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment_form = comment_form.save(commit=False)
            new_comment_form.user = request.user
            new_comment_form.review = review
            new_comment_form.save()
            return redirect('reviews:detail', review_pk)
    else:
        comment_form = CommentForm()
    context = {
        'comment_form': comment_form
    }
    return render(request, 'reviews/create.html', context=context)

@login_required
def comment_delete(request, review_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()
    return redirect('reviews:detail', review_pk)