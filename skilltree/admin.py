from django.contrib import admin
from django.contrib.admin import TabularInline, ModelAdmin
from skilltree.models import SkillGroup, Skill, SkillLevel

class SkillLevelInline(TabularInline):
    model = SkillLevel

class SkillAdmin(ModelAdmin):
    inlines = (SkillLevelInline,)
    filter_horizontal = ("required_skills", )

class SkillInline(TabularInline):
    model = Skill
    inlines = (SkillAdmin,)

class SkillGroupAdmin(ModelAdmin):
    inlines = (SkillInline,)

admin.site.register(SkillGroup, SkillGroupAdmin)
admin.site.register(Skill, SkillAdmin)
