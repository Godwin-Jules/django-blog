from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from .models import *
from .forms import CommentForm


all_posts_registered = Post.objects.all()

def get_date(post):
    return post.date

# Create your views here.


class IndexView(ListView):
    template_name = 'blog/index.html'
    model = Post
    ordering = ['-date']
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data


class PostsView(ListView):
    template_name = 'blog/all-posts.html'
    model = Post
    ordering = ['-date']
    context_object_name = 'all_posts'


class PostView(View):

    def is_stored(self, request, post_id):
        stored_posts = request.session.get('stored_posts')
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts    #type:ignore
        else:
            is_saved_for_later = False

        return is_saved_for_later

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        

        return render(request, 'blog/post-detail.html', {
            'post': post,
            'post_tags': post.tags.all(),
            'comment_form': CommentForm(),
            'comments': post.comments.all().order_by('-id'),     #type:ignore
            'saved_for_later': self.is_stored(request, post.id)      #type:ignore
        })

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse('blog-post', args=[slug]))

        return render(request, 'blog/post-detail.html', {
            'post': post,
            'post_tags': post.tags.all(),
            'comment_form': comment_form,
            'comments': post.comments.all().order_by('-id'),     #type:ignore
            'saved_for_later': is_stored(request, post.id)      #type:ignore
        })


class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get('stored_posts')
        context = {}

        if stored_posts is None or len(stored_posts) == 0:
            context['posts'] = []
            context['has_posts'] = False
        else:
            context['posts'] = Post.objects.filter(id__in = stored_posts)
            context['has_posts'] = True

        return render(request, 'blog/read-later.html', context)


    def post(self, request):
        stored_posts = request.session.get('stored_posts')
        post_id = int(request.POST['post_id'])
        post_slug = Post.objects.get(id = post_id).slug

        if  stored_posts is None:
            stored_posts = []

        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)

        request.session['stored_posts'] = stored_posts

        return HttpResponseRedirect(reverse('blog-post', args=[post_slug]))
