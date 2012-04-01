from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Model, CharField, ForeignKey, BooleanField, TextField, PositiveSmallIntegerField, ManyToManyField
from django_extensions.db.models import TimeStampedModel
from zope.interface.exceptions import DoesNotImplement

class SkillGroup(TimeStampedModel):
    name = CharField("Name", max_length=300)

    class Meta(object):
        verbose_name = "Skill Group"
        verbose_name_plural = "Skill Groups"
        ordering = ("name",)

    def __unicode__(self):
        return self.name

class Skill(TimeStampedModel):
    name = CharField("Name", max_length=300)
    description = TextField("Description")
    rank = PositiveSmallIntegerField("Rank")
    published = BooleanField("Published")
    group = ForeignKey(SkillGroup, related_name="skills")
    required_skills = ManyToManyField("SkillLevel", verbose_name="Required Skills", symmetrical=False, related_name="enables_skills")

    class Meta(object):
        verbose_name = "Skill"
        verbose_name_plural = "Skills"
        ordering = ("name", )

    def __unicode__(self):
        return self.name

    def all_required_skills(self):
        required_skills = set()
        open_list = set((self,))
        seen_list = set()
        while open_list:
            current_skill = open_list.pop()
            for req in current_skill.required_skills.all():
                required_skills.add(req)
                if req.skill not in seen_list:
                    open_list.add(req.skill)
            seen_list.add(current_skill)
        return required_skills


class SkillLevel(TimeStampedModel):
    skill = ForeignKey(Skill, related_name="levels")
    level = PositiveSmallIntegerField("Level")

    class Meta(object):
        verbose_name = "Skill Level"
        verbose_name_plural = "Skill Levels"
        ordering = ("skill__name",  "level", )

    def __unicode__(self):
        return u"%s Level %d" % (self.skill.name, self.level)

    def previous(self):
        if self.level > 1:
            try:
                return SkillLevel.objects.get(level=self.level - 1, skill=self.skill)
            except ObjectDoesNotExist:
                return None
