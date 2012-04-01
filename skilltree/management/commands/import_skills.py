from django.core.management.base import NoArgsCommand
from skilltree.importer import import_skills_from_api

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        import_skills_from_api()
