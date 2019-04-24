
from aiodataloader import DataLoader


class BooleanValueLoader(DataLoader):
    def __init__(self, client, id):
        super().__init__()
        self.client = client
        self._id = id

    async def batch_load_fn(self, keys):
        fields = " ".join(set(keys))
        res = await self.client.query('{booleanValue(id:"%s"){%s}}' % (self._id, fields), keys=["booleanValue"])

        # if fetching object the key will be the first part of the field
        # e.g. when fetching device{id} the result is in the device key
        resolvedValues = [res[key.split("{")[0]] for key in keys]

        return resolvedValues


class BooleanValue:
    def __init__(self, client, id):
        self.client = client
        self._id = id
        self.loader = BooleanValueLoader(client, id)

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        if self.client.asyncio:
            return self.loader.load("name")
        else:
            return self.client.query('{booleanValue(id:"%s"){name}}' % self._id, keys=[
                "booleanValue", "name"])

    @name.setter
    def name(self, newName):
        self.client.mutation(
            'mutation{booleanValue(id:"%s", name:"%s"){id}}' % (self._id, newName), asyncio=False)

    @property
    def private(self):
        if self.client.asyncio:
            return self.loader.load("private")
        else:
            return self.client.query('{booleanValue(id:"%s"){private}}' % self._id, keys=[
                "booleanValue", "private"])

    @private.setter
    def private(self, newValue):
        self.client.mutation(
            'mutation{booleanValue(id:"%s", private:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def hidden(self):
        if self.client.asyncio:
            return self.loader.load("hidden")
        else:
            return self.client.query('{booleanValue(id:"%s"){hidden}}' % self._id, keys=[
                "booleanValue", "hidden"])

    @hidden.setter
    def hidden(self, newValue):
        self.client.mutation(
            'mutation{booleanValue(id:"%s", hidden:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def cardSize(self):
        if self.client.asyncio:
            return self.loader.load("cardSize")
        else:
            return self.client.query('{booleanValue(id:"%s"){cardSize}}' % self._id, keys=[
                "booleanValue", "cardSize"])

    @cardSize.setter
    def cardSize(self, newValue):
        self.client.mutation(
            'mutation{booleanValue(id:"%s", cardSize:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def index(self):
        if self.client.asyncio:
            return self.loader.load("index")
        else:
            return self.client.query('{booleanValue(id:"%s"){index}}' % self._id, keys=[
                "booleanValue", "index"])

    @index.setter
    def index(self, newValue):
        self.client.mutation(
            'mutation{booleanValue(id:"%s", index:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def myRole(self):
        if self.client.asyncio:
            return self.loader.load("myRole")
        else:
            return self.client.query('{booleanValue(id:"%s"){myRole}}' % self._id, keys=[
                "booleanValue", "myRole"])

    @property
    def createdAt(self):
        if self.client.asyncio:
            return self.loader.load("createdAt")
        else:
            return self.client.query('{booleanValue(id:"%s"){createdAt}}' % self._id, keys=[
                "booleanValue", "createdAt"])

    @property
    def updatedAt(self):
        if self.client.asyncio:
            return self.loader.load("updatedAt")
        else:
            return self.client.query('{booleanValue(id:"%s"){updatedAt}}' % self._id, keys=[
                "booleanValue", "updatedAt"])

    async def _async_load_device(self):
        id = await self.loader.load("device{id}")["id"]
        from .device import Device
        return Device(self.client, id)

    @property
    def device(self):
        if self.client.asyncio:
            return self._async_load_device()
        else:
            id = self.client.query('{booleanValue(id:"%s"){device{id}}}' % self._id, keys=[
                "booleanValue", "device", "id"])

            from .device import Device
            return Device(self.client, id)

    @property
    def value(self):
        if self.client.asyncio:
            return self.loader.load("value")
        else:
            return self.client.query('{booleanValue(id:"%s"){value}}' % self._id, keys=[
                "booleanValue", "value"])

    @value.setter
    def value(self, newValue):
        self.client.mutation(
            'mutation{booleanValue(id:"%s", value:%s){id}}' % (self._id, "true" if newValue else "false"), asyncio=False)
