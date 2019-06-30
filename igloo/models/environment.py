from igloo.models.utils import wrapWith
from igloo.utils import get_representation
from aiodataloader import DataLoader


class EnvironmentLoader(DataLoader):
    def __init__(self, client, id):
        super().__init__()
        self.client = client
        self._id = id

    async def batch_load_fn(self, keys):
        fields = " ".join(set(keys))
        res = await self.client.query('{environment(id:"%s"){%s}}' % (self._id, fields), keys=["environment"])

        resolvedValues = [res[key.split("{")[0]] for key in keys]

        return resolvedValues


class Environment:
    def __init__(self, client, id):
        self.client = client
        self._id = id
        self.loader = EnvironmentLoader(client, id)

    @property
    def id(self):
        return self._id

    @property
    def createdAt(self):
        if self.client.asyncio:
            return self.loader.load("createdAt")
        else:
            return self.client.query('{environment(id:"%s"){createdAt}}' % self._id, keys=[
                "environment", "createdAt"])

    @property
    def updatedAt(self):
        if self.client.asyncio:
            return self.loader.load("updatedAt")
        else:
            return self.client.query('{environment(id:"%s"){updatedAt}}' % self._id, keys=[
                "environment", "updatedAt"])

    @property
    def name(self):
        if self.client.asyncio:
            return self.loader.load("name")
        else:
            return self.client.query('{environment(id:"%s"){name}}' % self._id, keys=[
                "environment", "name"])

    @name.setter
    def name(self, newName):
        self.client.mutation(
            'mutation{environment(id:"%s", name:"%s"){id}}' % (self._id, newName), asyncio=False)

    @property
    def owner(self):
        if self.client.asyncio:
            res = self.loader.load("owner{id}")
        else:
            res = self.client.query('{environment(id:"%s"){owner{id}}}' % self._id, keys=[
                "environment", "owner"])

        def wrapper(res):
            from .user import User
            res = User(self.client, res["id"])

            return res

        return wrapWith(res, wrapper)

    @property
    def myRole(self):
        if self.client.asyncio:
            return self.loader.load("myRole")
        else:
            return self.client.query('{environment(id:"%s"){myRole}}' % self._id, keys=[
                "environment", "myRole"])

    @property
    def picture(self):
        if self.client.asyncio:
            return self.loader.load("picture")
        else:
            return self.client.query('{environment(id:"%s"){picture}}' % self._id, keys=[
                "environment", "picture"])

    @picture.setter
    def picture(self, newPicture):
        self.client.mutation(
            'mutation{environment(id:"%s", picture:"%s"){id}}' % (self._id, newPicture), asyncio=False)

    @property
    def uniqueFirmwares(self):
        if self.client.asyncio:
            return self.loader.load("uniqueFirmwares")
        else:
            return self.client.query('{environment(id:"%s"){uniqueFirmwares}}' % self._id, keys=[
                "environment", "uniqueFirmwares"])

    @property
    def index(self):
        if self.client.asyncio:
            return self.loader.load("index")
        else:
            return self.client.query('{environment(id:"%s"){index}}' % self._id, keys=[
                "environment", "index"])

    @index.setter
    def index(self, newIndex):
        self.client.mutation(
            'mutation{environment(id:"%s", index:%s){id}}' % (self._id, newIndex), asyncio=False)

    @property
    def muted(self):
        if self.client.asyncio:
            return self.loader.load("muted")
        else:
            return self.client.query('{environment(id:"%s"){muted}}' % self._id, keys=[
                "environment", "muted"])

    @muted.setter
    def muted(self, newMuted):
        self.client.mutation(
            'mutation{environment(id:"%s", muted:%s){id}}' % (self._id, "true" if newMuted else "false"), asyncio=False)

    @property
    def things(self):
        from .thing import EnvironmentThingList
        return EnvironmentThingList(self.client, self._id)

    @property
    def admins(self):
        from .user import EnvironmentAdminList
        return EnvironmentAdminList(self.client, self._id)

    @property
    def editors(self):
        from .user import EnvironmentEditorList
        return EnvironmentEditorList(self.client, self._id)

    @property
    def spectators(self):
        from .user import EnvironmentSpectatorList
        return EnvironmentSpectatorList(self.client, self._id)

    @property
    def pendingEnvironmentShares(self):
        from .pending_environment_share import EnvironmentPendingEnvironmentShareList
        return EnvironmentPendingEnvironmentShareList(self.client, self._id)

    @property
    def pendingOwnerChange(self):
        if self.client.asyncio:
            res = self.loader.load("pendingOwnerChange{id}")
        else:
            res = self.client.query('{environment(id:"%s"){pendingOwnerChange{id}}}' % self._id, keys=[
                "environment", "pendingOwnerChange"])

        def wrapper(res):
            from .pending_owner_change import PendingOwnerChange
            res = PendingOwnerChange(self.client, res["id"])

            return res

        return wrapWith(res, wrapper)


class EnvironmentList:
    def __init__(self, client, userId):
        self.client = client
        self.current = 0
        self._filter = "{}"
        self.userId = userId

    def filter(self, _filter):
        self._filter = get_representation(_filter)
        return self

    def __len__(self):
        res = self.client.query('{user(id:%s){environmentCount(filter:%s)}}' % (self.userId, self._filter), keys=[
                                "user", "environmentCount"])
        return res

    def __getitem__(self, i):
        if isinstance(i, int):
            res = self.client.query(
                '{user(id:%s){environments(limit:1, offset:%d, filter:%s){id}}}' % (self.userId, i, self._filter))
            if len(res["user"]["environments"]) != 1:
                raise IndexError()
            return Environment(self.client, res["user"]["environments"][0]["id"])
        elif isinstance(i, slice):
            start, end, _ = i.indices(len(self))
            res = self.client.query(
                '{user(id:%s){environments(offset:%d, limit:%d, filter:%s){id}}}' % (self.userId, start, end-start, self._filter))
            return [Environment(self.client, environment["id"]) for environment in res["user"]["environments"]]
        else:
            raise TypeError("Unexpected type {} passed as index".format(i))

    def __iter__(self):
        return self

    def __next__(self):
        res = self.client.query(
            '{user(id:%s){environments(limit:1, offset:%d, filter:%s){id}}}' % (self.userId, self.current, self._filter))

        if len(res["user"]["environments"]) != 1:
            raise StopIteration

        self.current += 1
        return Environment(self.client, res["user"]["environments"][0]["id"])

    def next(self):
        return self.__next__()
