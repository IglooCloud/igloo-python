
from aiodataloader import DataLoader


class StringVariableLoader(DataLoader):
    def __init__(self, client, id):
        super().__init__()
        self.client = client
        self._id = id

    async def batch_load_fn(self, keys):
        fields = " ".join(set(keys))
        res = await self.client.query('{stringVariable(id:"%s"){%s}}' % (self._id, fields), keys=["stringVariable"])

        # if fetching object the key will be the first part of the field
        # e.g. when fetching thing{id} the result is in the thing key
        resolvedValues = [res[key.split("{")[0]] for key in keys]

        return resolvedValues


class StringVariable:
    def __init__(self, client, id):
        self.client = client
        self._id = id
        self.loader = StringVariableLoader(client, id)

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        if self.client.asyncio:
            return self.loader.load("name")
        else:
            return self.client.query('{stringVariable(id:"%s"){name}}' % self._id, keys=[
                "stringVariable", "name"])

    @name.setter
    def name(self, newName):
        self.client.mutation(
            'mutation{stringVariable(id:"%s", name:"%s"){id}}' % (self._id, newName), asyncio=False)

    @property
    def private(self):
        if self.client.asyncio:
            return self.loader.load("private")
        else:
            return self.client.query('{stringVariable(id:"%s"){private}}' % self._id, keys=[
                "stringVariable", "private"])

    @private.setter
    def private(self, newValue):
        self.client.mutation(
            'mutation{stringVariable(id:"%s", private:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def hidden(self):
        if self.client.asyncio:
            return self.loader.load("hidden")
        else:
            return self.client.query('{stringVariable(id:"%s"){hidden}}' % self._id, keys=[
                "stringVariable", "hidden"])

    @hidden.setter
    def hidden(self, newValue):
        self.client.mutation(
            'mutation{stringVariable(id:"%s", hidden:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def index(self):
        if self.client.asyncio:
            return self.loader.load("index")
        else:
            return self.client.query('{stringVariable(id:"%s"){index}}' % self._id, keys=[
                "stringVariable", "index"])

    @index.setter
    def index(self, newValue):
        self.client.mutation(
            'mutation{stringVariable(id:"%s", index:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def myRole(self):
        if self.client.asyncio:
            return self.loader.load("myRole")
        else:
            return self.client.query('{stringVariable(id:"%s"){myRole}}' % self._id, keys=[
                "stringVariable", "myRole"])

    @property
    def createdAt(self):
        if self.client.asyncio:
            return self.loader.load("createdAt")
        else:
            return self.client.query('{stringVariable(id:"%s"){createdAt}}' % self._id, keys=[
                "stringVariable", "createdAt"])

    @property
    def updatedAt(self):
        if self.client.asyncio:
            return self.loader.load("updatedAt")
        else:
            return self.client.query('{stringVariable(id:"%s"){updatedAt}}' % self._id, keys=[
                "stringVariable", "updatedAt"])

    async def _async_load_thing(self):
        id = await self.loader.load("thing{id}")["id"]

        from .thing import Thing
        return Thing(self.client, id)

    @property
    def thing(self):
        if self.client.asyncio:
            return self._async_load_thing()
        else:
            id = self.client.query('{stringVariable(id:"%s"){thing{id}}}' % self._id, keys=[
                "stringVariable", "thing", "id"])

            from .thing import Thing
            return Thing(self.client, id)

    @property
    def permission(self):
        if self.client.asyncio:
            return self.loader.load("permission")
        else:
            return self.client.query('{stringVariable(id:"%s"){permission}}' % self._id, keys=[
                "stringVariable", "permission"])

    @permission.setter
    def permission(self, newValue):
        self.client.mutation(
            'mutation{stringVariable(id:"%s", permission:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def value(self):
        if self.client.asyncio:
            return self.loader.load("value")
        else:
            return self.client.query('{stringVariable(id:"%s"){value}}' % self._id, keys=[
                "stringVariable", "value"])

    @value.setter
    def value(self, newValue):
        self.client.mutation(
            'mutation{stringVariable(id:"%s", value:"%s"){id}}' % (self._id, newValue), asyncio=False)

    @property
    def maxChars(self):
        if self.client.asyncio:
            return self.loader.load("maxChars")
        else:
            return self.client.query('{stringVariable(id:"%s"){maxChars}}' % self._id, keys=[
                "stringVariable", "maxChars"])

    @maxChars.setter
    def maxChars(self, newValue):
        self.client.mutation(
            'mutation{stringVariable(id:"%s", maxChars:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def allowedValues(self):
        if self.client.asyncio:
            return self.loader.load("allowedValues")
        else:
            return self.client.query('{stringVariable(id:"%s"){allowedValues}}' % self._id, keys=[
                "stringVariable", "allowedValues"])

    @allowedValues.setter
    def allowedValues(self, newValue):
        self.client.mutation(
            'mutation{stringVariable(id:"%s", allowedValues:%s){id}}' % (self._id, str(newValue)), asyncio=False)
