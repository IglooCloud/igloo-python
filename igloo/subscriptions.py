# proigloogrammatically generated file
from igloo.models.user import User
from igloo.models.access_token import AccessToken
from igloo.models.pending_share import PendingShare
from igloo.models.environment import Environment
from igloo.models.thing import Thing
from igloo.models.variable import Variable
from igloo.models.float_variable import FloatVariable
from igloo.models.notification import Notification
from igloo.models.boolean_variable import BooleanVariable
from igloo.models.string_variable import StringVariable
from igloo.models.float_series_variable import FloatSeriesVariable
from igloo.models.category_series_variable import CategorySeriesVariable
from igloo.models.category_series_node import CategorySeriesNode
from igloo.models.file_variable import FileVariable
from igloo.models.float_series_node import FloatSeriesNode
from igloo.utils import parse_arg


class SubscriptionRoot:
    def __init__(self, client):
        self.client = client

    async def thingCreated(self, environmentId=None):
        environmentId_arg = parse_arg("environmentId", environmentId)

        async for data in self.client.subscribe(('subscription{thingCreated(%s){id}}' % (environmentId_arg)).replace('()', '')):
            yield Thing(self.client, data["thingCreated"]["id"])

    async def thingClaimed(self, environmentId=None, id=None):
        environmentId_arg = parse_arg("environmentId", environmentId)
        id_arg = parse_arg("id", id)

        async for data in self.client.subscribe(('subscription{thingClaimed(%s%s){id}}' % (environmentId_arg, id_arg)).replace('()', '')):
            yield Thing(self.client, data["thingClaimed"]["id"])

    async def environmentCreated(self, ):
        async for data in self.client.subscribe(('subscription{environmentCreated(){id}}' % ()).replace('()', '')):
            yield Environment(self.client, data["environmentCreated"]["id"])

    async def valueCreated(self, thingId=None, hidden=None):
        thingId_arg = parse_arg("thingId", thingId)
        hidden_arg = parse_arg("hidden", hidden)

        async for data in self.client.subscribe(('subscription{valueCreated(%s%s){id __typename}}' % (thingId_arg, hidden_arg)).replace('()', '')):
            yield Value(self.client, data["valueCreated"]["id"], data["valueCreated"]["__typename"])

    async def floatSeriesNodeCreated(self, seriesId=None):
        seriesId_arg = parse_arg("seriesId", seriesId)

        async for data in self.client.subscribe(('subscription{floatSeriesNodeCreated(%s){id}}' % (seriesId_arg)).replace('()', '')):
            yield FloatSeriesNode(self.client, data["floatSeriesNodeCreated"]["id"])

    async def categorySeriesNodeCreated(self, seriesId=None):
        seriesId_arg = parse_arg("seriesId", seriesId)

        async for data in self.client.subscribe(('subscription{categorySeriesNodeCreated(%s){id}}' % (seriesId_arg)).replace('()', '')):
            yield CategorySeriesNode(self.client, data["categorySeriesNodeCreated"]["id"])

    async def accessTokenCreated(self, ):
        async for data in self.client.subscribe(('subscription{accessTokenCreated(){id}}' % ()).replace('()', '')):
            yield AccessToken(self.client, data["accessTokenCreated"]["id"])

    async def notificationCreated(self, ):
        async for data in self.client.subscribe(('subscription{notificationCreated(){id}}' % ()).replace('()', '')):
            yield Notification(self.client, data["notificationCreated"]["id"])

    async def thingMoved(self, environmentId=None, id=None):
        environmentId_arg = parse_arg("environmentId", environmentId)
        id_arg = parse_arg("id", id)

        async for data in self.client.subscribe(('subscription{thingMoved(%s%s){id}}' % (environmentId_arg, id_arg)).replace('()', '')):
            yield Thing(self.client, data["thingMoved"]["id"])

    async def pendingShareReceived(self, ):
        async for data in self.client.subscribe(('subscription{pendingShareReceived(){id}}' % ()).replace('()', '')):
            yield PendingShare(self.client, data["pendingShareReceived"]["id"])

    async def pendingShareUpdated(self, ):
        async for data in self.client.subscribe(('subscription{pendingShareUpdated(){id}}' % ()).replace('()', '')):
            yield PendingShare(self.client, data["pendingShareUpdated"]["id"])

    async def pendingShareAccepted(self, ):
        async for data in self.client.subscribe(('subscription{pendingShareAccepted(){id sender receiver role environment}}' % ()).replace('()', '')):
            yield data["pendingShareAccepted"]

    async def pendingShareDeclined(self, ):
        async for data in self.client.subscribe(('subscription{pendingShareDeclined()}' % ()).replace('()', '')):
            yield data["pendingShareDeclined"]

    async def pendingShareRevoked(self, ):
        async for data in self.client.subscribe(('subscription{pendingShareRevoked()}' % ()).replace('()', '')):
            yield data["pendingShareRevoked"]

    async def environmentShareDeleted(self, environmentId=None, userId=None):
        environmentId_arg = parse_arg("environmentId", environmentId)
        userId_arg = parse_arg("userId", userId)
        async for data in self.client.subscribe(('subscription{environmentShareDeleted(%s%s){environment{id} user{id}}}' % (environmentId_arg, userId_arg)).replace('()', '')):
            res = data["environmentShareDeleted"]
            res["environment"] = Environment(
                self.client, res["environment"]["id"])
            res["user"] = User(
                self.client, res["user"]["id"])

            yield res

    async def environmentShareUpdated(self, environmentId=None, userId=None):
        environmentId_arg = parse_arg("environmentId", environmentId)
        userId_arg = parse_arg("userId", userId)
        async for data in self.client.subscribe(('subscription{environmentShareUpdated(%s%s){environment{id} user{id} newRole}}' % (environmentId_arg, userId_arg)).replace('()', '')):
            res = data["environmentShareUpdated"]
            res["environment"] = Environment(
                self.client, res["environment"]["id"])
            res["user"] = User(
                self.client, res["user"]["id"])

            yield res

    async def userUpdated(self, id=None):
        id_arg = parse_arg("id", id)

        async for data in self.client.subscribe(('subscription{userUpdated(%s){id}}' % (id_arg)).replace('()', '')):
            yield User(self.client, data["userUpdated"]["id"])

    async def thingUpdated(self, environmentId=None, id=None):
        environmentId_arg = parse_arg("environmentId", environmentId)
        id_arg = parse_arg("id", id)

        async for data in self.client.subscribe(('subscription{thingUpdated(%s%s){id}}' % (environmentId_arg, id_arg)).replace('()', '')):
            yield Thing(self.client, data["thingUpdated"]["id"])

    async def environmentUpdated(self, id=None):
        id_arg = parse_arg("id", id)

        async for data in self.client.subscribe(('subscription{environmentUpdated(%s){id}}' % (id_arg)).replace('()', '')):
            yield Environment(self.client, data["environmentUpdated"]["id"])

    async def valueUpdated(self, thingId=None, id=None, hidden=None):
        thingId_arg = parse_arg("thingId", thingId)
        id_arg = parse_arg("id", id)
        hidden_arg = parse_arg("hidden", hidden)

        async for data in self.client.subscribe(('subscription{valueUpdated(%s%s%s){id __typename}}' % (thingId_arg, id_arg, hidden_arg)).replace('()', '')):
            yield Value(self.client, data["valueUpdated"]["id"], data["valueUpdated"]["__typename"])

    async def floatSeriesNodeUpdated(self, seriesId=None, id=None):
        seriesId_arg = parse_arg("seriesId", seriesId)
        id_arg = parse_arg("id", id)

        async for data in self.client.subscribe(('subscription{floatSeriesNodeUpdated(%s%s){id}}' % (seriesId_arg, id_arg)).replace('()', '')):
            yield FloatSeriesNode(self.client, data["floatSeriesNodeUpdated"]["id"])

    async def categorySeriesNodeUpdated(self, seriesId=None, id=None):
        seriesId_arg = parse_arg("seriesId", seriesId)
        id_arg = parse_arg("id", id)

        async for data in self.client.subscribe(('subscription{categorySeriesNodeUpdated(%s%s){id}}' % (seriesId_arg, id_arg)).replace('()', '')):
            yield CategorySeriesNode(self.client, data["categorySeriesNodeUpdated"]["id"])

    async def notificationUpdated(self, thingId=None, id=None):
        thingId_arg = parse_arg("thingId", thingId)
        id_arg = parse_arg("id", id)

        async for data in self.client.subscribe(('subscription{notificationUpdated(%s%s){id}}' % (thingId_arg, id_arg)).replace('()', '')):
            yield Notification(self.client, data["notificationUpdated"]["id"])

    async def valueDeleted(self, thingId=None, id=None, hidden=None):
        thingId_arg = parse_arg("thingId", thingId)
        id_arg = parse_arg("id", id)
        hidden_arg = parse_arg("hidden", hidden)

        async for data in self.client.subscribe(('subscription{valueDeleted(%s%s%s)}' % (thingId_arg, id_arg, hidden_arg)).replace('()', '')):
            yield data["valueDeleted"]

    async def floatSeriesNodeDeleted(self, seriesId=None, id=None):
        seriesId_arg = parse_arg("seriesId", seriesId)
        id_arg = parse_arg("id", id)

        async for data in self.client.subscribe(('subscription{floatSeriesNodeDeleted(%s%s)}' % (seriesId_arg, id_arg)).replace('()', '')):
            yield data["floatSeriesNodeDeleted"]

    async def categorySeriesNodeDeleted(self, seriesId=None, id=None):
        seriesId_arg = parse_arg("seriesId", seriesId)
        id_arg = parse_arg("id", id)

        async for data in self.client.subscribe(('subscription{categorySeriesNodeDeleted(%s%s)}' % (seriesId_arg, id_arg)).replace('()', '')):
            yield data["categorySeriesNodeDeleted"]

    async def thingDeleted(self, environmentId=None, id=None):
        environmentId_arg = parse_arg("environmentId", environmentId)
        id_arg = parse_arg("id", id)

        async for data in self.client.subscribe(('subscription{thingDeleted(%s%s)}' % (environmentId_arg, id_arg)).replace('()', '')):
            yield data["thingDeleted"]

    async def thingUnclaimed(self, environmentId=None, id=None):
        environmentId_arg = parse_arg("environmentId", environmentId)
        id_arg = parse_arg("id", id)

        async for data in self.client.subscribe(('subscription{thingUnclaimed(%s%s)}' % (environmentId_arg, id_arg)).replace('()', '')):
            yield data["thingUnclaimed"]

    async def environmentDeleted(self, id=None):
        id_arg = parse_arg("id", id)

        async for data in self.client.subscribe(('subscription{environmentDeleted(%s)}' % (id_arg)).replace('()', '')):
            yield data["environmentDeleted"]

    async def userDeleted(self, id=None):
        id_arg = parse_arg("id", id)

        async for data in self.client.subscribe(('subscription{userDeleted(%s)}' % (id_arg)).replace('()', '')):
            yield data["userDeleted"]

    async def accessTokenDeleted(self, ):
        async for data in self.client.subscribe(('subscription{accessTokenDeleted()}' % ()).replace('()', '')):
            yield data["accessTokenDeleted"]

    async def notificationDeleted(self, thingId=None, id=None):
        thingId_arg = parse_arg("thingId", thingId)
        id_arg = parse_arg("id", id)

        async for data in self.client.subscribe(('subscription{notificationDeleted(%s%s)}' % (thingId_arg, id_arg)).replace('()', '')):
            yield data["notificationDeleted"]

    async def keepOnline(self, thingId):
        thingId_arg = parse_arg("thingId", thingId)

        async for data in self.client.subscribe(('subscription{keepOnline(%s)}' % (thingId_arg)).replace('()', '')):
            yield data["keepOnline"]
