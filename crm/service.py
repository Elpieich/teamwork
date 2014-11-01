# -*- encoding:utf-8 -*-

import werkzeug.exceptions

from functools import wraps
from itertools import chain
from bson import json_util
from flask import request, jsonify, current_app
from flask_security.decorators import auth_token_required

from .core import db

from pprint import pprint 
#pprint(werkzeug.exceptions.__doc__)

#autentificacion
#autorizacion
#permisos

#chequeo de headers
#chequeo de parametros (contenido y cuales)
#manejo de errores
#clean


CONTENT_TYPES = (
    'application/json',)



def route(bp, *args, **kwargs):
    kwargs.setdefault('strict_slashes', False)
    def decorated(fn):
        @bp.route(*args, **kwargs)
        @content_type(*CONTENT_TYPES)
        @auth_token_required
        @wraps(fn)
        def wrapper(*args, **kwargs):
            sc = 200

            try:
                rv = fn(*args, **kwargs)

                if hasattr(rv, 'to_json'):
                    rv = rv.to_json()
                else:
                    rv = json_util.dumps(rv)

            except db.DoesNotExist:
                raise werkzeug.exceptions.ImATeapot
            except db.ValidationError:
                raise werkzeug.exceptions.ImATeapot

            if isinstance(rv, tuple):
                sc = rv[1]
                rv = rv[0]
            return rv, sc
        return wrapper
    return decorated


def content_type(*content_types):
    def decorated(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if request.mimetype not in content_types:
                raise werkzeug.exceptions.UnsupportedMediaType
            return fn(*args, **kwargs)
        return wrapper
    return decorated


def authenticity(fn):
    def decorated(*args, **kwargs):
        return fn(*args, **kwargs)
    return decorated


def output(fn):
    def decorated(*args, **kwargs):
        sc = 200
        rv = fn(*args, **kwargs).to_json()
        if isinstance(rv, tuple):
            sc = rv[1]
            rv = rv[0]
        return jsonify(dict(data=rv)), sc
    return decorated


class Service(object):
    """A :class:`Service` instance encapsulates common MongoEngine model
    operations in the context of a :class:`Flask` application.
    """
    __model__ = None
    __request__ = None

    def __init__(self):
        methods = ('POST', 'UPDATE', 'DELETE', )
        if set(methods) & set([request.method]):
            self.__request__ = request.get_json()

    def _isinstance(self, instance, raise_error=True):
        """Checks if the specified model instance matches the service's model.
        By default this method will raise a `ValueError` if the model is not the
        expected type.

        :param model: the model instance to check
        :param raise_error: flag to raise an error on a mismatch
        """
        if not isinstance(instance, self.__model__) and raise_error:
            raise ValueError('%s is not of type %s' % (instance, self.__model__))
        return True

    def _preprocess_params(self, kwargs):
        """Returns a preprocessed dictionary of parameters. Used by default
        before creating a new instance or updating an existing instance.

        :param kwargs: a dictionary of parameters
        """
        kwargs.pop('csrf_token', None)
        return kwargs

    def save(self, instance):
        """Commits the model to the database and returns the model

        :param model: the model to save
        """
        self._isinstance(instance)
        instance.save()
        return instance

    def all(self):
        """Returns a generator containing all instances of the service's model.
        """
        return self.__model__.objects()

    def get(self, id):
        """Returns an instance of the service's model with the specified id.
        Returns `None` if an instance with the specified id does not exist.

        :param id: the instance id
        """
        return self.__model__.objects.get(id=id)

    def get_all(self, *ids):
        """Returns a list of instances of the service's model with the specified
        ids.

        :param *ids: instance ids
        """
        return self.__model__.objects.filter(self.__model__.id.in_(ids)).all()

    def find(self, **kwargs):
        """Returns a list of instances of the service's model filtered by the
        specified key word arguments.

        :param **kwargs: filter parameters
        """
        return self.__model__.objects.filter(**kwargs)

    def first(self, **kwargs):
        """Returns the first instance found of the service's model filtered by
        the specified key word arguments.

        :param **kwargs: filter parameters
        """
        return self.__model__.objects.find(**kwargs).first()

    def get_or_404(self, id):
        """Returns an instance of the service's model with the specified id or
        raises an 404 error if an instance with the specified id does not exist.

        :param id: the instance id
        """
        return self.__model__.query.get_or_404(id)

    def new(self, **kwargs):
        """Returns a new, unsaved instance of the service's model class.

        :param **kwargs: instance parameters
        """
        return self.__model__(**kwargs)

    def create(self, **kwargs):
        """Returns a new, saved instance of the service's model class.

        :param **kwargs: instance parameters
        """

        parameters = dict(chain(self.__request__.items(), kwargs.items()))
        instance = self.new(**parameters)
        return self.save(instance)

    def update(self, id, **kwargs):
        """Returns an updated instance of the service's model class.

        :param model: the model to update
        :param **kwargs: update parameters
        """
        parameters = dict(chain(self.__request__.items(), kwargs.items()))
        instance = self.get(id=id)
        self._isinstance(instance)
        for field, value in self._preprocess_params(**parameters).items():
            setattr(instance, field, value)
        return self.save(instance)

    def delete(self, id):
        """Immediately deletes the specified model instance.

        :param model: the model instance to delete
        """
        instance = self.get(id)
        self._isinstance(instance)
        return instance.delete()
