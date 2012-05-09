# -*- coding: utf-8; mode: django -*-
"""
Store and view task results data in standalone ci
"""
from django.views.generic import View


class BaseTaskDataExtract(object):
    def extract_build_data(self, tasks):
        """
        Extrats current build ci data 
        """
        return {}

    def extract_details_data(self, tasks):
        """
        Extract details view data
        """
        return None
    


class BaseTaskDataView(object):
    """
    Renters html part of ci index page
    """
    def add_build_data(self, build_id, build_data):
        pass

    def render_part(self, request):
        pass


class TaskDetailView(View):
    """
    Renders build task detail page
    """
    def view(request, build_id, build_data):
        pass
