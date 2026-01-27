from django.db import models
from django.urls import reverse
from django.db.models.functions import Upper
from django.conf import settings
from django.core.mail import send_mail
import logging


logger = logging.getLogger(__name__)


# Secondary Models


class Collection(models.Model):
    """
    A collection in which an ArtObject exists
    """

    related_name = 'collections'

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = [Upper('name'), 'id']


class Material(models.Model):
    """
    A material used to make an ArtObject
    """

    related_name = 'materials'

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = [Upper('name'), 'id']


# Primary Model


class ArtObject(models.Model):
    """
    An object created by an artist, e.g. wooden carved figure
    """

    related_name = 'art_objects'

    reference = models.CharField(max_length=255, blank=True, null=True, help_text='e.g. catalogue code')
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='art-objects')
    interactive_object_embed_code = models.TextField(blank=True, null=True)
    carver = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    date = models.CharField(max_length=255, blank=True, null=True)
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, blank=True, null=True)
    collection = models.ForeignKey(Collection, on_delete=models.SET_NULL, blank=True, null=True)
    published = models.BooleanField(default=False, help_text='Only published Art Objects will appear on the public web interface')
    admin_notes = models.TextField(blank=True, null=True, help_text='Optional. Used for internal notes. Only visible on this page and will not appear on public website.')
    created = models.DateTimeField(auto_now_add=True)
    lastupdated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('researchdata:artobjects-detail', args=[str(self.id)])

    def __str__(self):
        return f'Art Object #{self.id}'


class Questionnaire(models.Model):
    """
    A Questionnaire completed by a user via the website's Share section
    """

    class AgeBrackets(models.TextChoices):
        BELOW_16 = 'U16', 'Below 16'
        AGE_16_25 = '16-25', '16-25'
        AGE_26_35 = '26-35', '26-35'
        AGE_36_45 = '36-45', '36-45'
        AGE_46_55 = '46-55', '46-55'
        AGE_56_65 = '56-65', '56-65'
        ABOVE_65 = '65+', '65+'

    # Story
    story_text = models.TextField()
    story_file = models.FileField(upload_to='questionnaires', blank=True, null=True)

    # Permission
    permission_contact = models.BooleanField(default=False)
    permission_public = models.BooleanField(default=False)

    # User info
    email = models.EmailField(blank=True, null=True)
    age = models.CharField(max_length=5, choices=AgeBrackets.choices, blank=True, null=True)
    gender = models.CharField(max_length=255, blank=True, null=True)
    ethnicity = models.CharField(max_length=255, blank=True, null=True)
    country_of_residence = models.CharField(max_length=255, blank=True, null=True)

    admin_notes = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    lastupdated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """ When a new object is saved email the research team """

        if not self.created:
            try:
                send_mail("Beyond the Fattening Room: New questionnaire",
                          "A new questionnaire has been submitted to the database",
                          settings.DEFAULT_FROM_EMAIL,
                          settings.NOTIFICATION_EMAIL,
                          fail_silently=True)
            except Exception:
                logger.exception("Failed to send email")
        super().save(*args, **kwargs)
