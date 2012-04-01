from django.db import transaction
import requests
from lxml import objectify
from skilltree.models import SkillGroup, Skill, SkillLevel
from logging import getLogger

log = getLogger(__name__)

class SkillImporter(object):
    def __init__(self, uri):
        self.uri = uri
        self._source = None

    def run(self):
        with transaction.commit_on_success():
            skills = objectify.fromstring(self.source)
            log.info("Starting import pass 1")
            self.pass1(skills)
            log.info("Starting import pass 2")
            self.pass2(skills)
            log.info("Finished import")

    def pass1(self, skills):
        # import skills themselves
        try:
            group = None
            for e in skills.result.rowset.getiterator():
                if e.tag == "rowset" and e.attrib.get("name") == "skillGroups":
                    continue
                elif e.tag == "row" and "groupName" in e.attrib:
                    group, created = SkillGroup.objects.get_or_create(
                        id=int(e.attrib.get("groupID")),
                        name=e.attrib.get("groupName")
                    )
                    log.info("  Imported SkillGroup '%s'", group)
                elif e.tag == "rowset" and e.attrib.get("name") == "skills":
                    continue
                elif e.tag == "row" and "typeName" in e.attrib:
                    if group and group.id == int(e.attrib.get("groupID")):
                        skill = Skill()
                        skill.name = e.attrib.get("typeName")
                        skill.group = group
                        skill.id = int(e.attrib.get("typeID"))
                        skill.published = e.attrib.get("published") == "1"
                        skill.description = e.description
                        skill.rank = int(e.rank)
                        skill.save()
                        log.info("    Imported Skill '%s'", skill)
                        SkillLevel.objects.create(skill=skill, level=1)
                        SkillLevel.objects.create(skill=skill, level=2)
                        SkillLevel.objects.create(skill=skill, level=3)
                        SkillLevel.objects.create(skill=skill, level=4)
                        SkillLevel.objects.create(skill=skill, level=5)
                    else:
                        # bad - blow up
                        raise ValueError("Invalid xml. Expecting group_id %d, got %d" % (group.id, int(e.attrib.get("groupID"))), e)

        except AttributeError as e:
            raise ValueError("Invalid skills xml", e)

    def pass2(self, skills):
        # import required skills
        for e in skills.result.rowset.getiterator():
            if e.tag == "row" and "typeName" in e.attrib:
                skill = Skill.objects.get(id=e.attrib.get("typeID"))
                for e2 in e.rowset.iterchildren():
                    level = int(e2.attrib.get("skillLevel"))
                    if level > 0:
                        skill.required_skills.add(
                            SkillLevel.objects.get(
                                skill__id=e2.attrib.get("typeID"),
                                level=level
                            )
                        )
                log.info("  Imported required skills for Skill '%s'", skill)

    @property
    def source(self):
        if not self._source:
            if "http" in self.uri:
                self._source = requests.get(self.uri).text.encode("UTF-8")
            else:
                # guess file
                with open(self.uri, "r") as f:
                    self._source = f.read()
        return self._source

def import_skills_from_api():
    importer = SkillImporter("http://api.eve-online.com/eve/SkillTree.xml.aspx")
    importer.run()
