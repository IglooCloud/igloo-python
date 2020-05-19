
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
    def __init__(self, client, id=None):
        self.client = client

        if id is None:
            self._id = self.client.query(
                '{thing{id}}', keys=["thing", "id"], asyncio=False)
        else:
            self._id = id

        self.loader = ThingLoader(client, self._id)

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
    def type(self):
        if self.client.asyncio:
            return self.loader.load("type")
        else:
            return self.client.query('{thing(id:"%s"){type}}' %
                                     self._id, keys=["thing", "type"])

    @type.setter
    def type(self, newThingType):
        self.client.mutation(
            'mutation{thing(id:"%s", type:"%s"){id}}' % (self._id, newThingType), asyncio=False)

    @property
    def my_role(self):
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

    @online.setter
    def online(self, newValue):
        raise Exception(
            "You cannot set `online` directly, use the `keep_online` subscription")

    @property
    def token(self):
        if self.client.asyncio:
            return self.loader.load("token")
        else:
            return self.client.query('{thing(id:"%s"){token}}' %
                                     self._id, keys=["thing", "token"])

    @property
    def used_storage(self):
        if self.client.asyncio:
            return self.loader.load("usedStorage")
        else:
            return self.client.query('{thing(id:"%s"){usedStorage}}' %
                                     self._id, keys=["thing", "usedStorage"])

    @property
    def stored_notifications(self):
        if self.client.asyncio:
            return self.loader.load("storedNotifications")
        else:
            return self.client.query('{thing(id:"%s"){storedNotifications}}' %
                                     self._id, keys=["thing", "storedNotifications"])

    @stored_notifications.setter
    def stored_notifications(self, newValue):
        self.client.mutation(
            'mutation{thing(id:"%s", storedNotifications:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def signal_status(self):
        if self.client.asyncio:
            return self.loader.load("signalStatus")
        else:
            return self.client.query('{thing(id:"%s"){signalStatus}}' %
                                     self._id, keys=["thing", "signalStatus"])

    @signal_status.setter
    def signal_status(self, newValue):
        self.client.mutation(
            'mutation{thing(id:"%s", signalStatus:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def battery_status(self):
        if self.client.asyncio:
            return self.loader.load("batteryStatus")
        else:
            return self.client.query('{thing(id:"%s"){batteryStatus}}' %
                                     self._id, keys=["thing", "batteryStatus"])

    @battery_status.setter
    def battery_status(self, newValue):
        self.client.mutation(
            'mutation{thing(id:"%s", batteryStatus:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def battery_charging(self):
        if self.client.asyncio:
            return self.loader.load("batteryCharging")
        else:
            return self.client.query('{thing(id:"%s"){batteryCharging}}' %
                                     self._id, keys=["thing", "batteryCharging"])

    @battery_charging.setter
    def battery_charging(self, newValue):
        self.client.mutation(
            'mutation{thing(id:"%s", batteryCharging:%s){id}}' % (self._id, "true" if newValue else "false"), asyncio=False)

    @property
    def battery_threshold(self):
        if self.client.asyncio:
            return self.loader.load("batteryThreshold")
        else:
            return self.client.query('{thing(id:"%s"){batteryThreshold}}' %
                                     self._id, keys=["thing", "batteryThreshold"])

    @battery_threshold.setter
    def battery_threshold(self, newValue):
        self.client.mutation(
            'mutation{thing(id:"%s", batteryThreshold:%s){id}}' % (self._id, newValue), asyncio=False)

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
    def qr_code(self):
        if self.client.asyncio:
            return self.loader.load("qrCode")
        else:
            return self.client.query('{thing(id:"%s"){qrCode}}' %
                                     self._id, keys=["thing", "qrCode"])

    @property
    def claim_code(self):
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
    def producer(self):
        from .user import User

        if self.client.asyncio:
            res = self.loader.load("producer{id}")
        else:
            res = self.client.query('{thing(id:"%s"){producer{id}}}' %
                                    self._id, keys=["thing", "producer"])

        def wrapper(res):
            return User(self.client, res["id"])

        return wrapWith(res, wrapper)

    @property
    def notifications(self):
        from .notification import ThingNotificationList
        return ThingNotificationList(self.client, self.id)

    @property
    def last_notification(self):
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
    def variables(self):
        from .variable import ThingVariablesList
        return ThingVariablesList(self.client, self.id)

    async def keep_online(self):
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
