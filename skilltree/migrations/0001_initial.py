# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SkillGroup'
        db.create_table('skilltree_skillgroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
        ))
        db.send_create_signal('skilltree', ['SkillGroup'])

        # Adding model 'Skill'
        db.create_table('skilltree_skill', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('rank', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(related_name='skills', to=orm['skilltree.SkillGroup'])),
        ))
        db.send_create_signal('skilltree', ['Skill'])

        # Adding model 'SkillLevel'
        db.create_table('skilltree_skilllevel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('skill', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['skilltree.Skill'])),
            ('level', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('skilltree', ['SkillLevel'])

        # Adding M2M table for field required_skills on 'SkillLevel'
        db.create_table('skilltree_skilllevel_required_skills', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_skilllevel', models.ForeignKey(orm['skilltree.skilllevel'], null=False)),
            ('to_skilllevel', models.ForeignKey(orm['skilltree.skilllevel'], null=False))
        ))
        db.create_unique('skilltree_skilllevel_required_skills', ['from_skilllevel_id', 'to_skilllevel_id'])

    def backwards(self, orm):
        # Deleting model 'SkillGroup'
        db.delete_table('skilltree_skillgroup')

        # Deleting model 'Skill'
        db.delete_table('skilltree_skill')

        # Deleting model 'SkillLevel'
        db.delete_table('skilltree_skilllevel')

        # Removing M2M table for field required_skills on 'SkillLevel'
        db.delete_table('skilltree_skilllevel_required_skills')

    models = {
        'skilltree.skill': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'Skill'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'skills'", 'to': "orm['skilltree.SkillGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rank': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'skilltree.skillgroup': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'SkillGroup'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        'skilltree.skilllevel': {
            'Meta': {'ordering': "('-modified', '-created')", 'object_name': 'SkillLevel'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'required_skills': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'enabled_skills'", 'symmetrical': 'False', 'to': "orm['skilltree.SkillLevel']"}),
            'skill': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['skilltree.Skill']"})
        }
    }

    complete_apps = ['skilltree']