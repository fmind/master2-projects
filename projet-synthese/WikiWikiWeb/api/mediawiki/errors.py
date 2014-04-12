# -*- coding: utf-8 -*-

class APIException(Exception):
    ''' Classe d'exception personnalisée ajoutant un code d'erreur '''
    NETWORK_ERROR       = 10
    API_ERROR           = 20
    API_WARNING         = 20
    API_LOGIN_ERROR     = 30

    def __init__(self, message, code):
        Exception.__init__(self, message)
        self.code = code

    def __str__(self):
        return "APIException[%d]: %s" % (self.code, self.message)

    def __unicode__(self):
        return unicode(self.__str__)
