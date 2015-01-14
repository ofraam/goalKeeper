# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'StatusUpdate.reporting_caregiver'
        db.alter_column(u'gk_statusupdate', 'reporting_caregiver_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gk.Caregiver'], null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'StatusUpdate.reporting_caregiver'
        raise RuntimeError("Cannot reverse this migration. 'StatusUpdate.reporting_caregiver' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'StatusUpdate.reporting_caregiver'
        db.alter_column(u'gk_statusupdate', 'reporting_caregiver_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gk.Caregiver']))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'gk.action': {
            'Meta': {'object_name': 'Action'},
            'caregiver': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gk.Caregiver']"}),
            'completed': ('django.db.models.fields.BooleanField', [], {}),
            'deadline': ('django.db.models.fields.DateField', [], {}),
            'goal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gk.Goal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'gk.caregiver': {
            'Meta': {'object_name': 'Caregiver'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'gk.goal': {
            'Meta': {'object_name': 'Goal'},
            'active': ('django.db.models.fields.BooleanField', [], {}),
            'caregivers': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['gk.Caregiver']", 'symmetrical': 'False'}),
            'data_type': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'patient': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gk.Patient']"})
        },
        u'gk.patient': {
            'Meta': {'object_name': 'Patient'},
            'age': ('django.db.models.fields.IntegerField', [], {}),
            'caregiver': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['gk.Caregiver']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'gk.statusupdate': {
            'Meta': {'object_name': 'StatusUpdate'},
            'data_value': ('django.db.models.fields.IntegerField', [], {}),
            'goal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gk.Goal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pub_time': ('django.db.models.fields.DateTimeField', [], {}),
            'reporting_caregiver': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gk.Caregiver']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['gk']