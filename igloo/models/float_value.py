
from aiodataloader import DataLoader


class FloatVariableLoader(DataLoader):
    def __init__(self, client, id):
        super().__init__()
        self.client = client
        self._id = id

    async def batch_load_fn(self, keys):
        fields = " ".join(set(keys))
        res = await self.client.query('{floatVariable(id:"%s"){%s}}' % (self._id, fields), keys=["floatVariable"])

        # if fetching object the key will be the first part of the field
        # e.g. when fetching thing{id} the result is in the thing key
        resolvedValues = [res[key.split("{")[0]] for key in keys]

        return resolvedValues


class FloatVariable:
    def __init__(self, client, id):
        self.client = client
        self._id = id
        self.loader = FloatVariableLoader(client, id)

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        if self.client.asyncio:
            return self.loader.load("name")
        else:
            return self.client.query('{floatVariable(id:"%s"){name}}' % self._id, keys=[
                "floatVariable", "name"])

    @name.setter
    def name(self, newName):
        self.client.mutation(
            'mutation{floatVariable(id:"%s", name:"%s"){id}}' % (self._id, newName), asyncio=False)

    @property
    def private(self):
        if self.client.asyncio:
            return self.loader.load("private")
        else:
            return self.client.query('{floatVariable(id:"%s"){private}}' % self._id, keys=[
                "floatVariable", "private"])

    @private.setter
    def private(self, newValue):
        self.client.mutation(
            'mutation{floatVariable(id:"%s", private:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def hidden(self):
        if self.client.asyncio:
            return self.loader.load("hidden")
        else:
            return self.client.query('{floatVariable(id:"%s"){hidden}}' % self._id, keys=[
                "floatVariable", "hidden"])

    @hidden.setter
    def hidden(self, newValue):
        self.client.mutation(
            'mutation{floatVariable(id:"%s", hidden:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def index(self):
        if self.client.asyncio:
            return self.loader.load("index")
        else:
            return self.client.query('{floatVariable(id:"%s"){index}}' % self._id, keys=[
                "floatVariable", "index"])

    @index.setter
    def index(self, newValue):
        self.client.mutation(
            'mutation{floatVariable(id:"%s", index:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def myRole(self):
        if self.client.asyncio:
            return self.loader.load("myRole")
        else:
            return self.client.query('{floatVariable(id:"%s"){myRole}}' % self._id, keys=[
                "floatVariable", "myRole"])

    @property
    def createdAt(self):
        if self.client.asyncio:
            return self.loader.load("createdAt")
        else:
            return self.client.query('{floatVariable(id:"%s"){createdAt}}' % self._id, keys=[
                "floatVariable", "createdAt"])

    @property
    def updatedAt(self):
        if self.client.asyncio:
            return self.loader.load("updatedAt")
        else:
            return self.client.query('{floatVariable(id:"%s"){updatedAt}}' % self._id, keys=[
                "floatVariable", "updatedAt"])

    async def _async_load_thing(self):
        id = await self.loader.load("thing{id}")["id"]

        from .thing import Thing
        return Thing(self.client, id)

    @property
    def thing(self):
        if self.client.asyncio:
            return self._async_load_thing()
        else:
            id = self.client.query('{floatVariable(id:"%s"){thing{id}}}' % self._id, keys=[
                "floatVariable", "thing", "id"])

            from .thing import Thing
            return Thing(self.client, id)

    @property
    def permission(self):
        if self.client.asyncio:
            return self.loader.load("permission")
        else:
            return self.client.query('{floatVariable(id:"%s"){permission}}' % self._id, keys=[
                "floatVariable", "permission"])

    @permission.setter
    def permission(self, newValue):
        self.client.mutation(
            'mutation{floatVariable(id:"%s", permission:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def value(self):
        if self.client.asyncio:
            return self.loader.load("value")
        else:
            return self.client.query('{floatVariable(id:"%s"){value}}' % self._id, keys=[
                "floatVariable", "value"])

    @value.setter
    def value(self, newValue):
        self.client.mutation(
            'mutation{floatVariable(id:"%s", value:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def precision(self):
        if self.client.asyncio:
            return self.loader.load("precision")
        else:
            return self.client.query('{floatVariable(id:"%s"){precision}}' % self._id, keys=[
                "floatVariable", "precision"])

    @precision.setter
    def precision(self, newValue):
        self.client.mutation(
            'mutation{floatVariable(id:"%s", precision:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def min(self):
        if self.client.asyncio:
            return self.loader.load("min")
        else:
            return self.client.query('{floatVariable(id:"%s"){min}}' % self._id, keys=[
                "floatVariable", "min"])

    @min.setter
    def min(self, newValue):
        self.client.mutation(
            'mutation{floatVariable(id:"%s", min:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def max(self):
        if self.client.asyncio:
            return self.loader.load("max")
        else:
            return self.client.query('{floatVariable(id:"%s"){max}}' % self._id, keys=[
                "floatVariable", "max"])

    @max.setter
    def max(self, newValue):
        self.client.mutation(
            'mutation{floatVariable(id:"%s", max:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def unitOfMeasurement(self):
        if self.client.asyncio:
            return self.loader.load("unitOfMeasurement")
        else:
            return self.client.query('{floatVariable(id:"%s"){unitOfMeasurement}}' % self._id, keys=[
                "floatVariable", "unitOfMeasurement"])

    @unitOfMeasurement.setter
    def unitOfMeasurement(self, newValue):
        self.client.mutation(
            'mutation{floatVariable(id:"%s", unitOfMeasurement:"%s"){id}}' % (self._id, newValue), asyncio=False)
