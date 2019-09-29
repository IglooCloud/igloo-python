
from aiodataloader import DataLoader
from igloo.models.utils import wrapWith


class CategorySeriesVariableLoader(DataLoader):
    def __init__(self, client, id):
        super().__init__()
        self.client = client
        self._id = id

    async def batch_load_fn(self, keys):
        fields = " ".join(set(keys))
        res = await self.client.query('{categorySeriesVariable(id:"%s"){%s}}' % (self._id, fields), keys=["categorySeriesVariable"])

        # if fetching object the key will be the first part of the field
        # e.g. when fetching thing{id} the result is in the thing key
        resolvedValues = [res[key.split("{")[0]] for key in keys]

        return resolvedValues


class CategorySeriesVariable:
    def __init__(self, client, id):
        self.client = client
        self._id = id
        self.loader = CategorySeriesVariableLoader(client, id)

    @property
    def id(self):
        return self._id

    @property
    def lastNode(self):
        if self.client.asyncio:
            res = self.loader.load("lastNode{id}")
        else:
            res = self.client.query('{categorySeriesVariable(id:"%s"){lastNode{id}}}' % self._id, keys=[
                "categorySeriesVariable", "lastNode"])

        def wrapper(res):
            from .category_series_node import CategorySeriesNode
            return CategorySeriesNode(self.client, res["id"])

        return wrapWith(res, wrapper)

    @property
    def nodes(self):
        from .category_series_node import CategorySeriesNodeList
        return CategorySeriesNodeList(self.client, self.id)

    @property
    def name(self):
        if self.client.asyncio:
            return self.loader.load("name")
        else:
            return self.client.query('{categorySeriesVariable(id:"%s"){name}}' % self._id, keys=[
                "categorySeriesVariable", "name"])

    @name.setter
    def name(self, newName):
        self.client.mutation(
            'mutation{categorySeriesVariable(id:"%s", name:"%s"){id}}' % (self._id, newName), asyncio=False)

    @property
    def private(self):
        if self.client.asyncio:
            return self.loader.load("private")
        else:
            return self.client.query('{categorySeriesVariable(id:"%s"){private}}' % self._id, keys=[
                "categorySeriesVariable", "private"])

    @private.setter
    def private(self, newValue):
        self.client.mutation(
            'mutation{categorySeriesVariable(id:"%s", private:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def hidden(self):
        if self.client.asyncio:
            return self.loader.load("hidden")
        else:
            return self.client.query('{categorySeriesVariable(id:"%s"){hidden}}' % self._id, keys=[
                "categorySeriesVariable", "hidden"])

    @hidden.setter
    def hidden(self, newValue):
        self.client.mutation(
            'mutation{categorySeriesVariable(id:"%s", hidden:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def index(self):
        if self.client.asyncio:
            return self.loader.load("index")
        else:
            return self.client.query('{categorySeriesVariable(id:"%s"){index}}' % self._id, keys=[
                "categorySeriesVariable", "index"])

    @index.setter
    def index(self, newValue):
        self.client.mutation(
            'mutation{categorySeriesVariable(id:"%s", index:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def myRole(self):
        if self.client.asyncio:
            return self.loader.load("myRole")
        else:
            return self.client.query('{categorySeriesVariable(id:"%s"){myRole}}' % self._id, keys=[
                "categorySeriesVariable", "myRole"])

    @property
    def createdAt(self):
        if self.client.asyncio:
            return self.loader.load("createdAt")
        else:
            return self.client.query('{categorySeriesVariable(id:"%s"){createdAt}}' % self._id, keys=[
                "categorySeriesVariable", "createdAt"])

    @property
    def updatedAt(self):
        if self.client.asyncio:
            return self.loader.load("updatedAt")
        else:
            return self.client.query('{categorySeriesVariable(id:"%s"){updatedAt}}' % self._id, keys=[
                "categorySeriesVariable", "updatedAt"])

    async def _async_load_thing(self):
        id = await self.loader.load("thing{id}")["id"]
        from .thing import Thing
        return Thing(self.client, id)

    @property
    def thing(self):
        if self.client.asyncio:
            return self._async_load_thing()
        else:
            id = self.client.query('{categorySeriesVariable(id:"%s"){thing{id}}}' % self._id, keys=[
                "categorySeriesVariable", "thing", "id"])

            from .thing import Thing
            return Thing(self.client, id)

    @property
    def allowedValues(self):
        if self.client.asyncio:
            return self.loader.load("allowedValues")
        else:
            return self.client.query('{categorySeriesVariable(id:"%s"){allowedValues}}' % self._id, keys=[
                "categorySeriesVariable", "allowedValues"])

    @allowedValues.setter
    def allowedValues(self, newValue):
        self.client.mutation(
            'mutation{categorySeriesVariable(id:"%s", allowedValues:%s){id}}' % (self._id, str(newValue)), asyncio=False)
