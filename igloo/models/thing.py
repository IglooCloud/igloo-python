
from aiodataloader import DataLoader
from igloo.models.utils import wrapWith
from igloo.utils import get_representation


class ThingLoader(DataLoader):
    def __init__(self, client, id):
        super().__init__()
        self.client = client
        self._id = id

    async def batch_load_fn(self, keys):
        fields = " ".join(set(keys))
        res = await self.client.query('{thing(id:"%s"){%s}}' % (self._id, fields), keys=["thing"])

        resolvedValues = [res[key.split("{")[0]] for key in keys]

        return resolvedValues


class Thing:
    def __init__(self, client, id):
        self.client = client
        self._id = id
        self.loader = ThingLoader(client, id)

    @property
    def id(self):
        return self._id

    @property
    def createdAt(self):
        if self.client.asyncio:
            return self.loader.load("createdAt")
        else:
            return self.client.query('{thing(id:"%s"){createdAt}}' % self._id, keys=[
                "thing", "createdAt"])

    @property
    def updatedAt(self):
        if self.client.asyncio:
            return self.loader.load("updatedAt")
        else:
            return self.client.query('{thing(id:"%s"){updatedAt}}' % self._id, keys=[
                "thing", "updatedAt"])

    @property
    def thingType(self):
        if self.client.asyncio:
            return self.loader.load("thingType")
        else:
            return self.client.query('{thing(id:"%s"){thingType}}' %
                                     self._id, keys=["thing", "thingType"])

    @thingType.setter
    def thingType(self, newThingType):
        self.client.mutation(
            'mutation{thing(id:"%s", thingType:"%s"){id}}' % (self._id, newThingType), asyncio=False)

    @property
    def myRole(self):
        if self.client.asyncio:
            return self.loader.load("myRole")
        else:
            return self.client.query('{thing(id:"%s"){myRole}}' %
                                     self._id, keys=["thing", "myRole"])

    @property
    def starred(self):
        if self.client.asyncio:
            return self.loader.load("starred")
        else:
            return self.client.query('{thing(id:"%s"){starred}}' %
                                     self._id, keys=["thing", "starred"])

    @starred.setter
    def starred(self, newValue):
        self.client.mutation(
            'mutation{thing(id:"%s", starred:%s){id}}' % (self._id, "true" if newValue else "false"), asyncio=False)

    @property
    def name(self):
        if self.client.asyncio:
            return self.loader.load("name")
        else:
            return self.client.query('{thing(id:"%s"){name}}' %
                                     self._id, keys=["thing", "name"])

    @name.setter
    def name(self, newName):
        self.client.mutation(
            'mutation{thing(id:"%s", name:"%s"){id}}' % (self._id, newName), asyncio=False)

    @property
    def index(self):
        if self.client.asyncio:
            return self.loader.load("index")
        else:
            return self.client.query('{thing(id:"%s"){index}}' %
                                     self._id, keys=["thing", "index"])

    @index.setter
    def index(self, newValue):
        self.client.mutation(
            'mutation{thing(id:"%s", index:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def online(self):
        if self.client.asyncio:
            return self.loader.load("online")
        else:
            return self.client.query('{thing(id:"%s"){online}}' %
                                     self._id, keys=["thing", "online"])

    @property
    def storageUsed(self):
        if self.client.asyncio:
            return self.loader.load("storageUsed")
        else:
            return self.client.query('{thing(id:"%s"){storageUsed}}' %
                                     self._id, keys=["thing", "storageUsed"])

    @property
    def signalStatus(self):
        if self.client.asyncio:
            return self.loader.load("signalStatus")
        else:
            return self.client.query('{thing(id:"%s"){signalStatus}}' %
                                     self._id, keys=["thing", "signalStatus"])

    @signalStatus.setter
    def signalStatus(self, newValue):
        self.client.mutation(
            'mutation{thing(id:"%s", signalStatus:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def batteryStatus(self):
        if self.client.asyncio:
            return self.loader.load("batteryStatus")
        else:
            return self.client.query('{thing(id:"%s"){batteryStatus}}' %
                                     self._id, keys=["thing", "batteryStatus"])

    @batteryStatus.setter
    def batteryStatus(self, newValue):
        self.client.mutation(
            'mutation{thing(id:"%s", batteryStatus:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def batteryCharging(self):
        if self.client.asyncio:
            return self.loader.load("batteryCharging")
        else:
            return self.client.query('{thing(id:"%s"){batteryCharging}}' %
                                     self._id, keys=["thing", "batteryCharging"])

    @batteryCharging.setter
    def batteryCharging(self, newValue):
        self.client.mutation(
            'mutation{thing(id:"%s", batteryCharging:%s){id}}' % (self._id, "true" if newValue else "false"), asyncio=False)

    @property
    def firmware(self):
        if self.client.asyncio:
            return self.loader.load("firmware")
        else:
            return self.client.query('{thing(id:"%s"){firmware}}' %
                                     self._id, keys=["thing", "firmware"])

    @firmware.setter
    def firmware(self, newValue):
        self.client.mutation(
            'mutation{thing(id:"%s", firmware:"%s"){id}}' % (self._id, newValue), asyncio=False)

    @property
    def muted(self):
        if self.client.asyncio:
            return self.loader.load("muted")
        else:
            return self.client.query('{thing(id:"%s"){muted}}' %
                                     self._id, keys=["thing", "muted"])

    @muted.setter
    def muted(self, newValue):
        self.client.mutation(
            'mutation{thing(id:"%s", muted:%s){id}}' % (self._id, "true" if newValue else "false"), asyncio=False)

    @property
    def qrCode(self):
        if self.client.asyncio:
            return self.loader.load("qrCode")
        else:
            return self.client.query('{thing(id:"%s"){qrCode}}' %
                                     self._id, keys=["thing", "qrCode"])

    @property
    def claimCode(self):
        if self.client.asyncio:
            return self.loader.load("claimCode")
        else:
            return self.client.query('{thing(id:"%s"){claimCode}}' %
                                     self._id, keys=["thing", "claimCode"])

    @property
    def claimed(self):
        if self.client.asyncio:
            return self.loader.load("claimed")
        else:
            return self.client.query('{thing(id:"%s"){claimed}}' %
                                     self._id, keys=["thing", "claimed"])

    @property
    def environment(self):
        from .environment import Environment

        if self.client.asyncio:
            res = self.loader.load("environment{id}")
        else:
            res = self.client.query('{thing(id:"%s"){environment{id}}}' %
                                    self._id, keys=["thing", "environment"])

        def wrapper(res):
            return Environment(self.client, res["id"])

        return wrapWith(res, wrapper)

    @property
    def notifications(self):
        from .notification import ThingNotificationList
        return ThingNotificationList(self.client, self.id)

    @property
    def lastNotification(self):
        from .notification import Notification

        if self.client.asyncio:
            res = self.loader.load("lastNotification{id}")
        else:
            res = self.client.query('{thing(id:"%s"){lastNotification{id}}}' %
                                    self._id, keys=["thing", "lastNotification"])

        def wrapper(res):
            return Notification(self.client, res["id"])

        return wrapWith(res, wrapper)

    @property
    def values(self):
        from .value import ThingValuesList
        return ThingValuesList(self.client, self.id)

    async def keepOnline(self):
        async for _ in self.client.subscription_root.keepOnline(self._id):
            pass


class EnvironmentThingList:
    def __init__(self, client, environmentId):
        self.client = client
        self.environmentId = environmentId
        self.current = 0
        self._filter = "{}"

    def filter(self, _filter):
        self._filter = get_representation(_filter)
        return self

    def __len__(self):
        res = self.client.query(
            '{environment(id:"%s"){thingCount(filter:%s)}}' % (self.environmentId, self._filter))
        return res["environment"]["thingCount"]

    def __getitem__(self, i):
        if isinstance(i, int):
            res = self.client.query(
                '{environment(id:"%s"){things(limit:1, offset:%d, filter:%s){id}}}' % (self.environmentId, i, self._filter))
            if len(res["environment"]["things"]) != 1:
                raise IndexError()
            return Thing(self.client, res["environment"]["things"][0]["id"])
        elif isinstance(i, slice):
            start, end, _ = i.indices(len(self))
            res = self.client.query(
                '{environment(id:"%s"){things(offset:%d, limit:%d, filter:%s){id}}}' % (self.environmentId, start, end-start, self._filter))
            return [Thing(self.client, thing["id"]) for thing in res["environment"]["things"]]
        else:
            raise TypeError("Unexpected type {} passed as index".format(i))

    def __iter__(self):
        return self

    def __next__(self):
        res = self.client.query(
            '{environment(id:"%s"){things(limit:1, offset:%d, filter:%s){id}}}' % (self.environmentId, self.current, self._filter))

        if len(res["environment", "things"]) != 1:
            raise StopIteration

        self.current += 1
        return Thing(self.client, res["environment"]["things"][0]["id"])

    def next(self):
        return self.__next__()


class DeveloperThingList:
    def __init__(self, client, userId):
        self.client = client
        self.current = 0
        self._filter = "{}"
        self.userId = userId

    def filter(self, _filter):
        self._filter = get_representation(_filter)
        return self

    def __len__(self):
        res = self.client.query(
            '{user(id:%s){developerThingCount(filter:%s)}}' % (self.userId, self._filter))
        return res["user"]["developerThingCount"]

    def __getitem__(self, i):
        if isinstance(i, int):
            res = self.client.query(
                '{user(id:%s){developerThings(limit:1, offset:%d, filter:%s){id}}}' % (self.userId, i, self._filter))
            if len(res["user"]["developerThings"]) != 1:
                raise IndexError()
            return Thing(self.client, res["user"]["developerThings"][0]["id"])
        elif isinstance(i, slice):
            start, end, _ = i.indices(len(self))
            res = self.client.query(
                '{user(id:%s){developerThings(offset:%d, limit:%d, filter:%s){id}}}' % (self.userId, start, end-start, self._filter))
            return [Thing(self.client, thing["id"]) for thing in res["user"]["developerThings"]]
        else:
            raise TypeError("Unexpected type {} passed as index".format(i))

    def __iter__(self):
        return self

    def __next__(self):
        res = self.client.query(
            '{user(id:%s){developerThings(limit:1, offset:%d, filter:%s){id}}}' % (self.userId, self.current, self._filter))

        if len(res["user", "developerThings"]) != 1:
            raise StopIteration

        self.current += 1
        return Thing(self.client, res["user"]["developerThings"][0]["id"])

    def next(self):
        return self.__next__()
