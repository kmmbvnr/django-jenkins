from south.v2 import SchemaMigration

class Migration(SchemaMigration):
    def forwards(self, orm):
        a = 1 # pyflakes/pylint violation
        pass

    def backwards(self, orm):
        pass
