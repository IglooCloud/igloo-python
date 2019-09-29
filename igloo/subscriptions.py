# proigloogrammatically generated file
from igloo.models.user import User
from igloo.models.permanent_token import PermanentToken
from igloo.models.pending_environment_share import PendingEnvironmentShare
from igloo.models.environment import Environment
from igloo.models.thing import Thing
from igloo.models.value import Value
from igloo.models.float_value import FloatVariable
from igloo.models.notification import Notification
from igloo.models.boolean_value import BooleanVariable
from igloo.models.string_value import StringVariable
from igloo.models.float_series_value import FloatSeriesVariable
from igloo.models.category_series_value import CategorySeriesVariable
from igloo.models.category_series_node import CategorySeriesNode
from igloo.models.file_value import FileVariable
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

    async def permanentTokenCreated(self, ):
        async for data in self.client.subscribe(('subscription{permanentTokenCreated(){id}}' % ()).replace('()', '')):
            yield PermanentToken(self.client, data["permanentTokenCreated"]["id"])

    async def notificationCreated(self, ):
        async for data in self.client.subscribe(('subscription{notificationCreated(){id}}' % ()).replace('()', '')):
            yield Notification(self.client, data["notificationCreated"]["id"])

    async def thingMoved(self, environmentId=None, id=None):
        environmentId_arg = parse_arg("environmentId", environmentId)
        id_arg = parse_arg("id", id)

        async for data in self.client.subscribe(('subscription{thingMoved(%s%s){id}}' % (environmentId_arg, id_arg)).replace('()', '')):
            yield Thing(self.client, data["thingMoved"]["id"])

    async def pendingEnvironmentShareReceived(self, ):
        async for data in self.client.subscribe(('subscription{pendingEnvironmentShareReceived(){id}}' % ()).replace('()', '')):
            yield PendingEnvironmentShare(self.client, data["pendingEnvironmentShareReceived"]["id"])

    async def pendingEnvironmentShareUpdated(self, ):
        async for data in self.client.subscribe(('subscription{pendingEnvironmentShareUpdated(){id}}' % ()).replace('()', '')):
            yield PendingEnvironmentShare(self.client, data["pendingEnvironmentShareUpdated"]["id"])

    async def pendingEnvironmentShareAccepted(self, ):
        async for data in self.client.subscribe(('subscription{pendingEnvironmentShareAccepted(){id sender receiver role environment}}' % ()).replace('()', '')):
            yield data["pendingEnvironmentShareAccepted"]

    async def pendingEnvironmentShareDeclined(self, ):
        async for data in self.client.subscribe(('subscription{pendingEnvironmentShareDeclined()}' % ()).replace('()', '')):
            yield data["pendingEnvironmentShareDeclined"]

    async def pendingEnvironmentShareRevoked(self, ):
        async for data in self.client.subscribe(('subscription{pendingEnvironmentShareRevoked()}' % ()).replace('()', '')):
            yield data["pendingEnvironmentShareRevoked"]

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

    async def permanentTokenDeleted(self, ):
        async for data in self.client.subscribe(('subscription{permanentTokenDeleted()}' % ()).replace('()', '')):
            yield data["permanentTokenDeleted"]

    async def notificationDeleted(self, thingId=None, id=None):
        thingId_arg = parse_arg("thingId", thingId)
        id_arg = parse_arg("id", id)

        async for data in self.client.subscribe(('subscription{notificationDeleted(%s%s)}' % (thingId_arg, id_arg)).replace('()', '')):
            yield data["notificationDeleted"]

    async def keepOnline(self, thingId):
        thingId_arg = parse_arg("thingId", thingId)

        async for data in self.client.subscribe(('subscription{keepOnline(%s)}' % (thingId_arg)).replace('()', '')):
            yield data["keepOnline"]
