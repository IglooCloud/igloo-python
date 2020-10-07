
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
            'mutation{updateStringVariable(id:"%s", name:"%s"){id}}' % (self._id, newName), asyncio=False)

    @property
    def developer_only(self):
        if self.client.asyncio:
            return self.loader.load("developerOnly")
        else:
            return self.client.query('{stringVariable(id:"%s"){developerOnly}}' % self._id, keys=[
                "stringVariable", "developerOnly"])

    @developer_only.setter
    def developer_only(self, newValue):
        self.client.mutation(
            'mutation{updateStringVariable(id:"%s", developerOnly:%s){id}}' % (self._id, newValue), asyncio=False)

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
            'mutation{updateStringVariable(id:"%s", hidden:%s){id}}' % (self._id, newValue), asyncio=False)

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
            'mutation{updateStringVariable(id:"%s", index:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def my_role(self):
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
    def user_permission(self):
        if self.client.asyncio:
            return self.loader.load("userPermission")
        else:
            return self.client.query('{stringVariable(id:"%s"){userPermission}}' % self._id, keys=[
                "stringVariable", "userPermission"])

    @user_permission.setter
    def user_permission(self, newValue):
        self.client.mutation(
            'mutation{updateStringVariable(id:"%s", userPermission:%s){id}}' % (self._id, newValue), asyncio=False)

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
            'mutation{updateStringVariable(id:"%s", value:"%s"){id}}' % (self._id, newValue), asyncio=False)

    @property
    def max_characters(self):
        if self.client.asyncio:
            return self.loader.load("maxCharacters")
        else:
            return self.client.query('{stringVariable(id:"%s"){maxCharacters}}' % self._id, keys=[
                "stringVariable", "maxCharacters"])

    @max_characters.setter
    def max_characters(self, newValue):
        self.client.mutation(
            'mutation{updateStringVariable(id:"%s", maxCharacters:%s){id}}' % (self._id, newValue), asyncio=False)

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
            'mutation{updateStringVariable(id:"%s", allowedValues:%s){id}}' % (self._id, str(newValue)), asyncio=False)
