
from aiodataloader import DataLoader


class StringValueLoader(DataLoader):
    def __init__(self, client, id):
        super().__init__()
        self.client = client
        self._id = id

    async def batch_load_fn(self, keys):
        fields = " ".join(set(keys))
        res = await self.client.query('{stringValue(id:"%s"){%s}}' % (self._id, fields), keys=["stringValue"])

        # if fetching object the key will be the first part of the field
        # e.g. when fetching thing{id} the result is in the thing key
        resolvedValues = [res[key.split("{")[0]] for key in keys]

        return resolvedValues


class StringValue:
    def __init__(self, client, id):
        self.client = client
        self._id = id
        self.loader = StringValueLoader(client, id)

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        if self.client.asyncio:
            return self.loader.load("name")
        else:
            return self.client.query('{stringValue(id:"%s"){name}}' % self._id, keys=[
                "stringValue", "name"])

    @name.setter
    def name(self, newName):
        self.client.mutation(
            'mutation{stringValue(id:"%s", name:"%s"){id}}' % (self._id, newName), asyncio=False)

    @property
    def private(self):
        if self.client.asyncio:
            return self.loader.load("private")
        else:
            return self.client.query('{stringValue(id:"%s"){private}}' % self._id, keys=[
                "stringValue", "private"])

    @private.setter
    def private(self, newValue):
        self.client.mutation(
            'mutation{stringValue(id:"%s", private:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def hidden(self):
        if self.client.asyncio:
            return self.loader.load("hidden")
        else:
            return self.client.query('{stringValue(id:"%s"){hidden}}' % self._id, keys=[
                "stringValue", "hidden"])

    @hidden.setter
    def hidden(self, newValue):
        self.client.mutation(
            'mutation{stringValue(id:"%s", hidden:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def index(self):
        if self.client.asyncio:
            return self.loader.load("index")
        else:
            return self.client.query('{stringValue(id:"%s"){index}}' % self._id, keys=[
                "stringValue", "index"])

    @index.setter
    def index(self, newValue):
        self.client.mutation(
            'mutation{stringValue(id:"%s", index:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def myRole(self):
        if self.client.asyncio:
            return self.loader.load("myRole")
        else:
            return self.client.query('{stringValue(id:"%s"){myRole}}' % self._id, keys=[
                "stringValue", "myRole"])

    @property
    def createdAt(self):
        if self.client.asyncio:
            return self.loader.load("createdAt")
        else:
            return self.client.query('{stringValue(id:"%s"){createdAt}}' % self._id, keys=[
                "stringValue", "createdAt"])

    @property
    def updatedAt(self):
        if self.client.asyncio:
            return self.loader.load("updatedAt")
        else:
            return self.client.query('{stringValue(id:"%s"){updatedAt}}' % self._id, keys=[
                "stringValue", "updatedAt"])

    async def _async_load_thing(self):
        id = await self.loader.load("thing{id}")["id"]

        from .thing import Thing
        return Thing(self.client, id)

    @property
    def thing(self):
        if self.client.asyncio:
            return self._async_load_thing()
        else:
            id = self.client.query('{stringValue(id:"%s"){thing{id}}}' % self._id, keys=[
                "stringValue", "thing", "id"])

            from .thing import Thing
            return Thing(self.client, id)

    @property
    def permission(self):
        if self.client.asyncio:
            return self.loader.load("permission")
        else:
            return self.client.query('{stringValue(id:"%s"){permission}}' % self._id, keys=[
                "stringValue", "permission"])

    @permission.setter
    def permission(self, newValue):
        self.client.mutation(
            'mutation{stringValue(id:"%s", permission:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def value(self):
        if self.client.asyncio:
            return self.loader.load("value")
        else:
            return self.client.query('{stringValue(id:"%s"){value}}' % self._id, keys=[
                "stringValue", "value"])

    @value.setter
    def value(self, newValue):
        self.client.mutation(
            'mutation{stringValue(id:"%s", value:"%s"){id}}' % (self._id, newValue), asyncio=False)

    @property
    def maxChars(self):
        if self.client.asyncio:
            return self.loader.load("maxChars")
        else:
            return self.client.query('{stringValue(id:"%s"){maxChars}}' % self._id, keys=[
                "stringValue", "maxChars"])

    @maxChars.setter
    def maxChars(self, newValue):
        self.client.mutation(
            'mutation{stringValue(id:"%s", maxChars:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def allowedValues(self):
        if self.client.asyncio:
            return self.loader.load("allowedValues")
        else:
            return self.client.query('{stringValue(id:"%s"){allowedValues}}' % self._id, keys=[
                "stringValue", "allowedValues"])

    @allowedValues.setter
    def allowedValues(self, newValue):
        self.client.mutation(
            'mutation{stringValue(id:"%s", allowedValues:%s){id}}' % (self._id, str(newValue)), asyncio=False)
