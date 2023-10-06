from django.urls import reverse, resolve
from graphene_django.views import GraphQLView


def test_graphql_url():
    path = reverse("graphql")
    assert isinstance(resolve(path).func.view_class(), GraphQLView)
