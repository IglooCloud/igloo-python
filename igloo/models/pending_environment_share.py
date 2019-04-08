
from aiodataloader import DataLoader


class PendingEnvironmentShareLoader(DataLoader):
    def __init__(self, client, id):
        super().__init__()
        self.client = client
        self._id = id

    async def batch_load_fn(self, keys):
        fields = " ".join(set(keys))
        res = await self.client.query('{pendingEnvironmentShare(id:"%s"){%s}}' % (self._id, fields), keys=["pendingEnvironmentShare"])

        # if fetching object the key will be the first part of the field
        # e.g. when fetching device{id} the result is in the device key
        resolvedValues = [res[key.split("{")[0]] for key in keys]

        return resolvedValues


class PendingEnvironmentShare:
    def __init__(self, client, id):
        self.client = client
        self._id = id
        self.loader = PendingEnvironmentShareLoader(client, id)

    @property
    def id(self):
        return self._id

    @property
    def role(self):
        if self.client.asyncio:
            return self.loader.load("role")
        else:
            return self.client.query('{pendingEnvironmentShare(id:"%s"){role}}' % self._id, keys=[
                "pendingEnvironmentShare", "role"])


class UserPendingEnvironmentShareList:
    def __init__(self, client):
        self.client = client
        self.current = 0

    def __len__(self):
        res = self.client.query('{user{pendingEnvironmentShareCount}}', keys=[
                                "user", "pendingEnvironmentShareCount"])
        return res

    def __getitem__(self, i):
        if isinstance(i, int):
            res = self.client.query(
                '{user{pendingEnvironmentShares(limit:1, offset:%d){id}}}' % i)
            if len(res["user"]["pendingEnvironmentShares"]) != 1:
                raise IndexError()
            return PendingEnvironmentShare(self.client, res["user"]["pendingEnvironmentShares"][0]["id"])
        elif isinstance(i, slice):
            start, end, _ = i.indices(len(self))
            res = self.client.query(
                '{user{pendingEnvironmentShares(offset:%d, limit:%d){id}}}' % (start, end-start))
            return [PendingEnvironmentShare(self.client, pendingShare["id"]) for pendingShare in res["user"]["pendingEnvironmentShares"]]
        else:
            print("i", type(i))
            raise TypeError("Unexpected type {} passed as index".format(i))

    def __iter__(self):
        return self

    def __next__(self):
        res = self.client.query(
            '{user{pendingEnvironmentShares(limit:1, offset:%d){id}}}' % self.current)

        if len(res["user"]["pendingEnvironmentShares"]) != 1:
            raise StopIteration

        self.current += 1
        return PendingEnvironmentShare(self.client, res["user"]["pendingEnvironmentShares"][0]["id"])

    def next(self):
        return self.__next__()