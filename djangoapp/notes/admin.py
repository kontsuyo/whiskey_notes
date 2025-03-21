from django.contrib import admin

from notes.models import TastingNote, Whisky

admin.site.register(Whisky)
admin.site.register(TastingNote)
