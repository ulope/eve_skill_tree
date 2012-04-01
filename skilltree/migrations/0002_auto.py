# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field required_skills on 'Skill'
        db.create_table('skilltree_skill_required_skills', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('skill', models.ForeignKey(orm['skilltree.skill'], null=False)),
            ('skilllevel', models.ForeignKey(orm['skilltree.skilllevel'], null=False))
        ))
        db.create_unique('skilltree_skill_required_skills', ['skill_id', 'skilllevel_id'])

        # Removing M2M table for field required_skills on 'SkillLevel'
        db.delete_table('skilltree_skilllevel_required_skills')

    def backwards(self, orm):
        # Removing M2M table for field required_skills on 'Skill'
        db.delete_table('skilltree_skill_required_skills')

        # Adding M2M table for field required_skills on 'SkillLevel'
        db.create_table('skilltree_skilllevel_required_skills', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_skilllevel', models.ForeignKey(orm['skilltree.skilllevel'], null=False)),
            ('to_skilllevel', models.ForeignKey(orm['skilltree.skilllevel'], null=False))
        ))
        db.create_unique('skilltree_skilllevel_required_skills', ['from_skilllevel_id', 'to_skilllevel_id'])

    models = {
        'skilltree.skill': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Skill'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'skills'", 'to': "orm['skilltree.SkillGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rank': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'required_skills': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'enables_skills'", 'symmetrical': 'False', 'to': "orm['skilltree.SkillLevel']"})
        },
        'skilltree.skillgroup': {
            'Meta': {'ordering': "('name',)", 'object_name': 'SkillGroup'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        'skilltree.skilllevel': {
            'Meta': {'ordering': "('skill__name', 'level')", 'object_name': 'SkillLevel'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'skill': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['skilltree.Skill']"})
        }
    }

    complete_apps = ['skilltree']