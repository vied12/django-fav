import graphene
from .models import Favorite as FavoriteModel
from graphql_relay.node.node import from_global_id
from django.apps import apps
from graphql_schema import Query


FIELDS = [f for f in  Query._meta.fields.values() if hasattr(f._type, '_meta') and hasattr(f.type._meta, 'model')]
MAP_MODELS = {f._type._meta.name: '{}.{}'.format(f.type._meta.model._meta.app_label, f.type._meta.model._meta.model_name) for f in FIELDS}
# MAP_MODELS = {
#     'CurrentUser': 'core.user',
#     'User': 'core.user',
# }


class Query(object):
    is_in_user_favorites = graphene.Boolean(
        description='If the given object is favorited by the current user',
        object_id=graphene.ID(),
    )

    def resolve_is_in_user_favorites(self, info, object_id):
        model, obj = from_global_id(object_id)
        if not info.context.user.is_authenticated:
            return False
        fav = dict(user=info.context.user, obj=int(obj), model=MAP_MODELS[model])
        existing = FavoriteModel.objects.get_favorite(**fav)
        return existing is not None


class FavoriteMutation(graphene.relay.ClientIDMutation):

    class Input:
        object_id = graphene.ID()

    deleted = graphene.Boolean(default_value=True)
    created = graphene.Boolean(default_value=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        assert info.context.user.is_authenticated
        model, obj = from_global_id(input['object_id'])
        fav = dict(user=info.context.user, obj=int(obj), model=MAP_MODELS[model])
        existing = FavoriteModel.objects.get_favorite(**fav)
        if existing:
            existing.delete()
            return FavoriteMutation(deleted=True)
        else:
            FavoriteModel.objects.create(**fav)
            return FavoriteMutation(created=True)


class Mutation(object):
    favorite = FavoriteMutation.Field()
