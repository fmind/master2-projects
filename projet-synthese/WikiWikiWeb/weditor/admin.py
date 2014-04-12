from django.contrib import admin
from models import Wiki, Settings, Article, Version


class WikiAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'date_updated', 'date_created',)
    list_filter = ('date_created',)

admin.site.register(Wiki, WikiAdmin)


class SettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'default_wiki', 'version_limit',)

    def has_add_permission(self, request):
        return False

admin.site.register(Settings, SettingsAdmin)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('wiki', 'user', 'link', 'state', 'date_refreshed', 'date_published', 'date_updated', 'date_created')
    list_filter = ('state', 'user', 'wiki', 'date_updated',)
    exclude = ('wiki',)

    def has_add_permission(self, request):
        return False

admin.site.register(Article, ArticleAdmin)


class VersionAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'article', 'origin', 'counter', 'date_created',)
    list_filter = ('article', 'origin', 'date_created',)

    def username(self, obj):
        return obj.article.user.username

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        return False

admin.site.register(Version, VersionAdmin)
