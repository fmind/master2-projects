# -*- coding: utf-8 -*-

from django.db import models
from django.core import validators
from django.contrib.auth.models import User

name_validator = validators.RegexValidator(r'^[0-9a-zA-Z- ]*$', "Seul les caractères alphanumériques, '-' et des espaces sont admis")


class Wiki(models.Model):
    display_name = models.CharField("Nom d'affichage", max_length=30, unique=True, validators=[name_validator,])
    api_url = models.URLField("URL de l'API")
    date_created = models.DateTimeField("Ajouté le", auto_now_add=True, editable=False)
    date_updated = models.DateTimeField("Modifié le", auto_now=True, editable=False)

    def __unicode__(self):
        return self.display_name

    class Meta:
        verbose_name = u"Wiki"
        verbose_name_plural = u"Wiki"
        ordering = ('display_name',)


class Settings(models.Model):
    VERSION_LIMITS = zip(range(2,11), range(2,11))

    version_limit = models.PositiveIntegerField("Limite du nombre de version", default=10, choices=VERSION_LIMITS)
    default_wiki = models.ForeignKey(Wiki, verbose_name="Wiki utilisé par défaut", blank=True, null=True)
    user = models.OneToOneField(User, verbose_name="Utilisateur", editable=False)

    def __unicode__(self):
        return "Configuration de " + self.user.username

    class Meta:
        verbose_name = u"Configuration"
        verbose_name_plural = u"Configurations"
        ordering = ('user',)


class Article(models.Model):
    OK = 'OK'
    NEW = 'NEW'
    DRAFT = 'DRAFT'
    CONFLICT = 'CONFLICT'

    STATES = (
        (OK, u"OK"),
        (NEW, u"Nouveau"),
        (DRAFT, u"Brouillon"),
        (CONFLICT, u'Conflit'),
    )

    title = models.CharField("Titre", max_length=30, validators=[name_validator,])
    state = models.CharField("État", max_length=10, choices=STATES, default=OK)
    url = models.URLField("URL de l'article", blank=True, editable=False)
    date_created = models.DateTimeField("Ajouté le", auto_now_add=True, editable=False)
    date_updated = models.DateTimeField("Modifié le", auto_now=True, editable=False)
    date_refreshed = models.DateTimeField("Dernière MAJ", null=True, editable=False)
    date_published = models.DateTimeField("Dernière publication", null=True, editable=False)
    user = models.ForeignKey(User, verbose_name="Utilisateur", editable=False)
    wiki = models.ForeignKey(Wiki, verbose_name="Wiki")

    def link(self):
        if self.url:
            return u"""<a href="%s" title="Cliquez pour voir l'article sur le Wiki" target="_blank">%s</a>""" % (self.url, self.title)
        else:
            return self.title
    link.allow_tags = True
    link.short_description = "Lien vers l'article"

    def clean_old_versions(self):
        limit = self.user.settings.version_limit
        versions_to_delete =  Version.objects.filter(article=self.id).order_by('-date_created')[limit:]

        for v in versions_to_delete:
            v.delete()

    @staticmethod
    def exists(title, user):
        return Article.objects.filter(title=title, user=user).exists()

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u"Article"
        verbose_name_plural = u"Articles"
        ordering = ('wiki', 'user', 'state', '-date_updated',)


class Version(models.Model):
    CREATION = 'CRE'
    RESOLUTION = 'RES'
    MODIFICATION = 'MOD'
    IMPORT = 'IMP'
    DOWNLOAD = 'DOW'
    REVIEW = 'REV'
    ORIGINS = (
        (CREATION, u"Création"),
        (RESOLUTION, u'Résolution'),
        (MODIFICATION, u'Modification'),
        (IMPORT, u"Import"),
        (DOWNLOAD, u"Récupération"),
        (REVIEW, u"Reprise"),
    )

    text = models.CharField("Texte", blank=True, max_length=512)
    origin = models.CharField("Origine", max_length=3, choices=ORIGINS)
    counter = models.PositiveIntegerField("Numéro de version", default=1)
    date_created = models.DateTimeField("Ajouté le", auto_now_add=True, editable=False)
    article = models.ForeignKey(Article, verbose_name="Article", editable=False)

    def __unicode__(self):
        return str(self.id)

    class Meta:
        verbose_name = u"Version"
        verbose_name_plural = u"Versions"
        ordering = ('article__user__username', '-date_created',)
