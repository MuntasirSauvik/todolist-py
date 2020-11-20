from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
import transaction

from .. import models
