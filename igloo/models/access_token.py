
from aiodataloader import DataLoader
from igloo.models.utils import wrapWith


class AccessTokenLoader(DataLoader):
    def __init__(self, client, id):
        super().__init__()
        self.client = client
        self._id = id

    async def batch_load_fn(self, keys):
        fields = " ".join(set(keys))
        res = await self.client.query('{accessToken(id:"%s"){%s}}' % (self._id, fields), keys=["accessToken"])

        # if fetching object the key will be the first part of the field
        # e.g. when fetching thing{id} the result is in the thing key
        resolvedValues = [res[key.split("{")[0]] for key in keys]

        return resolvedValues


class AccessToken:
    def __init__(self, client, id):
        self.client = client
        self._id = id
        self.loader = AccessTokenLoader(client, id)

    @property
    def id(self):
        return self._id

    @property
    def user(self):
        if self.client.asyncio:
            res = self.loader.load("user{id}")
        else:
            res = self.client.query('{accessToken(id:"%s"){user{id}}}' % self._id, keys=[
                "accessToken", "user"])

        from .user import User

        def wrapper(res):
            return User(self.client, res["id"])

        return wrapWith(res, wrapper)

    @property
    def name(self):
        if self.client.asyncio:
            return self.loader.load("name")
        else:
            return self.client.query('{accessToken(id:"%s"){name}}' % self._id, keys=[
                "accessToken", "name"])

    @property
    def createdAt(self):
        if self.client.asyncio:
            return self.loader.load("createdAt")
        else:
            return self.client.query('{accessToken(id:"%s"){createdAt}}' % self._id, keys=[
                "accessToken", "createdAt"])

    @property
    def updatedAt(self):
        if self.client.asyncio:
            return self.loader.load("updatedAt")
        else:
            return self.client.query('{accessToken(id:"%s"){updatedAt}}' % self._id, keys=[
                "accessToken", "updatedAt"])

    @property
    def lastUsed(self):
        if self.client.asyncio:
            return self.loader.load("lastUsed")
        else:
            return self.client.query('{accessToken(id:"%s"){lastUsed}}' % self._id, keys=[
                "accessToken", "lastUsed"])


class AccessTokenList:
    def __init__(self, client, userId):
        self.client = client
        self.current = 0
        self.userId = userId

    def __len__(self):
        res = self.client.query(
            '{user(id:%s){accessTokenCount}}' % self.userId)
        return res["user"]["accessTokenCount"]

    def __getitem__(self, i):
        if isinstance(i, int):
            res = self.client.query(
                '{user(id:%s){accessTokens(limit:1, offset:%d){id}}}' % (self.userId, i))
            if len(res["user"]["accessTokens"]) != 1:
                raise IndexError()
            return AccessToken(self.client, res["user"]["accessTokens"][0]["id"])
        elif isinstance(i, slice):
            start, end, _ = i.indices(len(self))
            res = self.client.query(
                '{user(id:%s){accessTokens(offset:%d, limit:%d){id}}}' % (self.userId, start, end-start))
            return [AccessToken(self.client, token["id"]) for token in res["user"]["accessTokens"]]
        else:
            raise TypeError("Unexpected type {} passed as index".format(i))

    def __iter__(self):
        return self

    def __next__(self):
        res = self.client.query(
            '{user(id:%s){accessTokens(limit:1, offset:%d){id}}}' % (self.userId, self.current))

        if len(res["user", "accessTokens"]) != 1:
            raise StopIteration

        self.current += 1
        return AccessToken(self.client, res["user"]["accessTokens"][0]["id"])

    def next(self):
        return self.__next__()
