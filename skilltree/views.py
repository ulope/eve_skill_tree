from django.views.generic import TemplateView
from skilltree.models import SkillGroup

class SkillTreeView(TemplateView):
    template_name = "skilltree/tree.html"

    def get_context_data(self, **kwargs):
        context = super(SkillTreeView, self).get_context_data(**kwargs)
        context['groups'] = SkillGroup.objects.all()
        context['date'] = SkillGroup.objects.all()[0].created
        return context


