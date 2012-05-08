# -*- coding: utf-8; mode: django -*-
"""
View for tasks with tests runner
"""
from django_jenkins.standalone import taskviews


class TaskDataExtract(taskviews.BaseTaskDataExtract):
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
    


class TaskDataView(taskviews.BaseTaskDataView):
    """
    Renters html part of ci index page
    """
    def add_build_data(self, build_data_id, build_data):
        pass

    def render_part(self, request):
        pass


class TaskDetailView(taskviews.BaseTaskDetailView):
    """
    Renders build task detail page
    """
    def view(request, build_id, build_data):
        pass

