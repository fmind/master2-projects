# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from django.contrib import messages
from django.http import Http404
from api.mediawiki.errors import APIException
from addons import raise404_if_different
import logging

logger = logging.getLogger('weditor')

def index(request):
    from forms import AuthForm

    # redirect to home if already log in
    if request.user.is_authenticated():
        return redirect('home')

    return render_to_response('pages/index.html', context_instance=RequestContext(request))


@login_required
def home(request):
    from django.conf import settings
    from models import Wiki, Article
    from addons import can_create_article

    wikis = Wiki.objects.all()
    articles = Article.objects.filter(user=request.user)

    return render_to_response('pages/home.html',
                              {'wikis': wikis, 'articles': articles,
                               'can_create_article': can_create_article(request),
                               'limit_create': settings.ARTICLES_PER_USER},
                              context_instance=RequestContext(request))


@login_required
def search(request):
    from django.conf import settings
    from api.mediawiki.requests import search
    from models import Article, Wiki
    from addons import can_create_article

    if not can_create_article(request):
        messages.warning(request, "Vous ne pouvez pas gérer plus de %d articles sur WikiWikiWeb!" % settings.ARTICLES_PER_USER)
        return redirect('home')

    if request.method == 'GET':
        get = request.GET.dict()

        if 'q' in get.keys() and len(get['q']):
            get['q'] = get['q'][0:50]

            if not 'wiki' in get:
                messages.warning(request, "Le wiki n'a pas été précisé dans les critères de recherche. Veuillez recommencer.")
                return redirect('home')

            wiki = get_object_or_404(Wiki, pk=get['wiki'])

            try:
                results = search(wiki.api_url, get['q'])
            except APIException as e:
                messages.warning(request, "Erreur de communication avec l'API. L'administrateur a été averti.")
                logger.error('%s (action=search)' % e)
                return redirect('home')

            cached_request = get
            cached_request['wiki'] = wiki
            cached_request['results'] = results
            request.session[settings.SEARCH_SESSION] = cached_request
        else:
            if not settings.SEARCH_SESSION in request.session:
                messages.warning(request, "Vous n'avez lancé aucune recherche")
                return redirect('home')

    query = request.session[settings.SEARCH_SESSION]

    return render_to_response('pages/search.html', {'query': query}, context_instance=RequestContext(request))


@login_required
def link(request, id):
    from django.conf import settings
    from models import Article, Version
    from api.mediawiki.requests import get_article_content
    from datetime import datetime

    if settings.SEARCH_SESSION not in request.session.keys():
        messages.warning(request, "Vous n'avez lancé aucune recherche")
        return redirect('home')

    if Article.objects.filter(user=request.user).count() >= settings.ARTICLES_PER_USER:
        messages.warning(request, "Vous ne pouvez pas gérer plus de %d articles sur WikiWikiWeb!" % settings.ARTICLES_PER_USER)
        return redirect('home')

    try:
        id = int(id)
        wiki = request.session[settings.SEARCH_SESSION]['wiki']
        wiki_article = request.session[settings.SEARCH_SESSION]['results'][id]
    except (ValueError, IndexError):
        messages.warning(request, "Impossible de retrouver l'article parmis vos résultats de recherche")
        return redirect('search')

    if Article.exists(wiki_article['title'], request.user):
        messages.warning(request, "L'article a déjà été crée ou importé")
        return redirect('search')

    try:
        content = get_article_content(wiki.api_url, wiki_article['title'])
    except APIException as e:
        messages.warning(request, "Erreur de communication avec l'API. L'administrateur a été averti.")
        logger.error('%s (action=link)' % e)
        return redirect('search')

    if len(content) > 512:
        messages.warning(request, "L'article fait plus de 512 caractères (%d), il ne peut pas être importé." % len(content))
        return redirect('search')

    article = Article.objects.create(
        title=wiki_article['title'],
        state=Article.OK,
        url=wiki_article['url'],
        user=request.user,
        wiki=wiki,
        date_refreshed=datetime.now()
    )
    Version.objects.create(
        origin=Version.IMPORT,
        text=content,
        article=article
    )

    messages.success(request, "L'article a bien été ajouté à votre interface")

    return redirect('home')


@login_required
def create(request):
    from django.conf import settings
    from forms import CreateArticleForm
    from models import Article, Version
    from addons import can_create_article

    # limit the number of article
    if not can_create_article(request):
        messages.warning(request, "Vous ne pouvez pas gérer plus de %d articles sur WikiWikiWeb !" % settings.ARTICLES_PER_USER)
        return redirect('home')

    if request.method == 'POST':
        create_form = CreateArticleForm(request.POST)
        create_form.instance.user = request.user
        create_form.instance.state = Article.NEW

        if create_form.is_valid():
            if Article.exists(create_form.instance.title, request.user):
                messages.warning(request, "Un article du même nom a déjà été crée/importé dans votre interface")
            else:
                if len(create_form.cleaned_data['text']) > 512:
                    messages.warning(request, "L'article fait plus de 512 caractères (%d), il ne peut pas être crée." % len(create_form.cleaned_data['text']))
                else:
                    article = create_form.save()
                    Version.objects.create(origin=Version.CREATION, text=create_form.cleaned_data['text'], article=article)
                    return redirect('home')
    else:
        create_form = CreateArticleForm()
        create_form.fields['wiki'].initial = request.user.settings.default_wiki

    return render_to_response('pages/create.html', {'create_form': create_form},
                              context_instance=RequestContext(request))


