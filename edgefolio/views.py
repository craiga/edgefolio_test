"""Edgefolio views."""

from django.urls import reverse
from django.views.generic import FormView


from edgefolio.forms import ExcelForm


class ExcelView(FormView):
    """Excel file upload view."""

    template_name = 'edgefolio/excel.html'
    form_class = ExcelForm

    def form_valid(self, form):
        """Create or update data from uploaded Excel file."""
        form.create_or_update_data(self.request)
        return super().form_valid(form)

    def get_success_url(self):
        """Get success URL."""
        return reverse('excel')
