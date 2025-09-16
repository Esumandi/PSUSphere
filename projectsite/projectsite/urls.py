"""
URL configuration for projectsite project.

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
from django.views.generic import TemplateView

from studentorg.views import (
    HomePageView,
    OrganizationList, OrganizationCreateView, OrganizationUpdateView, OrganizationDeleteView,
    CollegeList, CollegeCreateView, CollegeUpdateView, CollegeDeleteView,
    ProgramList, ProgramCreateView, ProgramUpdateView, ProgramDeleteView,
    StudentList, StudentCreateView, StudentUpdateView, StudentDeleteView,
    OrgMemberList, OrgMemberCreateView, OrgMemberUpdateView, OrgMemberDeleteView,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomePageView.as_view(), name="home"),

    # Organization
    path('organization_list', OrganizationList.as_view(), name='organization-list'),
    path('organization_list/add', OrganizationCreateView.as_view(), name='organization-add'),
    path('organization_list/<pk>', OrganizationUpdateView.as_view(), name='organization-update'),
    path('organization_list/<pk>/delete', OrganizationDeleteView.as_view(), name='organization-delete'),

    # Org Members
    path('members', OrgMemberList.as_view(), name='orgmember-list'),
    path('members/add', OrgMemberCreateView.as_view(), name='orgmember-add'),
    path('members/<pk>', OrgMemberUpdateView.as_view(), name='orgmember-update'),
    path('members/<pk>/delete', OrgMemberDeleteView.as_view(), name='orgmember-delete'),

    # Students
    path('students', StudentList.as_view(), name='student-list'),
    path('students/add', StudentCreateView.as_view(), name='student-add'),
    path('students/<pk>', StudentUpdateView.as_view(), name='student-update'),
    path('students/<pk>/delete', StudentDeleteView.as_view(), name='student-delete'),

    # Colleges
    path('colleges', CollegeList.as_view(), name='college-list'),
    path('colleges/add', CollegeCreateView.as_view(), name='college-add'),
    path('colleges/<pk>', CollegeUpdateView.as_view(), name='college-update'),
    path('colleges/<pk>/delete', CollegeDeleteView.as_view(), name='college-delete'),

    # Programs
    path('programs', ProgramList.as_view(), name='program-list'),
    path('programs/add', ProgramCreateView.as_view(), name='program-add'),
    path('programs/<pk>', ProgramUpdateView.as_view(), name='program-update'),
    path('programs/<pk>/delete', ProgramDeleteView.as_view(), name='program-delete'),
]