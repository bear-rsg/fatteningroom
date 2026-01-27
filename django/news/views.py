from django.views.generic import (DetailView, ListView)
from django.db.models import Q
from django.urls import reverse
from . import models


class ArticleDetailView(DetailView):
    """
    Class-based view for Article detail template
    """
    template_name = 'news/article-detail.html'

    def get_queryset(self):
        queryset = models.Article.objects.all()
        return queryset if self.request.user.is_authenticated else queryset.filter(admin_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['admin_url'] = reverse('admin:news_article_change', args=[self.object.id])
        return context


class ArticleListView(ListView):
    """
    Class-based view for Article list template
    """
    template_name = 'news/article-list.html'
    paginate_by = 50

    def get_queryset(self):
        queryset = models.Article.objects.all()
        # Filter published for non-admins
        queryset = queryset if self.request.user.is_authenticated else queryset.filter(admin_published=True)
        # Search
        search = self.request.GET.get('search', '')
        if search != '':
            queryset = queryset.filter(Q(title__icontains=search) | Q(content__icontains=search))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['example'] = 'TODO'

        return context
