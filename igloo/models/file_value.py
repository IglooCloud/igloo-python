
from aiodataloader import DataLoader


class FileVariableLoader(DataLoader):
    def __init__(self, client, id):
        super().__init__()
        self.client = client
        self._id = id

    async def batch_load_fn(self, keys):
        fields = " ".join(set(keys))
        res = await self.client.query('{fileVariable(id:"%s"){%s}}' % (self._id, fields), keys=["fileVariable"])

        # if fetching object the key will be the first part of the field
        # e.g. when fetching thing{id} the result is in the thing key
        resolvedValues = [res[key.split("{")[0]] for key in keys]

        return resolvedValues


class FileVariable:
    def __init__(self, client, id):
        self.client = client
        self._id = id
        self.loader = FileVariableLoader(client, id)

    @property
    def id(self):
        return self._id

    @property
    def createdAt(self):
        if self.client.asyncio:
            return self.loader.load("createdAt")
        else:
            return self.client.query('{fileVariable(id:"%s"){createdAt}}' % self._id, keys=[
                "fileVariable", "createdAt"])

    @property
    def updatedAt(self):
        if self.client.asyncio:
            return self.loader.load("updatedAt")
        else:
            return self.client.query('{fileVariable(id:"%s"){updatedAt}}' % self._id, keys=[
                "fileVariable", "updatedAt"])

    @property
    def name(self):
        if self.client.asyncio:
            return self.loader.load("name")
        else:
            return self.client.query('{fileVariable(id:"%s"){name}}' % self._id, keys=[
                "fileVariable", "name"])

    @name.setter
    def name(self, newName):
        self.client.mutation(
            'mutation{fileVariable(id:"%s", name:"%s"){id}}' % (self._id, newName), asyncio=False)

    @property
    def private(self):
        if self.client.asyncio:
            return self.loader.load("private")
        else:
            return self.client.query('{fileVariable(id:"%s"){private}}' % self._id, keys=[
                "fileVariable", "private"])

    @private.setter
    def private(self, newValue):
        self.client.mutation(
            'mutation{fileVariable(id:"%s", private:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def hidden(self):
        if self.client.asyncio:
            return self.loader.load("hidden")
        else:
            return self.client.query('{fileVariable(id:"%s"){hidden}}' % self._id, keys=[
                "fileVariable", "hidden"])

    @hidden.setter
    def hidden(self, newValue):
        self.client.mutation(
            'mutation{fileVariable(id:"%s", hidden:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def index(self):
        if self.client.asyncio:
            return self.loader.load("index")
        else:
            return self.client.query('{fileVariable(id:"%s"){index}}' % self._id, keys=[
                "fileVariable", "index"])

    @index.setter
    def index(self, newValue):
        self.client.mutation(
            'mutation{fileVariable(id:"%s", index:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def myRole(self):
        if self.client.asyncio:
            return self.loader.load("myRole")
        else:
            return self.client.query('{fileVariable(id:"%s"){myRole}}' % self._id, keys=[
                "fileVariable", "myRole"])

    async def _async_load_thing(self):
        id = await self.loader.load("thing{id}")["id"]

        from .thing import Thing
        return Thing(self.client, id)

    @property
    def thing(self):
        if self.client.asyncio:
            return self._async_load_thing()
        else:
            id = self.client.query('{fileVariable(id:"%s"){thing{id}}}' % self._id, keys=[
                "fileVariable", "thing", "id"])

            return Thing(self.client, id)

    @property
    def permission(self):
        if self.client.asyncio:
            return self.loader.load("permission")
        else:
            return self.client.query('{fileVariable(id:"%s"){permission}}' % self._id, keys=[
                "fileVariable", "permission"])

    @permission.setter
    def permission(self, newValue):
        self.client.mutation(
            'mutation{fileVariable(id:"%s", permission:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def value(self):
        if self.client.asyncio:
            return self.loader.load("value")
        else:
            return self.client.query('{fileVariable(id:"%s"){value}}' % self._id, keys=[
                "fileVariable", "value"])

    @property
    def fileName(self):
        if self.client.asyncio:
            return self.loader.load("fileName")
        else:
            return self.client.query('{fileVariable(id:"%s"){fileName}}' % self._id, keys=[
                "fileVariable", "fileName"])

    @property
    def mimeType(self):
        if self.client.asyncio:
            return self.loader.load("mimeType")
        else:
            return self.client.query('{fileVariable(id:"%s"){mimeType}}' % self._id, keys=[
                "fileVariable", "mimeType"])

    @property
    def size(self):
        if self.client.asyncio:
            return self.loader.load("size")
        else:
            return self.client.query('{fileVariable(id:"%s"){size}}' % self._id, keys=[
                "fileVariable", "size"])
