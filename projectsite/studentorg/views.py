from django.views.generic.list import ListView
from studentorg.models import Organization, College, Program, Student, OrgMember
from studentorg.forms import OrganizationForm, CollegeForm, ProgramForm, StudentForm, OrgMemberForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q

class OrganizationDeleteView(DeleteView):
    model = Organization
    template_name = 'crud_del.html'
    success_url = reverse_lazy('organization-list')

class HomePageView(ListView):
    model = Organization
    context_object_name = 'home'
    template_name = "home.html"

class OrganizationList(ListView):
     model = Organization
     context_object_name = 'object_list'
     template_name = 'org_list.html'
     paginate_by = 5

     def get_queryset(self):
         queryset = super().get_queryset()
         q = self.request.GET.get('q', '').strip()
         if q:
             queryset = queryset.filter(
                 Q(name__icontains=q)
                 | Q(description__icontains=q)
                 | Q(college__college_name__icontains=q)
             )
         return queryset

class OrganizationCreateView(CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'crud_form.html'
    success_url = reverse_lazy('organization-list')

class OrganizationUpdateView(UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'crud_form.html'
    success_url = reverse_lazy('organization-list')


# College CRUD
class CollegeList(ListView):
    model = College
    context_object_name = 'object_list'
    template_name = 'college_list.html'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q', '').strip()
        if q:
            queryset = queryset.filter(Q(college_name__icontains=q))
        return queryset

class CollegeCreateView(CreateView):
    model = College
    form_class = CollegeForm
    template_name = 'crud_form.html'
    success_url = reverse_lazy('college-list')

class CollegeUpdateView(UpdateView):
    model = College
    form_class = CollegeForm
    template_name = 'crud_form.html'
    success_url = reverse_lazy('college-list')

class CollegeDeleteView(DeleteView):
    model = College
    template_name = 'crud_del.html'
    success_url = reverse_lazy('college-list')

# Program CRUD
class ProgramList(ListView):
    model = Program
    context_object_name = 'object_list'
    template_name = 'program_list.html'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q', '').strip()
        if q:
            queryset = queryset.filter(
                Q(prog_name__icontains=q) | Q(college__college_name__icontains=q)
            )
        return queryset

class ProgramCreateView(CreateView):
    model = Program
    form_class = ProgramForm
    template_name = 'crud_form.html'
    success_url = reverse_lazy('program-list')

class ProgramUpdateView(UpdateView):
    model = Program
    form_class = ProgramForm
    template_name = 'crud_form.html'
    success_url = reverse_lazy('program-list')

class ProgramDeleteView(DeleteView):
    model = Program
    template_name = 'crud_del.html'
    success_url = reverse_lazy('program-list')

# Student CRUD
class StudentList(ListView):
    model = Student
    context_object_name = 'object_list'
    template_name = 'student_list.html'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q', '').strip()
        if q:
            queryset = queryset.filter(
                Q(student_id__icontains=q)
                | Q(lastname__icontains=q)
                | Q(firstname__icontains=q)
                | Q(middlename__icontains=q)
                | Q(program__prog_name__icontains=q)
            )
        return queryset


class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'crud_form.html'
    success_url = reverse_lazy('student-list')

class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'crud_form.html'
    success_url = reverse_lazy('student-list')

class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'crud_del.html'
    success_url = reverse_lazy('student-list')

# OrgMember CRUD
class OrgMemberList(ListView):
    model = OrgMember
    context_object_name = 'object_list'
    template_name = 'member_list.html'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q', '').strip()
        if q:
            queryset = queryset.filter(
                Q(student__lastname__icontains=q)
                | Q(student__firstname__icontains=q)
                | Q(student__student_id__icontains=q)
                | Q(organization__name__icontains=q)
            )
        return queryset

class OrgMemberCreateView(CreateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = 'crud_form.html'
    success_url = reverse_lazy('orgmember-list')

class OrgMemberUpdateView(UpdateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = 'crud_form.html'
    success_url = reverse_lazy('orgmember-list')

class OrgMemberDeleteView(DeleteView):
    model = OrgMember
    template_name = 'crud_del.html'
    success_url = reverse_lazy('orgmember-list')