@login_required
def edit(request, article_id):
    from forms import EditArticleForm
    from models import Article, Version
    from datetime import datetime

    if request.method == 'POST' and 'publish' in request.POST.keys():
        return publish(request, article_id)
    elif request.method == 'POST' and 'refresh' in request.POST.keys():
        return refresh(request, article_id)
    elif request.method == 'POST' and 'save' not in request.POST.keys():
        messages.warning(request, u"Action de modification inconnue")
        return redirect('edit', article_id)

    article = get_object_or_404(Article, pk=article_id)
    raise404_if_different(article.user, request.user)
    versions = Version.objects.filter(article=article).all()

    if len(versions) < 1:
        messages.warning(request, u"L'article \"%s\" n'est pas versionné." % (article.title,))
        logger.error("Article non versionné: %s" % article_id)
        return redirect('home')

    last_version = versions[0]
    history = versions[1:]

    if request.method == 'POST':
        edit_form = EditArticleForm(request.POST, instance=article)
        origin = Version.MODIFICATION
        if edit_form.instance.state == Article.CONFLICT:
            edit_form.instance.date_refreshed = datetime.now()
            origin = Version.RESOLUTION
        if article.state != Article.NEW:
            edit_form.instance.state = Article.DRAFT

        if edit_form.is_valid():
            if len(edit_form.cleaned_data['text']) > 512:
                messages.warning(request, "L'article fait plus de 512 caractères (%d), il ne peut pas être modifié." % len(edit_form.cleaned_data['text']))
            else:
                article = edit_form.save()
                version = Version.objects.create(
                    counter=last_version.counter+1,
                    origin=origin,
                    text=edit_form.cleaned_data['text'],
                    article=article
                )
                article.clean_old_versions()
                messages.success(request, u"L'article \"%s\" a bien été modifié ! (#%s)" % (article.title, version.counter))

                return redirect('edit', article_id)
    else:
        edit_form = EditArticleForm(instance=article, initial={'text': last_version.text,})

    # retrieve the last Wiki article on conflict
    last_wiki_version = None
    if article.state == Article.CONFLICT:
        from api.mediawiki.requests import get_article_content
        try:
            last_wiki_version = get_article_content(article.wiki.api_url, article.title)
        except APIException as e:
            messages.warning(request, "Erreur de communication avec l'API. L'administrateur a été averti.")
            logger.error('%s (action=edit)' % e)
            return redirect('edit', article_id)

    return render_to_response('pages/edit.html', {'edit_form': edit_form,
                                                  'article': article,
                                                  'last_wiki_version': last_wiki_version,
                                                  'history': history,},
                              context_instance=RequestContext(request))


@login_required
def review(request, article_id, version_id):
    from models import Article, Version
    from datetime import datetime

    article = get_object_or_404(Article, pk=article_id)
    version = get_object_or_404(Version, pk=version_id)
    last_version = Version.objects.filter(article=article).latest('date_created')

    raise404_if_different(article.user, request.user)
    raise404_if_different(version.article, article)

    if len(version.text) > 512:
        messages.warning(request, "L'article fait plus de 512 caractères (%d), il ne peut pas être rejoué." % len(version.text))

        return redirect('edit', article_id)

    review_version = Version.objects.create(origin=Version.REVIEW, counter=last_version.counter+1, text=version.text, article=article)
    article.clean_old_versions()

    if article.state == Article.CONFLICT:
        article.state = Article.DRAFT
        article.date_refreshed = datetime.now()
        article.save()

    messages.success(request, u"La version #%s de l'article a été rechargé !" % version.counter)

    return redirect('edit', article_id)

@login_required
def refresh(request, article_id):
    from django.utils import formats
    from api.mediawiki.requests import get_article_content, get_article_timestamp
    from models import Article, Version
    from datetime import datetime

    article = get_object_or_404(Article, pk=article_id)
    raise404_if_different(article.user, request.user)

    if article.state != Article.DRAFT and article.state != Article.CONFLICT:
        messages.warning(request, u"Vous ne pouvez récupérer qu'un article que dans l'état 'Brouillon' ou 'Conflit'")
        return redirect('edit', article_id)

    try:
        content = get_article_content(article.wiki.api_url, article.title)
        timestamp = get_article_timestamp(article.wiki.api_url, article.title)
    except APIException as e:
        messages.warning(request, "Erreur de communication avec l'API. L'administrateur a été averti.")
        logger.error('%s (action=refresh)' % e)
        return redirect('edit', article_id)

    if len(content) > 512:
        messages.warning(request, "L'article fait plus de 512 caractères (%d), il ne peut pas être téléchargé." % len(content))

        return redirect('edit', article_id)

    dt = formats.date_format(timestamp, "DATETIME_FORMAT")

    article.state = Article.OK
    article.date_refreshed = datetime.now()
    article.save()

    last_version = Version.objects.filter(article=article).all()[0]

    version = Version.objects.create(
        counter=last_version.counter+1,
        origin=Version.DOWNLOAD,
        text=content,
        article=article
    )
    article.clean_old_versions()

    messages.success(request, u"Vous avez récupéré la dernière version du Wiki (%s)" % (dt))

    return redirect('edit', article_id)


