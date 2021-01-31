from igloo.models.utils import wrapWith
from igloo.utils import get_representation
from aiodataloader import DataLoader


class CollectionLoader(DataLoader):
    def __init__(self, client, id):
        super().__init__()
        self.client = client
        self._id = id

    async def batch_load_fn(self, keys):
        fields = " ".join(set(keys))
        res = await self.client.query('{collection(id:"%s"){%s}}' % (self._id, fields), keys=["collection"])

        resolvedValues = [res[key.split("{")[0]] for key in keys]

        return resolvedValues


class Collection:
    def __init__(self, client, id):
        self.client = client
        self._id = id
        self.loader = CollectionLoader(client, id)

    @property
    def id(self):
        return self._id

    @property
    def createdAt(self):
        if self.client.asyncio:
            return self.loader.load("createdAt")
        else:
            return self.client.query('{collection(id:"%s"){createdAt}}' % self._id, keys=[
                "collection", "createdAt"])

    @property
    def updatedAt(self):
        if self.client.asyncio:
            return self.loader.load("updatedAt")
        else:
            return self.client.query('{collection(id:"%s"){updatedAt}}' % self._id, keys=[
                "collection", "updatedAt"])

    @property
    def name(self):
        if self.client.asyncio:
            return self.loader.load("name")
        else:
            return self.client.query('{collection(id:"%s"){name}}' % self._id, keys=[
                "collection", "name"])

    @name.setter
    def name(self, newName):
        self.client.mutation(
            'mutation{updateCollection(id:"%s", name:"%s"){id}}' % (self._id, newName), asyncio=False)

    @property
    def owner(self):
        if self.client.asyncio:
            res = self.loader.load("owner{id}")
        else:
            res = self.client.query('{collection(id:"%s"){owner{id}}}' % self._id, keys=[
                "collection", "owner"])

        def wrapper(res):
            from .user import User
            res = User(self.client, res["id"])

            return res

        return wrapWith(res, wrapper)

    @property
    def my_role(self):
        if self.client.asyncio:
            return self.loader.load("myRole")
        else:
            return self.client.query('{collection(id:"%s"){myRole}}' % self._id, keys=[
                "collection", "myRole"])

    @property
    def picture(self):
        if self.client.asyncio:
            return self.loader.load("picture")
        else:
            return self.client.query('{collection(id:"%s"){picture}}' % self._id, keys=[
                "collection", "picture"])

    @picture.setter
    def picture(self, newPicture):
        self.client.mutation(
            'mutation{updateCollection(id:"%s", picture:"%s"){id}}' % (self._id, newPicture), asyncio=False)

    @property
    def unique_firmwares(self):
        if self.client.asyncio:
            return self.loader.load("uniqueFirmwares")
        else:
            return self.client.query('{collection(id:"%s"){uniqueFirmwares}}' % self._id, keys=[
                "collection", "uniqueFirmwares"])

    @property
    def index(self):
        if self.client.asyncio:
            return self.loader.load("index")
        else:
            return self.client.query('{collection(id:"%s"){index}}' % self._id, keys=[
                "collection", "index"])

    @index.setter
    def index(self, newIndex):
        self.client.mutation(
            'mutation{updateCollection(id:"%s", index:%s){id}}' % (self._id, newIndex), asyncio=False)

    @property
    def muted(self):
        if self.client.asyncio:
            return self.loader.load("muted")
        else:
            return self.client.query('{collection(id:"%s"){muted}}' % self._id, keys=[
                "collection", "muted"])

    @muted.setter
    def muted(self, newMuted):
        self.client.mutation(
            'mutation{updateCollection(id:"%s", muted:%s){id}}' % (self._id, "true" if newMuted else "false"), asyncio=False)

    @property
    def things(self):
        from .thing import CollectionThingList
        return CollectionThingList(self.client, self._id)

    @property
    def editors(self):
        from .user import CollectionEditorList
        return CollectionEditorList(self.client, self._id)

    @property
    def viewers(self):
        from .user import CollectionViewerList
        return CollectionViewerList(self.client, self._id)

    @property
    def pending_shares(self):
        from .pending_share import CollectionPendingShareList
        return CollectionPendingShareList(self.client, self._id)

    @property
    def pending_transfer(self):
        if self.client.asyncio:
            res = self.loader.load("pendingTransfer{id}")
        else:
            res = self.client.query('{collection(id:"%s"){pendingTransfer{id}}}' % self._id, keys=[
                "collection", "pendingTransfer"])

        def wrapper(res):
            from .pending_transfer import PendingTransfer
            res = PendingTransfer(self.client, res["id"])

            return res

        return wrapWith(res, wrapper)


class CollectionList:
    def __init__(self, client, userId):
        self.client = client
        self.current = 0
        self._filter = "{}"
        self.userId = userId

    def filter(self, _filter):
        self._filter = get_representation(_filter)
        return self

    def __len__(self):
        res = self.client.query('{user(id:%s){collectionCount(filter:%s)}}' % (self.userId, self._filter), keys=[
                                "user", "collectionCount"])
        return res

    def __getitem__(self, i):
        if isinstance(i, int):
            res = self.client.query(
                '{user(id:%s){collections(limit:1, offset:%d, filter:%s){id}}}' % (self.userId, i, self._filter))
            if len(res["user"]["collections"]) != 1:
                raise IndexError()
            return Collection(self.client, res["user"]["collections"][0]["id"])
        elif isinstance(i, slice):
            start, end, _ = i.indices(len(self))
            res = self.client.query(
                '{user(id:%s){collections(offset:%d, limit:%d, filter:%s){id}}}' % (self.userId, start, end-start, self._filter))
            return [Collection(self.client, collection["id"]) for collection in res["user"]["collections"]]
        else:
            raise TypeError("Unexpected type {} passed as index".format(i))

    def __iter__(self):
        return self

    def __next__(self):
        res = self.client.query(
            '{user(id:%s){collections(limit:1, offset:%d, filter:%s){id}}}' % (self.userId, self.current, self._filter))

        if len(res["user"]["collections"]) != 1:
            raise StopIteration

        self.current += 1
        return Collection(self.client, res["user"]["collections"][0]["id"])

    def next(self):
        return self.__next__()
