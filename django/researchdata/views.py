from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView, TemplateView, DetailView
from django.urls import reverse_lazy
from django.http import HttpResponse
from datetime import datetime
from . import models, forms
import csv
import io


class ArtObjectListView(ListView):
    """
    Class-based view to show the ArtObject list template
    """
    template_name = 'researchdata/artobject-list.html'
    queryset = models.ArtObject.objects.filter(published=True)


class ArtObjectDetailView(DetailView):
    """
    Class-based view to show the ArtObject detail template
    """
    template_name = 'researchdata/artobject-detail.html'
    queryset = models.ArtObject.objects.filter(published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Queryset only includes root objects (those with no parent_text_part)
        # as recursive code in the template will loop through descendents
        context['object_data'] = [
            {'label': 'Reference', 'data': self.object.reference},
            {'label': 'Description', 'data': self.object.description},
            {'label': 'Carver', 'data': self.object.carver},
            {'label': 'Location', 'data': self.object.location},
            {'label': 'Date', 'data': self.object.date},
            {'label': 'Material', 'data': self.object.material},
            {'label': 'Collection', 'data': self.object.collection},
        ]

        return context


class QuestionnaireCreateView(CreateView):
    """
    Class-based view to show the 'share your questionnaire' template
    """
    template_name = 'researchdata/questionnaire-create.html'
    form_class = forms.QuestionnaireCreateForm
    success_url = reverse_lazy('researchdata:questionnaire-create-success')


class QuestionnaireCreateSuccessTemplateView(TemplateView):
    """
    Class-based view to show the questionnaire create success template
    """
    template_name = 'researchdata/questionnaire-create-success.html'


@login_required
def questionnaire_exportdata(request):
    """
    Functional view that exports data from Questionnaire objects as a CSV file
    """

    # Define the content (column titles and data) to write to file
    column_titles = [[
        "Questionnaire ID",
        "Story Text",
        "Story File",
        "Permission to Contact",
        "Permission to Make Data Public",
        "Email",
        "Age",
        "Gender",
        "Ethnicity",
        "Country of Residence",
        "Admin Notes",
        "Created",
        "Last Updated"
    ]]
    data = [
        [
            obj.id,
            obj.story_text,
            obj.story_file,
            obj.permission_contact,
            obj.permission_public,
            obj.email,
            obj.age,
            obj.gender,
            obj.ethnicity,
            obj.country_of_residence,
            obj.admin_notes,
            obj.created.strftime('%d %b %Y %X'),
            obj.lastupdated.strftime('%d %b %Y %X'),
        ] for obj in models.Questionnaire.objects.all()
    ]

    # Create an in-memory text buffer (StringIO for CSV writer)
    csv_buffer = io.StringIO()
    # Create a CSV writer object
    csv_writer = csv.writer(csv_buffer)
    # Write data to the CSV buffer
    csv_writer.writerows(column_titles + data)
    csv_file_content = csv_buffer.getvalue()
    csv_buffer.close()

    # Create and return the file as response
    response = HttpResponse(csv_file_content, content_type='text/csv')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    response['Content-Disposition'] = f'attachment; filename="bfr_questionnaires_{timestamp}.csv"'
    return response
