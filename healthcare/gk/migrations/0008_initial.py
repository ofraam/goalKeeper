# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Caregiver'
        db.create_table(u'gk_caregiver', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal(u'gk', ['Caregiver'])

        # Adding model 'Patient'
        db.create_table(u'gk_patient', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'gk', ['Patient'])

        # Adding M2M table for field caregiver on 'Patient'
        m2m_table_name = db.shorten_name(u'gk_patient_caregiver')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('patient', models.ForeignKey(orm[u'gk.patient'], null=False)),
            ('caregiver', models.ForeignKey(orm[u'gk.caregiver'], null=False))
        ))
        db.create_unique(m2m_table_name, ['patient_id', 'caregiver_id'])

        # Adding model 'Goal'
        db.create_table(u'gk_goal', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('caregiver', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gk.Caregiver'])),
            ('patient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gk.Patient'])),
            ('notes', self.gf('django.db.models.fields.TextField')()),
            ('active', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'gk', ['Goal'])

        # Adding model 'StatusUpdate'
        db.create_table(u'gk_statusupdate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('goal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gk.Goal'])),
            ('time', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('data_value', self.gf('django.db.models.fields.IntegerField')()),
            ('reporting_caregiver', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gk.Caregiver'])),
            ('notes', self.gf('django.db.models.fields.TextField')()),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'gk', ['StatusUpdate'])

        # Adding model 'Action'
        db.create_table(u'gk_action', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('goal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gk.Goal'])),
            ('completed', self.gf('django.db.models.fields.BooleanField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('notes', self.gf('django.db.models.fields.TextField')()),
            ('caregiver', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gk.Caregiver'])),
            ('deadline', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'gk', ['Action'])


    def backwards(self, orm):
        # Deleting model 'Caregiver'
        db.delete_table(u'gk_caregiver')

        # Deleting model 'Patient'
        db.delete_table(u'gk_patient')

        # Removing M2M table for field caregiver on 'Patient'
        db.delete_table(db.shorten_name(u'gk_patient_caregiver'))

        # Deleting model 'Goal'
        db.delete_table(u'gk_goal')

        # Deleting model 'StatusUpdate'
        db.delete_table(u'gk_statusupdate')

        # Deleting model 'Action'
        db.delete_table(u'gk_action')


    models = {
        u'gk.action': {
            'Meta': {'object_name': 'Action'},
            'caregiver': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gk.Caregiver']"}),
            'completed': ('django.db.models.fields.BooleanField', [], {}),
            'deadline': ('django.db.models.fields.DateField', [], {}),
            'goal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gk.Goal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'notes': ('django.db.models.fields.TextField', [], {})
        },
        u'gk.caregiver': {
            'Meta': {'object_name': 'Caregiver'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'gk.goal': {
            'Meta': {'object_name': 'Goal'},
            'active': ('django.db.models.fields.BooleanField', [], {}),
            'caregiver': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gk.Caregiver']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'patient': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gk.Patient']"})
        },
        u'gk.patient': {
            'Meta': {'object_name': 'Patient'},
            'caregiver': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['gk.Caregiver']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'gk.statusupdate': {
            'Meta': {'object_name': 'StatusUpdate'},
            'data_value': ('django.db.models.fields.IntegerField', [], {}),
            'goal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gk.Goal']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'reporting_caregiver': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['gk.Caregiver']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'time': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['gk']