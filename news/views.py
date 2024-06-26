from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse, HttpResponseNotFound
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import AddPostForm
from .models import News, TagPost
from .utils import DataMixin


class HomePage(DataMixin, ListView):
    model = News
    template_name = 'index.html'
    context_object_name = 'posts'
    title_page = "БастыБет"
    cat_selected = 0

    def get_queryset(self):
        return News.published.all().select_related('cat')


@login_required
def about(request):
    contact_list = News.published.all()
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "about.html", {'title': "About site", 'page_obj': page_obj})


class AddPage(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'addpage.html'
    title_page = 'МақалаҚосу'
    permission_required = 'news.add_news'

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('home')


class UpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):
    model = News
    fields = '__all__'
    template_name = 'addpage.html'
    title_page = 'МақаланыЖаңарту'
    permission_required = 'news.change_news'


class DeletePage(PermissionRequiredMixin, DataMixin, DeleteView):
    model = News
    template_name = 'news_confirm_delete.html'
    success_url = reverse_lazy('home')
    title = 'МақаланыӨшіру'
    permission_required = 'news.delete_news'




def contacts(request):
    title = 'Contacts'
    return render(request, 'content.html', {'title': title})


class ShowPost(DataMixin, DetailView):
    template_name = 'post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_data(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(News.published, slug=self.kwargs[self.slug_url_kwarg])


class Categories(DataMixin, ListView):
    template_name = 'index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return News.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_data(context, title=context['posts'], cat_selected=cat.pk)


class TagPostLists(DataMixin, ListView):
    template_name = 'index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_data(context, title='title' + tag.tag)

    def get_queryset(self):
        return News.published.filter(tag__slug=self.kwargs['tag_slug']).select_related('cat')


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page not found</h1>")
