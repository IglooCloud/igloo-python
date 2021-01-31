from aiodataloader import DataLoader
from igloo.models.utils import wrapWith
from igloo.utils import get_representation


class PendingShareLoader(DataLoader):
    def __init__(self, client, id):
        super().__init__()
        self.client = client
        self._id = id

    async def batch_load_fn(self, keys):
        fields = " ".join(set(keys))
        res = await self.client.query('{pendingShare(id:"%s"){%s}}' % (self._id, fields), keys=["pendingShare"])

        # if fetching object the key will be the first part of the field
        # e.g. when fetching thing{id} the result is in the thing key
        resolvedValues = [res[key.split("{")[0]] for key in keys]

        return resolvedValues


class PendingShare:
    def __init__(self, client, id):
        self.client = client
        self._id = id
        self.loader = PendingShareLoader(client, id)

    @property
    def id(self):
        return self._id

    @property
    def role(self):
        if self.client.asyncio:
            return self.loader.load("role")
        else:
            return self.client.query('{pendingShare(id:"%s"){role}}' % self._id, keys=[
                "pendingShare", "role"])

    @role.setter
    def role(self, newContent):
        self.client.mutation(
            'mutation{notification(id:"%s", role:"%s"){id}}' % (self._id, newContent), asyncio=False)

    @property
    def createdAt(self):
        if self.client.asyncio:
            return self.loader.load("createdAt")
        else:
            return self.client.query('{pendingShare(id:"%s"){createdAt}}' % self._id, keys=[
                "pendingShare", "createdAt"])

    @property
    def updatedAt(self):
        if self.client.asyncio:
            return self.loader.load("updatedAt")
        else:
            return self.client.query('{pendingShare(id:"%s"){updatedAt}}' % self._id, keys=[
                "pendingShare", "updatedAt"])

    @property
    def sender(self):
        if self.client.asyncio:
            res = self.loader.load("sender{id}")
        else:
            res = self.client.query('{pendingShare(id:"%s"){sender{id}}}' % self._id, keys=[
                "pendingShare", "sender"])

        def wrapper(res):
            from .user import User
            return User(self.client, res["id"])

        return wrapWith(res, wrapper)

    @property
    def recipient(self):
        if self.client.asyncio:
            res = self.loader.load("recipient{id}")
        else:
            res = self.client.query('{pendingShare(id:"%s"){recipient{id}}}' % self._id, keys=[
                "pendingShare", "recipient"])

        def wrapper(res):
            from .user import User
            return User(self.client, res["id"])

        return wrapWith(res, wrapper)

    @property
    def collection(self):
        if self.client.asyncio:
            res = self.loader.load("collection{id}")
        else:
            res = self.client.query('{pendingShare(id:"%s"){collection{id}}}' % self._id, keys=[
                "pendingShare", "collection"])

        def wrapper(res):
            from .collection import Collection
            return Collection(self.client, res["id"])

        return wrapWith(res, wrapper)


class UserPendingShareList:
    def __init__(self, client, userId):
        self.client = client
        self.current = 0
        self.userId = userId

    def __len__(self):
        res = self.client.query('{user(id:%s){pendingShareCount}}' % self.userId, keys=[
                                "user", "pendingShareCount"])
        return res

    def __getitem__(self, i):
        if isinstance(i, int):
            res = self.client.query(
                '{user(id:%s){pendingShares(limit:1, offset:%d){id}}}' % (self.userId, i))
            if len(res["user"]["pendingShares"]) != 1:
                raise IndexError()
            return PendingShare(self.client, res["user"]["pendingShares"][0]["id"])
        elif isinstance(i, slice):
            start, end, _ = i.indices(len(self))
            res = self.client.query(
                '{user(id:%s){pendingShares(offset:%d, limit:%d){id}}}' % (self.userId, start, end-start))
            return [PendingShare(self.client, pendingShare["id"]) for pendingShare in res["user"]["pendingShares"]]
        else:
            raise TypeError("Unexpected type {} passed as index".format(i))

    def __iter__(self):
        return self

    def __next__(self):
        res = self.client.query(
            '{user(id:%s){pendingShares(limit:1, offset:%d){id}}}' % (self.userId, self.current))

        if len(res["user"]["pendingShares"]) != 1:
            raise StopIteration

        self.current += 1
        return PendingShare(self.client, res["user"]["pendingShares"][0]["id"])

    def next(self):
        return self.__next__()


class CollectionPendingShareList:
    def __init__(self, client, collectionId):
        self.client = client
        self.current = 0
        self.collectionId = collectionId
        self._filter = "{}"

    def filter(self, _filter):
        self._filter = get_representation(_filter)
        return self

    def __len__(self):
        res = self.client.query('{collection(id:"%s"){pendingShareCount(filter:%s)}}' % (self.collectionId, self._filter), keys=[
                                "collection", "pendingShareCount"])
        return res

    def __getitem__(self, i):
        if isinstance(i, int):
            res = self.client.query(
                '{collection(id:"%s"){pendingShares(limit:1, offset:%d, filter:%s){id}}}' % (self.collectionId, i, self._filter))
            if len(res["collection"]["pendingShares"]) != 1:
                raise IndexError()
            return PendingShare(self.client, res["collection"]["pendingShares"][0]["id"])
        elif isinstance(i, slice):
            start, end, _ = i.indices(len(self))
            res = self.client.query(
                '{collection(id:"%s"){pendingShares(offset:%d, limit:%d, filter:%s){id}}}' % (self.collectionId, start, end-start, self._filter))
            return [PendingShare(self.client, pendingShare["id"]) for pendingShare in res["collection"]["pendingShares"]]
        else:
            raise TypeError("Unexpected type {} passed as index".format(i))

    def __iter__(self):
        return self

    def __next__(self):
        res = self.client.query(
            '{collection(id:"%s"){pendingShares(limit:1, offset:%d, filter:%s){id}}}' % (self.collectionId, self.current, self._filter))

        if len(res["collection"]["pendingShares"]) != 1:
            raise StopIteration

        self.current += 1
        return PendingShare(self.client, res["collection"]["pendingShares"][0]["id"])

    def next(self):
        return self.__next__()
