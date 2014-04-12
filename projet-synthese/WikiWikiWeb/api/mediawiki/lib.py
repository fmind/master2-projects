# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
from ConfigParser import ConfigParser
from errors import *
import hashlib
import urllib2
import urllib
import os


class APIRequest:
    ''' Création d'une requête utilisant l'API REST de Mediawiki '''

    def __init__(self, api_url):
        ''' Initialise la requête avec l'adresse de l'API '''
        self.api_url = api_url
        self._opener = urllib2.build_opener(urllib2.HTTPRedirectHandler(), urllib2.HTTPCookieProcessor)

    @staticmethod
    def normalize(title):
        ''' Adapte le titre d'un article pour être comptabile avec l'API '''
        return title.lower().capitalize().replace('_', ' ').strip()

    @staticmethod
    def wiki_error_handler(xml):
        ''' Retourne une erreur contenue dans un retour XML '''
        for error in xml.findall('error'):
            code = error.attrib['code']
            info = error.attrib['info']
            raise APIException("%s => %s" % (code, info), APIException.API_ERROR)
        for warning in xml.findall('warning'):
            code = warning.attrib['code']
            info = warning.attrib['info']
            raise APIException("%s => %s" % (code, info), APIException.API_WARNING)

    def search(self, title):
        ''' Retourne des suggestions d'article basé sur leur titre {title: {title:, description:, url:}, ...} '''
        result = []
        parameters = {}
        parameters['action'] = 'opensearch'
        parameters['format'] = 'xml'
        parameters['namespace'] = 0
        parameters['search'] = APIRequest.normalize(title)
        namespace = ' xmlns="http://opensearch.org/searchsuggest2"'

        response = self.__POST(parameters).replace(namespace, '')
        xml = ET.fromstring(response)

        APIRequest.wiki_error_handler(xml)

        for item in xml.iter('Item'):
            title = item.find('Text').text
            description = item.find('Description').text
            url = item.find('Url').text
            suggestion = {'title': title, 'description': description, 'url': url}
            result.append(suggestion)

        return result

    def getArticleTimestamp(self, title):
        ''' Retourne le timestamp d'un article '''
        from datetime import datetime
        from dateutil import tz

        parameters = {}
        parameters['action'] = 'query'
        parameters['prop'] = 'revisions'
        parameters['rvprop'] = 'timestamp'
        parameters['format'] = 'xml'
        parameters['titles'] = APIRequest.normalize(title)

        response = self.__POST(parameters)
        xml = ET.fromstring(response)

        APIRequest.wiki_error_handler(xml)

        result = xml.find('query/pages/page/revisions/rev').attrib['timestamp']
        utc = datetime.strptime(result, '%Y-%m-%dT%H:%M:%SZ')
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        local = utc.replace(tzinfo=from_zone)
        timestamp = local.astimezone(to_zone)

        return timestamp

    def getArticleContent(self, title):
        ''' Retourne le contenu d'un article '''
        parameters = {}
        parameters['action'] = 'parse'
        parameters['prop'] = 'text'
        parameters['disablepp'] = 1
        parameters['format'] = "xml"
        parameters['page'] = APIRequest.normalize(title)

        response = self.__POST(parameters)
        xml = ET.fromstring(response)

        APIRequest.wiki_error_handler(xml)

        text = xml.find('parse/text').text

        return text

    def getArticleUrl(self, title):
        ''' Retourne l'URL d'un article '''
        parameters = {}
        parameters['action'] = 'query'
        parameters['prop'] = 'info'
        parameters['inprop'] = 'url'
        parameters['format'] = 'xml'
        parameters['titles'] = APIRequest.normalize(title)

        response = self.__POST(parameters)
        xml = ET.fromstring(response)

        APIRequest.wiki_error_handler(xml)

        if 'missing' in xml.find('query/pages/page').attrib.keys():
            return None

        url = xml.find('query/pages/page').attrib['fullurl']

        return url

    def publish(self, title, content, last_timestamp):
        ''' Publie le contenu d'un article sur le Wiki '''
        from datetime import datetime
        from dateutil import tz

        token = self.getToken(title, 'edit', True)

        parameters = {}
        parameters['action'] = 'edit'
        parameters['md5'] = hashlib.md5(content.encode('utf-8')).hexdigest()
        parameters['summary'] = 'Edited with WikiWikiWeb'
        parameters['token'] = token
        parameters['format'] = 'xml'
        parameters['bot'] = 1
        parameters['title'] = self.normalize(title)
        if last_timestamp:
            from_zone = tz.tzlocal()
            to_zone = tz.tzutc()
            last_timestamp = last_timestamp.replace(tzinfo=from_zone)
            utc = last_timestamp.astimezone(to_zone)
            parameters['basetimestamp'] = datetime.strftime(utc, '%Y-%m-%dT%H:%M:%SZ')
        parameters['text'] = content.encode('utf-8')

        response = self.__POST(parameters)
        xml = ET.fromstring(response)

        # détection de conflit
        try:
            APIRequest.wiki_error_handler(xml)
        except APIException as e:
            if 'editconflict' in e.message:
                return -2
            else:
                raise e

        self.__logout()

        result = xml.find('edit')
        if result.attrib['result'] == 'Success':
            if 'nochange' in result.attrib:
                return 0
            elif 'oldrevid' in result.attrib and result.attrib['oldrevid'] != '0':
                return 1
            elif 'oldrevid' in result.attrib and result.attrib['oldrevid'] == '0':
                return 2
            else:
                return -1

        else:
            return -1

    #def delete(self, title):
        #''' Supprime un article sur le Wiki '''
        #token = self.getToken(title, 'delete', True)

        #parameters = {}
        #parameters['format'] = 'xml'
        #parameters['action'] = 'delete'
        #parameters['title'] = self.normalize(title)
        #parameters['token'] = token

        #response = self.__POST(parameters)
        #xml = ET.fromstring(response)

        #APIRequest.wiki_error_handler(xml)
        #self.__logout()

    def getToken(self, title, type, login=False, logout=False):
        ''' Récupère un token pour une action en 2 étapes '''

        if login:
            self.__login()

        parameters = {}
        parameters['action'] = 'query'
        parameters['prop'] = 'info|revisions'
        parameters['format'] = 'xml'
        parameters['intoken'] = type
        parameters['titles'] = APIRequest.normalize(title)

        response = self.__POST(parameters)
        xml = ET.fromstring(response)

        APIRequest.wiki_error_handler(xml)

        token = xml.find('query/pages/page').attrib['edittoken']

        if logout:
            self.__logout()

        return token

    def __login(self):
        ''' Connecte l'utilisateur sur le Wiki '''
        parameters = {}
        parameters['action'] = 'login'
        parameters['format'] = 'xml'
        parameters['lgname'] = self.__getConfig().get('Credentials', 'username')
        parameters['lgpassword'] = self.__getConfig().get('Credentials', 'password')

        response = self.__POST(parameters)
        xml = ET.fromstring(response)

        if xml.find('login').attrib['result'] == 'NeedToken':
            parameters['lgtoken'] = xml.find('login').attrib['token']
            response = self.__POST(parameters)
            xml = ET.fromstring(response)

        if xml.find('login').attrib['result'] != 'Success':
            result = xml.find('login').attrib['result']
            raise APIException(result, APIException.API_LOGIN_ERROR)
        else:
            return True

    def __logout(self):
        ''' Déconnecte l'utilisateur après requête '''
        parameters = {}
        parameters['format'] = 'xml'
        parameters['action'] = 'logout'

        self.__POST(parameters)

    def __getConfig(self):
        ''' Retourne le gestionnaire de configuration '''
        if not hasattr(self, 'config'):
            pwd = os.path.dirname(os.path.abspath(__file__))
            self.config = ConfigParser()
            self.config.read(os.path.join(pwd, 'client.ini'))

        return self.config

    def __POST(self, parameters):
        ''' POST HTTP '''
        try:
            # TODO: remove split('<html>')
            return self._opener.open(self.api_url, urllib.urlencode(parameters)).read().split('<html>')[0]
        except Exception as e:
            raise APIException("%s => %s" % (e.__class__.__name__, e), APIException.NETWORK_ERROR)
