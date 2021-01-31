
from aiodataloader import DataLoader
from igloo.models.utils import wrapWith


class PendingTransferLoader(DataLoader):
    def __init__(self, client, id):
        super().__init__()
        self.client = client
        self._id = id

    async def batch_load_fn(self, keys):
        fields = " ".join(set(keys))
        res = await self.client.query('{pendingTransfer(id:"%s"){%s}}' % (self._id, fields), keys=["pendingTransfer"])

        # if fetching object the key will be the first part of the field
        # e.g. when fetching thing{id} the result is in the thing key
        resolvedValues = [res[key.split("{")[0]] for key in keys]

        return resolvedValues


class PendingTransfer:
    def __init__(self, client, id):
        self.client = client
        self._id = id
        self.loader = PendingTransferLoader(client, id)

    @property
    def id(self):
        return self._id

    @property
    def sender(self):
        if self.client.asyncio:
            res = self.loader.load("sender{id}")
        else:
            res = self.client.query('{pendingTransfer(id:"%s"){sender{id}}}' % self._id, keys=[
                "pendingTransfer", "sender"])

        def wrapper(res):
            from .user import User
            return User(self.client, res["id"])

        return wrapWith(res, wrapper)

    @property
    def recipient(self):
        if self.client.asyncio:
            res = self.loader.load("recipient{id}")
        else:
            res = self.client.query('{pendingTransfer(id:"%s"){recipient{id}}}' % self._id, keys=[
                "pendingTransfer", "recipient"])

        def wrapper(res):
            from .user import User
            return User(self.client, res["id"])

        return wrapWith(res, wrapper)

    @property
    def collection(self):
        if self.client.asyncio:
            res = self.loader.load("collection{id}")
        else:
            res = self.client.query('{pendingTransfer(id:"%s"){collection{id}}}' % self._id, keys=[
                "pendingTransfer", "collection"])

        def wrapper(res):
            from .collection import Collection
            return Collection(self.client, res["id"])

        return wrapWith(res, wrapper)


class UserPendingTransferList:
    def __init__(self, client, userId):
        self.client = client
        self.current = 0
        self.userId = userId

    def __len__(self):
        res = self.client.query('{user(id:%s){pendingTransferCount}}' % (self.userId), keys=[
                                "user", "pendingTransferCount"])
        return res

    def __getitem__(self, i):
        if isinstance(i, int):
            res = self.client.query(
                '{user(id:%s){pendingTransfers(limit:1, offset:%d){id}}}' % (self.userId, i))
            if len(res["user"]["pendingTransfers"]) != 1:
                raise IndexError()
            return PendingTransfer(self.client, res["user"]["pendingTransfers"][0]["id"])
        elif isinstance(i, slice):
            start, end, _ = i.indices(len(self))
            res = self.client.query(
                '{user(id:%s){pendingTransfers(offset:%d, limit:%d){id}}}' % (self.userId, start, end-start))
            return [PendingTransfer(self.client, ownerChange["id"]) for ownerChange in res["user"]["pendingTransfers"]]
        else:
            raise TypeError("Unexpected type {} passed as index".format(i))

    def __iter__(self):
        return self

    def __next__(self):
        res = self.client.query(
            '{user(id:%s){pendingTransfers(limit:1, offset:%d){id}}}' % (self.userId, self.current))

        if len(res["user"]["pendingTransfers"]) != 1:
            raise StopIteration

        self.current += 1
        return PendingTransfer(self.client, res["user"]["pendingTransfers"][0]["id"])

    def next(self):
        return self.__next__()
