
from aiodataloader import DataLoader
from igloo.models.utils import wrapWith


class FloatSeriesValueLoader(DataLoader):
    def __init__(self, client, id):
        super().__init__()
        self.client = client
        self._id = id

    async def batch_load_fn(self, keys):
        fields = " ".join(set(keys))
        res = await self.client.query('{floatSeriesValue(id:"%s"){%s}}' % (self._id, fields), keys=["floatSeriesValue"])

        # if fetching object the key will be the first part of the field
        # e.g. when fetching device{id} the result is in the device key
        resolvedValues = [res[key.split("{")[0]] for key in keys]

        return resolvedValues


class FloatSeriesValue:
    def __init__(self, client, id):
        self.client = client
        self._id = id
        self.loader = FloatSeriesValueLoader(client, id)

    @property
    def id(self):
        return self._id

    @property
    def lastNode(self):
        if self.client.asyncio:
            res = self.loader.load("lastNode{id}")
        else:
            res = self.client.query('{floatSeriesValue(id:"%s"){lastNode{id}}}' % self._id, keys=[
                "floatSeriesValue", "lastNode"])

        def wrapper(res):
            from .float_series_node import FloatSeriesNode
            return FloatSeriesNode(self.client, res["id"])

        return wrapWith(res, wrapper)

    @property
    def nodes(self):
        from .float_series_node import FloatSeriesNodeList
        return FloatSeriesNodeList(self.client, self._id)

    @property
    def name(self):
        if self.client.asyncio:
            return self.loader.load("name")
        else:
            return self.client.query('{floatSeriesValue(id:"%s"){name}}' % self._id, keys=[
                "floatSeriesValue", "name"])

    @name.setter
    def name(self, newName):
        self.client.mutation(
            'mutation{floatSeriesValue(id:"%s", name:"%s"){id}}' % (self._id, newName), asyncio=False)

    @property
    def private(self):
        if self.client.asyncio:
            return self.loader.load("private")
        else:
            return self.client.query('{floatSeriesValue(id:"%s"){private}}' % self._id, keys=[
                "floatSeriesValue", "private"])

    @private.setter
    def private(self, newValue):
        self.client.mutation(
            'mutation{floatSeriesValue(id:"%s", private:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def hidden(self):
        if self.client.asyncio:
            return self.loader.load("hidden")
        else:
            return self.client.query('{floatSeriesValue(id:"%s"){hidden}}' % self._id, keys=[
                "floatSeriesValue", "hidden"])

    @hidden.setter
    def hidden(self, newValue):
        self.client.mutation(
            'mutation{floatSeriesValue(id:"%s", hidden:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def cardSize(self):
        if self.client.asyncio:
            return self.loader.load("cardSize")
        else:
            return self.client.query('{floatSeriesValue(id:"%s"){cardSize}}' % self._id, keys=[
                "floatSeriesValue", "cardSize"])

    @cardSize.setter
    def cardSize(self, newValue):
        self.client.mutation(
            'mutation{floatSeriesValue(id:"%s", cardSize:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def index(self):
        if self.client.asyncio:
            return self.loader.load("index")
        else:
            return self.client.query('{floatSeriesValue(id:"%s"){index}}' % self._id, keys=[
                "floatSeriesValue", "index"])

    @index.setter
    def index(self, newValue):
        self.client.mutation(
            'mutation{floatSeriesValue(id:"%s", index:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def myRole(self):
        if self.client.asyncio:
            return self.loader.load("myRole")
        else:
            return self.client.query('{floatSeriesValue(id:"%s"){myRole}}' % self._id, keys=[
                "floatSeriesValue", "myRole"])

    @property
    def createdAt(self):
        if self.client.asyncio:
            return self.loader.load("createdAt")
        else:
            return self.client.query('{floatSeriesValue(id:"%s"){createdAt}}' % self._id, keys=[
                "floatSeriesValue", "createdAt"])

    @property
    def updatedAt(self):
        if self.client.asyncio:
            return self.loader.load("updatedAt")
        else:
            return self.client.query('{floatSeriesValue(id:"%s"){updatedAt}}' % self._id, keys=[
                "floatSeriesValue", "updatedAt"])

    async def _async_load_device(self):
        id = await self.loader.load("device{id}")["id"]
        from .device import Device
        return Device(self.client, id)

    @property
    def device(self):
        if self.client.asyncio:
            return self._async_load_device()
        else:
            id = self.client.query('{floatSeriesValue(id:"%s"){device{id}}}' % self._id, keys=[
                "floatSeriesValue", "device", "id"])

            from .device import Device
            return Device(self.client, id)

    @property
    def unitOfMeasurement(self):
        if self.client.asyncio:
            return self.loader.load("unitOfMeasurement")
        else:
            return self.client.query('{floatSeriesValue(id:"%s"){unitOfMeasurement}}' % self._id, keys=[
                "floatSeriesValue", "unitOfMeasurement"])

    @unitOfMeasurement.setter
    def unitOfMeasurement(self, newValue):
        self.client.mutation(
            'mutation{floatSeriesValue(id:"%s", unitOfMeasurement:"%s"){id}}' % (self._id, newValue), asyncio=False)

    @property
    def precision(self):
        if self.client.asyncio:
            return self.loader.load("precision")
        else:
            return self.client.query('{floatSeriesValue(id:"%s"){precision}}' % self._id, keys=[
                "floatSeriesValue", "precision"])

    @precision.setter
    def precision(self, newValue):
        self.client.mutation(
            'mutation{floatSeriesValue(id:"%s", precision:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def min(self):
        if self.client.asyncio:
            return self.loader.load("min")
        else:
            return self.client.query('{floatSeriesValue(id:"%s"){min}}' % self._id, keys=[
                "floatSeriesValue", "min"])

    @min.setter
    def min(self, newValue):
        self.client.mutation(
            'mutation{floatSeriesValue(id:"%s", min:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def max(self):
        if self.client.asyncio:
            return self.loader.load("max")
        else:
            return self.client.query('{floatSeriesValue(id:"%s"){max}}' % self._id, keys=[
                "floatSeriesValue", "max"])

    @max.setter
    def max(self, newValue):
        self.client.mutation(
            'mutation{floatSeriesValue(id:"%s", max:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def threshold(self):
        if self.client.asyncio:
            return self.loader.load("threshold")
        else:
            return self.client.query('{floatSeriesValue(id:"%s"){threshold}}' % self._id, keys=[
                "floatSeriesValue", "threshold"])

    @threshold.setter
    def threshold(self, newValue):
        self.client.mutation(
            'mutation{floatSeriesValue(id:"%s", threshold:%s){id}}' % (self._id, newValue), asyncio=False)
