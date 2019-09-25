
from aiodataloader import DataLoader
from igloo.models.utils import wrapWith


class PendingOwnerChangeLoader(DataLoader):
    def __init__(self, client, id):
        super().__init__()
        self.client = client
        self._id = id

    async def batch_load_fn(self, keys):
        fields = " ".join(set(keys))
        res = await self.client.query('{pendingOwnerChange(id:"%s"){%s}}' % (self._id, fields), keys=["pendingOwnerChange"])

        # if fetching object the key will be the first part of the field
        # e.g. when fetching thing{id} the result is in the thing key
        resolvedValues = [res[key.split("{")[0]] for key in keys]

        return resolvedValues


class PendingOwnerChange:
    def __init__(self, client, id):
        self.client = client
        self._id = id
        self.loader = PendingOwnerChangeLoader(client, id)

    @property
    def id(self):
        return self._id

    @property
    def sender(self):
        if self.client.asyncio:
            res = self.loader.load("sender{id}")
        else:
            res = self.client.query('{pendingOwnerChange(id:"%s"){sender{id}}}' % self._id, keys=[
                "pendingOwnerChange", "sender"])

        def wrapper(res):
            from .user import User
            return User(self.client, res["id"])

        return wrapWith(res, wrapper)

    @property
    def receiver(self):
        if self.client.asyncio:
            res = self.loader.load("receiver{id}")
        else:
            res = self.client.query('{pendingOwnerChange(id:"%s"){receiver{id}}}' % self._id, keys=[
                "pendingOwnerChange", "receiver"])

        def wrapper(res):
            from .user import User
            return User(self.client, res["id"])

        return wrapWith(res, wrapper)

    @property
    def environment(self):
        if self.client.asyncio:
            res = self.loader.load("environment{id}")
        else:
            res = self.client.query('{pendingOwnerChange(id:"%s"){environment{id}}}' % self._id, keys=[
                "pendingOwnerChange", "environment"])

        def wrapper(res):
            from .environment import Environment
            return Environment(self.client, res["id"])

        return wrapWith(res, wrapper)


class UserPendingOwnerChangeList:
    def __init__(self, client, userId):
        self.client = client
        self.current = 0
        self.userId = userId

    def __len__(self):
        res = self.client.query('{user(id:%s){pendingOwnerChangeCount}}' % (self.userId), keys=[
                                "user", "pendingOwnerChangeCount"])
        return res

    def __getitem__(self, i):
        if isinstance(i, int):
            res = self.client.query(
                '{user(id:%s){pendingOwnerChanges(limit:1, offset:%d){id}}}' % (self.userId, i))
            if len(res["user"]["pendingOwnerChanges"]) != 1:
                raise IndexError()
            return PendingOwnerChange(self.client, res["user"]["pendingOwnerChanges"][0]["id"])
        elif isinstance(i, slice):
            start, end, _ = i.indices(len(self))
            res = self.client.query(
                '{user(id:%s){pendingOwnerChanges(offset:%d, limit:%d){id}}}' % (self.userId, start, end-start))
            return [PendingOwnerChange(self.client, ownerChange["id"]) for ownerChange in res["user"]["pendingOwnerChanges"]]
        else:
            raise TypeError("Unexpected type {} passed as index".format(i))

    def __iter__(self):
        return self

    def __next__(self):
        res = self.client.query(
            '{user(id:%s){pendingOwnerChanges(limit:1, offset:%d){id}}}' % (self.userId, self.current))

        if len(res["user"]["pendingOwnerChanges"]) != 1:
            raise StopIteration

        self.current += 1
        return PendingOwnerChange(self.client, res["user"]["pendingOwnerChanges"][0]["id"])

    def next(self):
        return self.__next__()
