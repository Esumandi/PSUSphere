from django.core.management.base import BaseCommand
from faker import Faker
from studentorg.models import College, Program, Organization, Student, OrgMember
import random


class Command(BaseCommand):
    help = 'Create initial data for the application'

    def add_arguments(self, parser):
        parser.add_argument('--colleges', type=int, default=5, help='Number of colleges to create')
        parser.add_argument('--programs', type=int, default=15, help='Number of programs to create')
        parser.add_argument('--orgs', type=int, default=25, help='Number of organizations to create')
        parser.add_argument('--students', type=int, default=200, help='Number of students to create')
        parser.add_argument('--members', type=int, default=150, help='Number of memberships to create')

    def handle(self, *args, **kwargs):
        fake = Faker()
        # Order matters due to FKs
        self.create_colleges(kwargs['colleges'], fake)
        self.create_programs(kwargs['programs'], fake)
        self.create_organization(kwargs['orgs'], fake)
        self.create_students(kwargs['students'], fake)
        self.create_membership(kwargs['members'], fake)

    def create_colleges(self, count, fake):
        created = 0
        for _ in range(count):
            name = f"College of {fake.unique.word().title()}"
            College.objects.create(college_name=name)
            created += 1
        self.stdout.write(self.style.SUCCESS(f"Created {created} colleges."))

    def create_programs(self, count, fake):
        colleges = list(College.objects.all())
        if not colleges:
            self.stdout.write(self.style.WARNING('No colleges found. Skipping program creation.'))
            return
        created = 0
        for _ in range(count):
            college = random.choice(colleges)
            prog_name = f"BS {fake.unique.word().title()}"
            Program.objects.create(prog_name=prog_name, college=college)
            created += 1
        self.stdout.write(self.style.SUCCESS(f"Created {created} programs."))

    def create_organization(self, count, fake):
        colleges = list(College.objects.all())
        created = 0
        for _ in range(count):
            words = [fake.word() for _ in range(2)]
            organization_name = ' '.join(words).title()
            college = random.choice(colleges) if colleges and fake.boolean(chance_of_getting_true=80) else None
            Organization.objects.create(
                name=organization_name,
                college=college,
                description=fake.sentence()
            )
            created += 1
        self.stdout.write(self.style.SUCCESS(f"Created {created} organizations."))

    def create_students(self, count, fake):
        programs = list(Program.objects.all())
        if not programs:
            self.stdout.write(self.style.WARNING('No programs found. Skipping student creation.'))
            return
        created = 0
        for _ in range(count):
            Student.objects.create(
                student_id=f"{fake.random_int(2020,2025)}-{fake.random_int(1,8)}-{fake.random_number(digits=4)}",
                lastname=fake.last_name(),
                firstname=fake.first_name(),
                middlename=fake.first_name(),
                program=random.choice(programs)
            )
            created += 1
        self.stdout.write(self.style.SUCCESS(f"Created {created} students."))

    def create_membership(self, count, fake):
        students = list(Student.objects.all())
        orgs = list(Organization.objects.all())
        if not students or not orgs:
            self.stdout.write(self.style.WARNING('No students or organizations found. Skipping memberships.'))
            return
        created = 0
        for _ in range(count):
            OrgMember.objects.create(
            )
        self.stdout.write(self.style.SUCCESS(
            'Initial data for student organization created successfully.'))
