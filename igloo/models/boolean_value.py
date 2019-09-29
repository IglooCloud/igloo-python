
from aiodataloader import DataLoader


class BooleanVariableLoader(DataLoader):
    def __init__(self, client, id):
        super().__init__()
        self.client = client
        self._id = id

    async def batch_load_fn(self, keys):
        fields = " ".join(set(keys))
        res = await self.client.query('{booleanVariable(id:"%s"){%s}}' % (self._id, fields), keys=["booleanVariable"])

        # if fetching object the key will be the first part of the field
        # e.g. when fetching thing{id} the result is in the thing key
        resolvedValues = [res[key.split("{")[0]] for key in keys]

        return resolvedValues


class BooleanVariable:
    def __init__(self, client, id):
        self.client = client
        self._id = id
        self.loader = BooleanVariableLoader(client, id)

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        if self.client.asyncio:
            return self.loader.load("name")
        else:
            return self.client.query('{booleanVariable(id:"%s"){name}}' % self._id, keys=[
                "booleanVariable", "name"])

    @name.setter
    def name(self, newName):
        self.client.mutation(
            'mutation{booleanVariable(id:"%s", name:"%s"){id}}' % (self._id, newName), asyncio=False)

    @property
    def private(self):
        if self.client.asyncio:
            return self.loader.load("private")
        else:
            return self.client.query('{booleanVariable(id:"%s"){private}}' % self._id, keys=[
                "booleanVariable", "private"])

    @private.setter
    def private(self, newValue):
        self.client.mutation(
            'mutation{booleanVariable(id:"%s", private:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def hidden(self):
        if self.client.asyncio:
            return self.loader.load("hidden")
        else:
            return self.client.query('{booleanVariable(id:"%s"){hidden}}' % self._id, keys=[
                "booleanVariable", "hidden"])

    @hidden.setter
    def hidden(self, newValue):
        self.client.mutation(
            'mutation{booleanVariable(id:"%s", hidden:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def index(self):
        if self.client.asyncio:
            return self.loader.load("index")
        else:
            return self.client.query('{booleanVariable(id:"%s"){index}}' % self._id, keys=[
                "booleanVariable", "index"])

    @index.setter
    def index(self, newValue):
        self.client.mutation(
            'mutation{booleanVariable(id:"%s", index:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def myRole(self):
        if self.client.asyncio:
            return self.loader.load("myRole")
        else:
            return self.client.query('{booleanVariable(id:"%s"){myRole}}' % self._id, keys=[
                "booleanVariable", "myRole"])

    @property
    def createdAt(self):
        if self.client.asyncio:
            return self.loader.load("createdAt")
        else:
            return self.client.query('{booleanVariable(id:"%s"){createdAt}}' % self._id, keys=[
                "booleanVariable", "createdAt"])

    @property
    def updatedAt(self):
        if self.client.asyncio:
            return self.loader.load("updatedAt")
        else:
            return self.client.query('{booleanVariable(id:"%s"){updatedAt}}' % self._id, keys=[
                "booleanVariable", "updatedAt"])

    async def _async_load_thing(self):
        id = await self.loader.load("thing{id}")["id"]
        from .thing import Thing
        return Thing(self.client, id)

    @property
    def thing(self):
        if self.client.asyncio:
            return self._async_load_thing()
        else:
            id = self.client.query('{booleanVariable(id:"%s"){thing{id}}}' % self._id, keys=[
                "booleanVariable", "thing", "id"])

            from .thing import Thing
            return Thing(self.client, id)

    @property
    def value(self):
        if self.client.asyncio:
            return self.loader.load("value")
        else:
            return self.client.query('{booleanVariable(id:"%s"){value}}' % self._id, keys=[
                "booleanVariable", "value"])

    @value.setter
    def value(self, newValue):
        self.client.mutation(
            'mutation{booleanVariable(id:"%s", value:%s){id}}' % (self._id, "true" if newValue else "false"), asyncio=False)
