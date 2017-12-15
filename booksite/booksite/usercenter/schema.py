# -*- coding: utf-8 -*-
from graphene import relay, AbstractType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import BookMark, User


class BookMarkNode(DjangoObjectType):
    class Meta:
        model = BookMark
        interfaces = (relay.Node, )
        filter_fields = {
            'user': ['exact'],
        }


class UserNode(DjangoObjectType):
    """
    User Node
    """
    class Meta:
        model = User
        filter_fields = {
            'email': ['exact', ]
        }
        exclude_fields = ('password', 'is_superuser', )
        interfaces = (relay.Node, )


class Query(AbstractType):
    # bookmark = relay.Node.Field(BookMarkNode)
    all_bookmarks = DjangoFilterConnectionField(BookMarkNode)

    user = relay.Node.Field(UserNode)
