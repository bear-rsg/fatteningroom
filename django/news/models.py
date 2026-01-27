from django.db import models
from django.urls import reverse
from account.models import User
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
import textwrap


class Article(models.Model):
    """
    A news article
    """

    title = models.CharField(max_length=1000, unique=True)
    image = models.ImageField(upload_to='news-articleimages')
    content = RichTextUploadingField()

    # Admin
    admin_published = models.BooleanField(default=False, verbose_name='published', help_text='Only published articles will appear on the public interface')
    admin_notes = models.TextField(blank=True, null=True, help_text='Optional. Used for internal notes. Only visible on this page and will not appear on public website.')

    # Metadata fields
    meta_created_by = models.ForeignKey(User, related_name="article_created_by",
                                        on_delete=models.PROTECT, blank=True, null=True, verbose_name="Created By")
    meta_created_datetime = models.DateTimeField(auto_now_add=True, verbose_name="Created")
    meta_lastupdated_by = models.ForeignKey(User, related_name="article_lastupdated_by",
                                            on_delete=models.PROTECT, blank=True, null=True, verbose_name="Last Updated By")
    meta_lastupdated_datetime = models.DateTimeField(auto_now=True, verbose_name="Last Updated")
    meta_firstpublished_datetime = models.DateTimeField(blank=True, null=True, verbose_name="First Published")

    @property
    def content_preview(self):
        return self.content[:100]

    @property
    def title_preview(self):
        return textwrap.shorten(self.title, width=70, placeholder='...')

    @property
    def public_date(self):
        if self.meta_firstpublished_datetime:
            return self.meta_firstpublished_datetime
        else:
            return self.meta_created_datetime

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:article-detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        # Set first published datetime value
        if self.admin_published and self.meta_firstpublished_datetime is None:
            self.meta_firstpublished_datetime = timezone.now()
        # Save object
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['admin_published', '-meta_firstpublished_datetime', 'id']
