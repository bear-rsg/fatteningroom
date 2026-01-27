from django.contrib import admin
from . import models


def publish(modeladmin, request, queryset):
    """
    Sets all selected objects in queryset to published
    """
    queryset.update(admin_published=True)


publish.short_description = "Publish selected articles (will appear on main site)"


def unpublish(modeladmin, request, queryset):
    """
    Sets all selected objects in queryset to not published
    """
    queryset.update(admin_published=False)


unpublish.short_description = "Unpublish selected articles (will not appear on main site)"


@admin.register(models.Article)
class ArticleAdminView(admin.ModelAdmin):
    """
    Customise the admin interface for Article model
    """
    list_display = (
        'title',
        'image',
        'content_preview',
        'admin_published',
        'meta_created_by',
        'meta_created_datetime',
        'meta_lastupdated_by',
        'meta_lastupdated_datetime',
        'meta_firstpublished_datetime'
    )
    list_display_links = ('title',)
    search_fields = ('title', 'content')
    readonly_fields = (
        'meta_created_by',
        'meta_created_datetime',
        'meta_lastupdated_by',
        'meta_lastupdated_datetime',
        'meta_firstpublished_datetime',
    )
    actions = (publish, unpublish)

    def get_actions(self, request):
        """
        Remove 'delete' action
        """
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def save_model(self, request, obj, form, change):
        """
        Update certain fields, e.g. meta_ fields, when model is saved in admin dashboard
        """
        # Meta: created by
        if getattr(obj, 'meta_created_by', None) is None:
            obj.meta_created_by = request.user
        # Meta: last updated by
        obj.meta_lastupdated_by = request.user
        # Save
        obj.save()

    class Media:
        css = {'all': ('/static/css/custom_admin.css',)}
