from django.contrib import admin
from django.db.models import ForeignKey, ManyToManyField
from django.utils.safestring import mark_safe
from django.urls import reverse
from . import models
from .apps import app_name


# Reusable functions


def fk_link(object, fk_field):
    """
    Generate a link for foreign key fields in admin lists
    """
    try:
        fk = getattr(object, fk_field)  # get the foreign key object
        model_name = fk.__class__.__name__.lower().replace('_', '')
        url = reverse(f"admin:{app_name}_{model_name}_change", args=[fk.id])
        return mark_safe(f'<a href="{url}">{fk}</a>')
    except AttributeError:
        return "-"  # If FK value is null


def get_manytomany_fields(model, exclude=[]):
    """
    Returns a list of strings containing the field names of many to many fields of a model
    To ignore certain fields, provide a list of such fields using the exclude parameter
    """
    return list(f.name for f in model._meta.get_fields() if type(f) is ManyToManyField and f.name not in exclude)


def get_foreignkey_fields(model, exclude=[]):
    """
    Returns a list of strings containing the field names of foreign key fields of a model
    To ignore certain fields, provide a list of such fields using the exclude parameter
    """
    return list(f.name for f in model._meta.get_fields() if type(f) is ForeignKey and f.name not in exclude)


class GenericAdminView(admin.ModelAdmin):
    """
    This is a generic base class for admin views

    This class can either be inherited from if further customisations are needed, e.g.:
    class [ModelName]AdminView(GenericAdminView):

    Or if no changes are needed, just register a model, e.g.:
    admin.site.register([model name], GenericAdminView)
    """
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name',)
    search_fields = ('name',)

    def get_actions(self, request):
        """
        Remove 'delete' action
        """
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set all many to many fields to display the filter_horizontal widget
        self.filter_horizontal = get_manytomany_fields(self.model)
        # Set all foreign key fields to display the autocomplete widget
        self.autocomplete_fields = get_foreignkey_fields(self.model)


# Simple Admin Views

admin.site.register(models.Collection, GenericAdminView)
admin.site.register(models.Material, GenericAdminView)


# Custom Admin Views


@admin.register(models.ArtObject)
class ArtObjectAdminView(GenericAdminView):
    """
    Customise the admin interface for ArtObject model
    """

    list_display_links = ('id',)
    list_display = (
        'id',
        'reference',
        'description',
        'carver',
        'location',
        'date',
        'material',
        'collection',
        'published',
        'created',
        'lastupdated'
    )
    search_fields = (
        'reference',
        'description',
        'carver',
        'location',
        'date',
    )
    readonly_fields = (
        'created',
        'lastupdated',
    )


@admin.register(models.Questionnaire)
class QuestionnaireAdminView(admin.ModelAdmin):
    list_display = ('id', 'story_text', 'story_file', 'email', 'created', 'lastupdated')
    search_fields = (
        'story_text',
        'story_file',
        'email',
        'age',
        'gender',
        'ethnicity',
        'country of residence',
        'admin_notes'
    )
    readonly_fields = (
        'created',
        'lastupdated',
    )
