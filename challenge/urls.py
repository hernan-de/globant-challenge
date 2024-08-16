"""
URL configuration for challenge project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api_rest.views import DepartmentBulkUpload, JobBulkUpload, HiredEmployeeBulkUpload, Requirement1, Requirement2

urlpatterns = [
    path('admin/', admin.site.urls),
    path('departments/upload/', DepartmentBulkUpload.as_view(), name='department-bulk-upload'),
    path('jobs/upload/', JobBulkUpload.as_view(), name='job-bulk-upload'),
    path('hired-employees/upload/', HiredEmployeeBulkUpload.as_view(), name='hired-employee-bulk-upload'),
    path('report/requirement1/', Requirement1.as_view(), name='report-requirement1'),
    path('report/requirement2/', Requirement2.as_view(), name='report-requirement2')
]
# http://127.0.0.1:8000/departments/upload/