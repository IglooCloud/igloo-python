
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
            'mutation{updateFloatVariable(id:"%s", name:"%s"){id}}' % (self._id, newName), asyncio=False)

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
            'mutation{updateFloatVariable(id:"%s", private:%s){id}}' % (self._id, newValue), asyncio=False)

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
            'mutation{updateFloatVariable(id:"%s", hidden:%s){id}}' % (self._id, newValue), asyncio=False)

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
            'mutation{updateFloatVariable(id:"%s", index:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def my_role(self):
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
    def user_permission(self):
        if self.client.asyncio:
            return self.loader.load("userPermission")
        else:
            return self.client.query('{floatVariable(id:"%s"){userPermission}}' % self._id, keys=[
                "floatVariable", "userPermission"])

    @user_permission.setter
    def user_permission(self, newValue):
        self.client.mutation(
            'mutation{updateFloatVariable(id:"%s", userPermission:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def developer_only(self):
        if self.client.asyncio:
            return self.loader.load("developerOnly")
        else:
            return self.client.query('{floatVariable(id:"%s"){developerOnly}}' % self._id, keys=[
                "floatVariable", "developerOnly"])

    @developer_only.setter
    def developer_only(self, newValue):
        self.client.mutation(
            'mutation{updateFloatVariable(id:"%s", developerOnly:%s){id}}' % (self._id, newValue), asyncio=False)

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
            'mutation{updateFloatVariable(id:"%s", value:%s){id}}' % (self._id, newValue), asyncio=False)

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
            'mutation{updateFloatVariable(id:"%s", precision:%s){id}}' % (self._id, newValue), asyncio=False)

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
            'mutation{updateFloatVariable(id:"%s", min:%s){id}}' % (self._id, newValue), asyncio=False)

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
            'mutation{updateFloatVariable(id:"%s", max:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def allowed_values(self):
        if self.client.asyncio:
            return self.loader.load("allowedValues")
        else:
            return self.client.query('{floatVariable(id:"%s"){allowedValues}}' % self._id, keys=[
                "floatVariable", "allowedValues"])

    @allowed_values.setter
    def allowed_values(self, newValue):
        self.client.mutation(
            'mutation{updateFloatVariable(id:"%s", allowedValues:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def unit_of_measurement(self):
        if self.client.asyncio:
            return self.loader.load("unitOfMeasurement")
        else:
            return self.client.query('{floatVariable(id:"%s"){unitOfMeasurement}}' % self._id, keys=[
                "floatVariable", "unitOfMeasurement"])

    @unit_of_measurement.setter
    def unit_of_measurement(self, newValue):
        self.client.mutation(
            'mutation{updateFloatVariable(id:"%s", unitOfMeasurement:"%s"){id}}' % (self._id, newValue), asyncio=False)
