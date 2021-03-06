# django-fav

A simple reusable app for django that makes it easy to deal with faving
and unfaving any object from any application.

It comes with a Graphene (GraphQL) Query to enable favs in your queries.

## Requirements

* Python 3.4+
* Django 1.11


## Installation

```
pip install django-fav
```

* Add the app to your settings.py

```python
INSTALLED_APPS = [
  ...
  "fav",
  ...
]
```

* Sync your database:

```
python manage.py migrate
```


## Usage:


### Favorites Manager

* Create a Favorite instance for a user and object:

```python
>>> from django.contrib.auth.models import User
>>> from music.models import Song
>>> user = User.objects.get(username='gengue')
>>> song = Song.objects.get(pk=1)
>>> fav = Favorite.objects.create(user, song)
```

    or:

```python
>>> fav = Favorite.objects.create(user, 1, Song)
```

    or:

```python
>>> fav = Favorite.objects.create(user, 1, "music.Song")
```

 * Get the objects favorited by a given user:

```python
>>> from django.contrib.auth.models import User
>>> user = User.objects.get(username='gengue')
>>> Favorite.objects.for_user(user)
>>> [<Favorite: Favorite object 1>, <Favorite: Favorite object 2>, <Favorite: Favorite object 3>]
```

* Now, get user favorited objects belonging to a given model:

```python
>>> from django.contrib.auth.models import User
>>> from music.models import Song
>>> user = User.objects.get(username='gengue')
>>> Favorite.objects.for_user(user, model=Song)
>>> [<Favorite: Favorite object 1>, <Favorite: Favorite object 2>, <Favorite: Favorite object 3>]
```

* Get the favorited object instances of a given model favorited by any user:

```python
>>> from music.models import Song
>>> Favorite.objects.for_model(Song)
>>> [<Favorite: Favorite object 1>, <Favorite: Favorite object 2>, <Favorite: Favorite object 3>]
```

* Get a Favorite instance for a given object and user:

```python
>>> from django.contrib.auth.models import User
>>> from music.models import Song
>>> user = User.objects.get(username='gengue')
>>> song = Song.objects.get(pk=1)
>>> fav = Favorite.objects.get_favorite(user, song)
```

* Get all Favorite instances for a given object

```python
>>> from music.models import Song
>>> song = Song.objects.get(pk=1)
>>> fav = Favorite.objects.for_object(song)
```

## Graphql

In `settings.py`, map your grahene queries to your django models

```python
FAV_MODELS = {
    'CurrentUser': 'core.user',
    'User': 'core.user',
    'Track': 'listen.Track',
}
```

Add `url_renditions.graphql_schema.Query` to your root query and mutation.
```python
import graphene
import fav.graphql_schema

class Query(
        ...
        fav.graphql_schema.Query,
        graphene.ObjectType):
    pass

class Mutation(
        ...
        fav.graphql_schema.Mutation,
        graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)

```

### Query

Then, you can ask for:

```graphql
query {
  isInUserFavorites(objectId: "VHJhY2s6OA==")
}
```

and you get

```json
{
  "data": {
    "isInUserFavorites": false
  }
}
```

### Mutation

```graphql
mutation {
  favorite(input: {objectId: "VHJhY2s6OA=="}) {
    deleted
    created
  }
}
```

and you get

```json
{
  "data": {
    "favorite": {
      "deleted": null,
      "created": true,
    }
  }
}
```

## Thanks

* This apps was based on the fork: https://github.com/gengue/django-favs which is based on the fork of https://github.com/streema/django-favit by streema.

