# -*- coding: utf-8 -*-
from django.conf import settings


def antispam_inc(request):
    """ Increases an antispam counter in the user session """
    if settings.ANTISPAM_SESSION in request.session:
        request.session[settings.ANTISPAM_SESSION] += 1
    else:
        request.session[settings.ANTISPAM_SESSION] = 1

    request.session.save()


def antispam_reset(request):
    """ Resets an antispam counter in the user session """
    if settings.ANTISPAM_SESSION in request.session:
        del request.session[settings.ANTISPAM_SESSION]


def get_auth_form(request, with_post=False):
    """ Returns a auth form with or without captcha based on the antispam counter """
    from forms import AuthForm, AuthFormWithCaptcha

    form_class = None

    # select which form to use
    if settings.ANTISPAM_SESSION in request.session and request.session[settings.ANTISPAM_SESSION] == settings.ANTISPAM_LIMIT:
        form_class = AuthFormWithCaptcha
    else:
        form_class = AuthForm

    # add post data or not
    if with_post:
        return form_class(request, request.POST)
    else:
        return form_class()

def can_create_article(request):
    """ Returns true if a user can create a new article """
    from django.conf import settings
    from models import Article

    return (Article.objects.filter(user=request.user).count() < settings.ARTICLES_PER_USER)

def raise404_if_different(o1, o2):
    """ Raises an HTTP 404 if the 2 objects are differents """
    from django.http import Http404

    if o1 != o2:
        raise Http404
