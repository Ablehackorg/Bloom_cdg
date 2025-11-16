from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Post, Comment
from django.urls import reverse_lazy


class BlogCreateView(CreateView):
    model = Post
    fields = ['title', 'content', 'image', 'video']
    template_name = 'blog/list.html'  # This will be handled by the modal
    success_url = reverse_lazy('blog-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class BlogListView(ListView):
    model = Post
    template_name = "blog/list.html"
    context_object_name = "posts"
    ordering = ["-created_at"]


class BlogDetailView(DetailView):
    model = Post
    template_name = "blog/detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем 3 последних поста, исключая текущий для related posts
        context['related_posts'] = Post.objects.exclude(id=self.object.id).order_by('-created_at')[:3]
        # Для боковой панели - последние 5 постов (включая текущий, потом исключим в шаблоне или нет)
        context['recent_posts'] = Post.objects.all().order_by('-created_at')[:5]
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user.is_authenticated:
            text = request.POST.get("text")
            if text and text.strip():
                Comment.objects.create(post=self.object, user=request.user, text=text.strip())
        return redirect("blog-detail", pk=self.object.pk)


@require_POST
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return JsonResponse({
        'liked': liked,
        'likes_count': post.likes.count()
    })


@require_POST
@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(request.user)
        liked = False
    else:
        comment.likes.add(request.user)
        liked = True

    return JsonResponse({
        'liked': liked,
        'likes_count': comment.likes.count()
    })