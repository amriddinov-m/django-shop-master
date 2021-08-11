import os
from datetime import datetime

from django.conf.global_settings import MEDIA_ROOT
from django.contrib import admin
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.template.response import TemplateResponse
from django.urls import path

from dsshop.settings import BASE_DIR
from other.models import Project
from other.tasks import import_xls


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    filter_horizontal = ['cat', ]
    change_list_template = 'admin/project_changelist.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('importer/', self.my_view, name='importer'),
        ]
        return my_urls + urls

    def my_view(self, request):
        if request.FILES:
            fs = FileSystemStorage(location=os.path.join(BASE_DIR, 'media/imported_files/'))
            f = File(request.FILES['file'])
            filename = fs.save(name='products.xlsx', content=f)
            import_xls.delay(os.path.join(BASE_DIR, 'media/imported_files/')+str(filename))
        context = dict(
            self.admin_site.each_context(request),
        )
        return TemplateResponse(request, "admin/import_view.html", context)
