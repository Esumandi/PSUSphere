from django.views.generic.list import ListView
from studentorg.models import Organization, College, Program, Student, OrgMember
from studentorg.forms import OrganizationForm, CollegeForm, ProgramForm, StudentForm, OrgMemberForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils import timezone


class OrganizationDeleteView(DeleteView):
    model = Organization
    template_name = 'crud_del.html'
    success_url = reverse_lazy('organization-list')

class HomePageView(ListView):
    model = Organization
    context_object_name = 'home'
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_students"] = Student.objects.count()
        context["org_count"] = Organization.objects.count()
        context["program_count"] = Program.objects.count()

        today = timezone.now().date()
        count = (
            OrgMember.objects.filter(
                date_joined__year=today.year
            )
            .values("student")
            .distinct()
            .count()
        )

        context["students_joined_this_year"] = count
        return context


class OrganizationList(ListView):
    model = Organization
    context_object_name = 'object_list'
    template_name = 'org_list.html'
    paginate_by = 5
    ordering = ["college__college_name", "name"]  # default

    def get_ordering(self):
        allowed = {"name", "college__college_name"}
        sort_by = self.request.GET.get('sort_by')
        direction = self.request.GET.get('direction', 'asc')
        if sort_by in allowed:
            if sort_by == 'college__college_name':
                order_list = [sort_by, 'name']
            else:
                order_list = [sort_by]
        else:
            order_list = self.ordering[:]
        if direction == 'desc' and order_list:
            order_list[0] = f"-{order_list[0].lstrip('-')}"
        return order_list

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(name__icontains=q) |
                Q(description__icontains=q) |
                Q(college__college_name__icontains=q)
            ).distinct()
        return qs

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
    ordering = ['college_name']

    def get_ordering(self):
        sort_by = self.request.GET.get('sort_by')
        direction = self.request.GET.get('direction', 'asc')
        order_list = ['college_name'] if sort_by == 'college_name' or not sort_by else self.ordering[:]
        if direction == 'desc':
            order_list[0] = f"-{order_list[0].lstrip('-')}"
        return order_list

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(Q(college_name__icontains=q)).distinct()
        return qs

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

    def get_ordering(self):
        allowed = ["prog_name", "college__college_name"]
        sort_by = self.request.GET.get("sort_by")
        direction = self.request.GET.get('direction', 'asc')
        if sort_by in allowed:
            if sort_by == 'college__college_name':
                order_list = [sort_by, 'prog_name']
            else:
                order_list = [sort_by]
        else:
            order_list = ['prog_name']
        if direction == 'desc':
            order_list[0] = f"-{order_list[0].lstrip('-')}"
        return order_list

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(prog_name__icontains=q) |
                Q(college__college_name__icontains=q)
            ).distinct()
        return qs

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
    ordering = ['lastname', 'firstname']

    def get_ordering(self):
        allowed = {"lastname", "firstname", "student_id", "program__prog_name"}
        sort_by = self.request.GET.get('sort_by')
        direction = self.request.GET.get('direction', 'asc')
        if sort_by in allowed:
            if sort_by in {"lastname", "firstname"}:
                secondary = 'firstname' if sort_by == 'lastname' else 'lastname'
                order_list = [sort_by, secondary]
            elif sort_by == 'program__prog_name':
                order_list = [sort_by, 'lastname']
            else:
                order_list = [sort_by]
        else:
            order_list = self.ordering[:]
        if direction == 'desc':
            order_list[0] = f"-{order_list[0].lstrip('-')}"
        return order_list

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(student_id__icontains=q) |
                Q(lastname__icontains=q) |
                Q(firstname__icontains=q) |
                Q(program__prog_name__icontains=q)
            ).distinct()
        return qs

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
    ordering = ['date_joined']

    def get_ordering(self):
        allowed = ["date_joined", "student__lastname", "organization__name"]
        sort_by = self.request.GET.get("sort_by")
        direction = self.request.GET.get('direction', 'asc')
        if sort_by in allowed:
            if sort_by == 'student__lastname':
                order_list = [sort_by, 'student__firstname']
            elif sort_by == 'organization__name':
                order_list = [sort_by, 'student__lastname']
            else:
                order_list = [sort_by]
        else:
            order_list = ['date_joined']
        if direction == 'desc':
            order_list[0] = f"-{order_list[0].lstrip('-')}"
        return order_list

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(student__lastname__icontains=q) |
                Q(student__firstname__icontains=q) |
                Q(organization__name__icontains=q)
            ).distinct()
        return qs

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
