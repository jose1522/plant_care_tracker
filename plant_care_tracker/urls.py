from django.urls import re_path
from graphene_django.views import GraphQLView

urlpatterns = [
    re_path(r"^graphql/?$", GraphQLView.as_view(graphiql=True), name="graphql"),
]