@login_required
def publish(request, article_id):
    from api.mediawiki.requests import publish, get_article_url
    from models import Article, Version
    from datetime import datetime

    article = get_object_or_404(Article, pk=article_id)
    raise404_if_different(article.user, request.user)

    # only for draft and new state
    if article.state != Article.DRAFT and article.state != Article.NEW:
        messages.warning(request, u"L'article n'a pas été modifié")
        return redirect('edit', article_id)

    last_version = Version.objects.filter(article=article).all()[0]

    try:
        last_timestamp = article.date_refreshed if article.date_refreshed else article.date_created
        result = publish(article.wiki.api_url, article.title, last_version.text, last_timestamp)
    except APIException as e:
        messages.warning(request, "Erreur de communication avec l'API. L'administrateur a été averti.")
        logger.error('%s (action=publish)' % e)
        return redirect('edit', article_id)

    # user message
    if result == 0:
        act = u'aucun changement'
    elif result == 1:
        act = u'modification'
    elif result == 2:
        act = u'création'
    elif result == -2:
        messages.error(request, "Conflit détécté ! Vous devez le résoudre avant de poursuivre la publication")
        article.state = Article.CONFLICT
        article.save()
        return redirect('edit', article_id)

    # retrieve the URL if necessary
    if not len(article.url):
        try:
            url = get_article_url(article.wiki.api_url, article.title)
            if url is not None:
                article.url = url
        except APIException as e:
            messages.warning(request, "Erreur de communication avec l'API. L'administrateur a été averti.")
            logger.error('%s (action=get_article_url)' % e)
            return redirect('edit', article_id)

    article.state = Article.OK
    article.date_published = datetime.now()
    article.date_refreshed = article.date_published
    messages.success(request, u"L'article a été envoyé avec succès ! (%s)" % act)
    article.save()

    return redirect('edit', article_id)


@login_required
def delete(request, id):
    from models import Article

    article = get_object_or_404(Article, pk=id)
    raise404_if_different(article.user, request.user)
    article.delete()
    messages.success(request, u"L'article \"%s\" a bien été supprimé !" % article.title)

    return redirect('home')


@login_required
def profile(request):
    from forms import ProfileForm

    if request.method == 'POST':
        profile_form = ProfileForm(request.user, request.POST)

        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, u"Vos informations ont bien été modifiées !")
    else:
        profile_form = ProfileForm(request.user)

    return render_to_response('pages/profile.html', {'profile_form': profile_form},
                              context_instance=RequestContext(request))


@login_required()
def settings(request):
    from forms import SettingsForm

    if request.method == 'POST':
        settings_form = SettingsForm(request.POST, instance=request.user.settings)

        if settings_form.is_valid():
            settings_form.save()
            messages.success(request, u"Vos préférences ont bien été modifiées !")
    else:
        settings_form = SettingsForm(instance=request.user.settings)

    return render_to_response('pages/settings.html', {'settings_form': settings_form},
                              context_instance=RequestContext(request))


def subscribe(request):
    from forms import SubscribeForm
    from models import Settings

    # redirect to home if already log in
    if request.user.is_authenticated():
        return redirect('home')

    if request.method == 'POST':
        subscribe_form = SubscribeForm(request.POST)

        if subscribe_form.is_valid():
            user = subscribe_form.save()
            my_settings = Settings.objects.create(user=user)
            messages.success(request, u"Votre compte a bien été crée !")
    else:
        subscribe_form = SubscribeForm()

    return render_to_response('pages/subscribe.html', {'subscribe_form': subscribe_form},
                              context_instance=RequestContext(request))


def login(request):
    from django.contrib.auth import authenticate, login
    from addons import antispam_inc, antispam_reset, get_auth_form
    from django.conf import settings
    from forms import AuthForm

    # redirect to home if he is already log in
    if request.user.is_authenticated():
        return redirect('home')

    if request.method == 'POST':
        auth_form = get_auth_form(request, with_post=True)

        if auth_form.is_valid():
            username = auth_form.cleaned_data['username']
            password = auth_form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None and user.is_active:
                login(request, user)
                antispam_reset(request)

                return redirect('home')
            else:
                antispam_inc(request)
        else:
            antispam_inc(request)

        # create a new form (borderline case, must be after validation)
        if request.session[settings.ANTISPAM_SESSION] == settings.ANTISPAM_LIMIT:
            auth_form = get_auth_form(request)

    else:
        auth_form = get_auth_form(request)

    return render_to_response('pages/login.html', {'auth_form': auth_form},
                              context_instance=RequestContext(request))


@login_required
def logout(request):
    from django.contrib.auth import logout

    logout(request)

    return redirect('index')
