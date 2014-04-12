# -*- coding: utf-8 -*-

from lib import APIRequest
from errors import APIException


def get_article_timestamp(url, title):
    ''' Retourne le timestamp d'un article '''
    return APIRequest(url).getArticleTimestamp(title)


def get_article_content(url, title):
    ''' Retourne le contenu d'un article '''
    return APIRequest(url).getArticleContent(title)


def get_article_url(url, title):
    ''' Retourne l'URL d'un article '''
    return APIRequest(url).getArticleUrl(title)


def search(url, title):
    ''' Retourne une liste de suggestion basée sur le titre d'un article (10 max) '''
    return APIRequest(url).search(title)


def publish(url, title, content, last_timestamp=None):
    ''' Publie une nouvelle version sur le Wiki (création ou modification '''
    return APIRequest(url).publish(title, content, last_timestamp)
