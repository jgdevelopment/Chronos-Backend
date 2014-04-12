from django.contrib import admin
from music.models import TopSong

class TopSongAdmin(admin.ModelAdmin):
	model = TopSong
	list_display = ('date', 'artist', 'song')
	list_filter = ['date']
admin.site.register(TopSong, TopSongAdmin)
