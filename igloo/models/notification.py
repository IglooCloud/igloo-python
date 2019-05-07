from aiodataloader import DataLoader
from igloo.models.utils import wrapWith
from igloo.utils import get_representation


class NotificationLoader(DataLoader):
    def __init__(self, client, id):
        super().__init__()
        self.client = client
        self._id = id

    async def batch_load_fn(self, keys):
        fields = " ".join(set(keys))
        res = await self.client.query('{notification(id:"%s"){%s}}' % (self._id, fields), keys=["device"])

        resolvedValues = [res[key] for key in keys]

        return resolvedValues


class Notification:
    def __init__(self, client, id):
        self.client = client
        self._id = id
        self.loader = NotificationLoader(client, id)

    @property
    def id(self):
        return self._id

    @property
    def device(self):
        if self.client.asyncio:
            res = self.loader.load("device{id}")
        else:
            res = self.client.query('{notification(id:"%s"){device{id}}}' % self._id, keys=[
                "notification", "device"])

        def wrapper(res):
            from .device import Device
            return Device(self.client, res["id"])

        return wrapWith(res, wrapper)

    @property
    def content(self):
        if self.client.asyncio:
            return self.loader.load("content")
        else:
            return self.client.query('{notification(id:"%s"){content}}' %
                                     self._id, keys=["notification", "content"])

    @content.setter
    def content(self, newContent):
        self.client.mutation(
            'mutation{notification(id:"%s", content:"%s"){id}}' % (self._id, newContent), asyncio=False)

    @property
    def date(self):
        if self.client.asyncio:
            return self.loader.load("date")
        else:
            return self.client.query('{notification(id:"%s"){date}}' %
                                     self._id, keys=["notification", "date"])

    @property
    def read(self):
        if self.client.asyncio:
            return self.loader.load("read")
        else:
            return self.client.query('{notification(id:"%s"){read}}' %
                                     self._id, keys=["notification", "read"])


class DeviceNotificationList:
    def __init__(self, client, deviceId):
        self.client = client
        self.deviceId = deviceId
        self.current = 0
        self._filter = "{}"

    def filter(self, _filter):
        self._filter = get_representation(_filter)
        return self

    def __len__(self):
        res = self.client.query(
            '{device(id:"%s"){notificationCount(filter:%s)}}' % (self.deviceId, self._filter))
        return res["device"]["notificationCount"]

    def __getitem__(self, i):
        if isinstance(i, int):
            res = self.client.query(
                '{device(id:"%s"){notifications(limit:1, offset:%d, filter:%s){id}}}' % (self.deviceId, i, self._filter))
            if len(res["device"]["notifications"]) != 1:
                raise IndexError()
            return Notification(self.client, res["device"]["notifications"][0]["id"])
        elif isinstance(i, slice):
            start, end, _ = i.indices(len(self))
            res = self.client.query(
                '{device(id:"%s"){notifications(offset:%d, limit:%d, filter:%s){id}}}' % (self.deviceId, start, end-start, self._filter))
            return [Notification(self.client, notification["id"]) for notification in res["device"]["notifications"]]
        else:
            print("i", type(i))
            raise TypeError("Unexpected type {} passed as index".format(i))

    def __iter__(self):
        return self

    def __next__(self):
        res = self.client.query(
            '{device(id:"%s"){notifications(limit:1, offset:%d, filter:%s){id}}}' % (self.deviceId, self.current, self._filter))

        if len(res["device", "notifications"]) != 1:
            raise StopIteration

        self.current += 1
        return Notification(self.client, res["device"]["notifications"][0]["id"])

    def next(self):
        return self.__next__()
