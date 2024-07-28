from django.views.generic import TemplateView


""" GENERIC VIEWS CUSTOM > DASHBOARD AND NGO """


class DashboardView(TemplateView):
    template_name = 'admins/dashboard.html'

