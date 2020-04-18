
from aiodataloader import DataLoader
from igloo.models.utils import wrapWith


class CategorySeriesNodeLoader(DataLoader):
    def __init__(self, client, id):
        super().__init__()
        self.client = client
        self._id = id

    async def batch_load_fn(self, keys):
        fields = " ".join(set(keys))
        res = await self.client.query('{categorySeriesNode(id:"%s"){%s}}' % (self._id, fields), keys=["categorySeriesNode"])

        # if fetching object the key will be the first part of the field
        # e.g. when fetching thing{id} the result is in the thing key
        resolvedValues = [res[key.split("{")[0]] for key in keys]

        return resolvedValues


class CategorySeriesNode:
    def __init__(self, client, id):
        self.client = client
        self._id = id
        self.loader = CategorySeriesNodeLoader(client, id)

    @property
    def id(self):
        return self._id

    @property
    def createdAt(self):
        if self.client.asyncio:
            return self.loader.load("createdAt")
        else:
            return self.client.query('{categorySeriesNode(id:"%s"){createdAt}}' % self._id, keys=[
                "categorySeriesNode", "createdAt"])

    @property
    def updatedAt(self):
        if self.client.asyncio:
            return self.loader.load("updatedAt")
        else:
            return self.client.query('{categorySeriesNode(id:"%s"){updatedAt}}' % self._id, keys=[
                "categorySeriesNode", "updatedAt"])

    @property
    def thing(self):
        if self.client.asyncio:
            res = self.loader.load("thing{id}")
        else:
            res = self.client.query('{categorySeriesNode(id:"%s"){thing{id}}}' % self._id, keys=[
                "categorySeriesNode", "thing"])

        def wrapper(res):
            from .thing import Thing
            return Thing(self.client, res["id"])

        return wrapWith(res, wrapper)

    @property
    def series(self):
        if self.client.asyncio:
            res = self.loader.load("series{id}")
        else:
            res = self.client.query('{categorySeriesNode(id:"%s"){series{id}}}' % self._id, keys=[
                "categorySeriesNode", "series"])

        def wrapper(res):
            from .category_series_variable import CategorySeriesVariable
            return CategorySeriesVariable(self.client, res["id"])

        return wrapWith(res, wrapper)

    @property
    def timestamp(self):
        if self.client.asyncio:
            return self.loader.load("timestamp")
        else:
            return self.client.query('{categorySeriesNode(id:"%s"){timestamp}}' % self._id, keys=[
                "categorySeriesNode", "timestamp"])

    @timestamp.setter
    def timestamp(self, newValue):
        self.client.mutation(
            'mutation{categorySeriesNode(id:"%s", timestamp:"%s"){id}}' % (self._id, newValue), asyncio=False)

    @property
    def value(self):
        if self.client.asyncio:
            return self.loader.load("value")
        else:
            return self.client.query('{categorySeriesNode(id:"%s"){value}}' % self._id, keys=[
                "categorySeriesNode", "value"])

    @value.setter
    def value(self, newValue):
        self.client.mutation(
            'mutation{categorySeriesNode(id:"%s", value:"%s"){id}}' % (self._id, newValue), asyncio=False)


class CategorySeriesNodeList:
    def __init__(self, client, seriesId):
        self.client = client
        self.seriesId = seriesId
        self.current = 0

    def __len__(self):
        res = self.client.query(
            '{categorySeriesVariable(id:"%s"){nodeCount}}' % self.seriesId)
        return res["categorySeriesVariable"]["nodeCount"]

    def __getitem__(self, i):
        if isinstance(i, int):
            res = self.client.query(
                '{categorySeriesVariable(id:"%s"){nodes(limit:1, offset:%d){id}}}' % (self.seriesId, i))
            if len(res["categorySeriesVariable"]["nodes"]) != 1:
                raise IndexError()
            return CategorySeriesNode(self.client, res["categorySeriesVariable"]["nodes"][0]["id"])
        elif isinstance(i, slice):
            start, end, _ = i.indices(len(self))
            res = self.client.query(
                '{categorySeriesVariable(id:"%s"){nodes(offset:%d, limit:%d){id}}}' % (self.seriesId, start, end-start))
            return [CategorySeriesNode(self.client, node["id"]) for node in res["categorySeriesVariable"]["nodes"]]
        else:
            raise TypeError("Unexpected type {} passed as index".format(i))

    def __iter__(self):
        return self

    def __next__(self):
        res = self.client.query(
            '{categorySeriesVariable(id:"%s"){nodes(limit:1, offset:%d){id}}}' % (self.seriesId, self.current))

        if len(res["categorySeriesVariable", "nodes"]) != 1:
            raise StopIteration

        self.current += 1
        return CategorySeriesNode(self.client, res["categorySeriesVariable"]["nodes"][0]["id"])

    def next(self):
        return self.__next__()
