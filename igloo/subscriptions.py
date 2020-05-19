# proigloogrammatically generated file
from igloo.models.user import User
from igloo.models.access_token import AccessToken
from igloo.models.pending_share import PendingShare
from igloo.models.pending_transfer import PendingTransfer
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
from igloo.utils import undefined, parse_arg


class SubscriptionRoot:
    def __init__(self, client):
        self.client = client

    async def thing_created(self, environment_id=undefined):
        environmentId_arg = parse_arg("environmentId", environment_id)

        async for data in self.client.subscribe(('subscription{thingCreated(%s){id}}' % (environmentId_arg)).replace('()', '')):
            yield Thing(self.client, data["thingCreated"]["id"])

    async def thing_claimed(self, environment_id=undefined, id=undefined):
        environmentId_arg = parse_arg(
            "environmentId", environment_id)
        id_arg = parse_arg("id", id)

        async for data in self.client.subscribe(('subscription{thingClaimed(%s%s){id}}' % (environmentId_arg, id_arg)).replace('()', '')):
            yield Thing(self.client, data["thingClaimed"]["id"])

    async def environment_created(self):
        async for data in self.client.subscribe(('subscription{environmentCreated(){id}}' % ()).replace('()', '')):
            yield Environment(self.client, data["environmentCreated"]["id"])

    async def variable_created(self, thing_id=undefined, hidden=undefined):
        thingId_arg = parse_arg("thingId", thing_id)
        hidden_arg = parse_arg("hidden", hidden)

        async for data in self.client.subscribe(('subscription{variableCreated(%s%s){id __typename}}' % (thingId_arg, hidden_arg)).replace('()', '')):
            yield Variable(self.client, data["variableCreated"]["id"], data["variableCreated"]["__typename"])

    async def float_series_node_created(self, series_id=undefined):
        seriesId_arg = parse_arg("seriesId", series_id)

        async for data in self.client.subscribe(('subscription{floatSeriesNodeCreated(%s){id}}' % (seriesId_arg)).replace('()', '')):
            yield FloatSeriesNode(self.client, data["floatSeriesNodeCreated"]["id"])

    async def category_series_node_created(self, series_id=undefined):
        seriesId_arg = parse_arg("seriesId", series_id)

        async for data in self.client.subscribe(('subscription{categorySeriesNodeCreated(%s){id}}' % (seriesId_arg)).replace('()', '')):
            yield CategorySeriesNode(self.client, data["categorySeriesNodeCreated"]["id"])

    async def access_token_created(self):
        async for data in self.client.subscribe(('subscription{accessTokenCreated(){id}}' % ()).replace('()', '')):
            yield AccessToken(self.client, data["accessTokenCreated"]["id"])

    async def notification_created(self):
        async for data in self.client.subscribe(('subscription{notificationCreated(){id}}' % ()).replace('()', '')):
            yield Notification(self.client, data["notificationCreated"]["id"])

    async def thing_moved(self, environment_id=undefined, id=undefined):
        environmentId_arg = parse_arg("environmentId", environment_id)
        id_arg = parse_arg("id", id)

        async for data in self.client.subscribe(('subscription{thingMoved(%s%s){id}}' % (environmentId_arg, id_arg)).replace('()', '')):
            yield Thing(self.client, data["thingMoved"]["id"])

    async def pending_share_created(self, ):
        async for data in self.client.subscribe(('subscription{pendingShareCreated(){id}}' % ()).replace('()', '')):
            yield PendingShare(self.client, data["pendingShareCreated"]["id"])

    async def pending_share_updated(self, ):
        async for data in self.client.subscribe(('subscription{pendingShareUpdated(){id}}' % ()).replace('()', '')):
            yield PendingShare(self.client, data["pendingShareUpdated"]["id"])

    async def pending_share_accepted(self, ):
        async for data in self.client.subscribe(('subscription{pendingShareAccepted(){id sender receiver role environment}}' % ()).replace('()', '')):
            yield data["pendingShareAccepted"]

    async def pending_share_declined(self, ):
        async for data in self.client.subscribe(('subscription{pendingShareDeclined()}' % ()).replace('()', '')):
            yield data["pendingShareDeclined"]

    async def pending_share_revoked(self, ):
        async for data in self.client.subscribe(('subscription{pendingShareRevoked()}' % ()).replace('()', '')):
            yield data["pendingShareRevoked"]

    async def user_left_environment(self, environment_id=undefined, user_id=undefined):
        environmentId_arg = parse_arg("environmentId", environment_id)
        userId_arg = parse_arg("userId", user_id)
        async for data in self.client.subscribe(('subscription{userLeftEnvironment(%s%s){environment{id} user{id}}}' % (environmentId_arg, userId_arg)).replace('()', '')):
            res = data["userLeftEnvironment"]
            res["environment"] = Environment(
                self.client, res["environment"]["id"])
            res["user"] = User(
                self.client, res["user"]["id"])

            yield res

    async def pending_transfer_created(self, ):
        async for data in self.client.subscribe(('subscription{pendingTransferCreated(){id}}' % ()).replace('()', '')):
            yield PendingTransfer(self.client, data["pendingTransferCreated"]["id"])

    async def pending_transfer_accepted(self):
        async for data in self.client.subscribe(('subscription{pendingTransferAccepted(){sender{id} receiver{id} environment{id} id}}').replace('()', '')):
            res = data["pendingTransferAccepted"]
            res["sender"] = User(
                self.client, res["sender"]["id"])
            res["receiver"] = User(
                self.client, res["receiver"]["id"])
            res["environment"] = Environment(
                self.client, res["environment"]["id"])

            yield res

    async def pending_transfer_declined(self, ):
        async for data in self.client.subscribe(('subscription{pendingTransferDeclined()}' % ()).replace('()', '')):
            yield data["pendingTransferDeclined"]

    async def pending_transfer_revoked(self, ):
        async for data in self.client.subscribe(('subscription{pendingTransferRevoked()}' % ()).replace('()', '')):
            yield data["pendingTransferRevoked"]

    async def user_updated(self, id=undefined, email=undefined):
        id_arg = parse_arg("id", id)
        email_arg = parse_arg("email", email)

        async for data in self.client.subscribe(('subscription{userUpdated(%s%s){id}}' % (id_arg, email_arg)).replace('()', '')):
            yield User(self.client, data["userUpdated"]["id"])

    async def thing_updated(self, environment_id=undefined, id=undefined):
        environmentId_arg = parse_arg("environmentId", environment_id)
        id_arg = parse_arg("id", id)

        async for data in self.client.subscribe(('subscription{thingUpdated(%s%s){id}}' % (environmentId_arg, id_arg)).replace('()', '')):
            yield Thing(self.client, data["thingUpdated"]["id"])

    async def environment_updated(self, id=undefined):
        id_arg = parse_arg("id", id)

        async for data in self.client.subscribe(('subscription{environmentUpdated(%s){id}}' % (id_arg)).replace('()', '')):
            yield Environment(self.client, data["environmentUpdated"]["id"])

    async def variable_updated(self, thing_id=undefined, id=undefined, hidden=undefined):
        thingId_arg = parse_arg("thingId", thing_id)
        id_arg = parse_arg("id", id)
        hidden_arg = parse_arg("hidden", hidden)

        async for data in self.client.subscribe(('subscription{variableUpdated(%s%s%s){id __typename}}' % (thingId_arg, id_arg, hidden_arg)).replace('()', '')):
            yield Variable(self.client, data["variableUpdated"]["id"], data["variableUpdated"]["__typename"])

    async def float_series_node_updated(self, series_id=undefined, id=undefined):
        seriesId_arg = parse_arg("seriesId", series_id)
        id_arg = parse_arg("id", id)

        async for data in self.client.subscribe(('subscription{floatSeriesNodeUpdated(%s%s){id}}' % (seriesId_arg, id_arg)).replace('()', '')):
            yield FloatSeriesNode(self.client, data["floatSeriesNodeUpdated"]["id"])

    async def category_series_node_updated(self, series_id=undefined, id=undefined):
        seriesId_arg = parse_arg("seriesId", series_id)
        id_arg = parse_arg("id", id)

        async for data in self.client.subscribe(('subscription{categorySeriesNodeUpdated(%s%s){id}}' % (seriesId_arg, id_arg)).replace('()', '')):
            yield CategorySeriesNode(self.client, data["categorySeriesNodeUpdated"]["id"])

    async def notification_updated(self, thing_id=undefined, id=undefined):
        thingId_arg = parse_arg("thingId", thing_id)
        id_arg = parse_arg("id", id)

        async for data in self.client.subscribe(('subscription{notificationUpdated(%s%s){id}}' % (thingId_arg, id_arg)).replace('()', '')):
            yield Notification(self.client, data["notificationUpdated"]["id"])

    async def variable_deleted(self, thing_id=undefined, id=undefined, hidden=undefined):
        thingId_arg = parse_arg("thingId", thing_id)
        id_arg = parse_arg("id", id)
        hidden_arg = parse_arg("hidden", hidden)

        async for data in self.client.subscribe(('subscription{variableDeleted(%s%s%s)}' % (thingId_arg, id_arg, hidden_arg)).replace('()', '')):
            yield data["variableDeleted"]

    async def float_series_node_deleted(self, series_id=undefined, id=undefined):
        seriesId_arg = parse_arg("seriesId", series_id)
        id_arg = parse_arg("id", id)

        async for data in self.client.subscribe(('subscription{floatSeriesNodeDeleted(%s%s)}' % (seriesId_arg, id_arg)).replace('()', '')):
            yield data["floatSeriesNodeDeleted"]

    async def category_series_node_deleted(self, series_id=undefined, id=undefined):
        seriesId_arg = parse_arg("seriesId", series_id)
        id_arg = parse_arg("id", id)

        async for data in self.client.subscribe(('subscription{categorySeriesNodeDeleted(%s%s)}' % (seriesId_arg, id_arg)).replace('()', '')):
            yield data["categorySeriesNodeDeleted"]

    async def thing_deleted(self, environment_id=undefined, id=undefined):
        environmentId_arg = parse_arg("environmentId", environment_id)
        id_arg = parse_arg("id", id)

        async for data in self.client.subscribe(('subscription{thingDeleted(%s%s)}' % (environmentId_arg, id_arg)).replace('()', '')):
            yield data["thingDeleted"]

    async def thing_unclaimed(self, environment_id=undefined, id=undefined):
        environmentId_arg = parse_arg("environmentId", environment_id)
        id_arg = parse_arg("id", id)

        async for data in self.client.subscribe(('subscription{thingUnclaimed(%s%s)}' % (environmentId_arg, id_arg)).replace('()', '')):
            yield data["thingUnclaimed"]

    async def environment_deleted(self, id=undefined):
        id_arg = parse_arg("id", id)

        async for data in self.client.subscribe(('subscription{environmentDeleted(%s)}' % (id_arg)).replace('()', '')):
            yield data["environmentDeleted"]

    async def user_deleted(self, id=undefined, email=undefined):
        id_arg = parse_arg("id", id)
        email_arg = parse_arg("id", email)

        async for data in self.client.subscribe(('subscription{userDeleted(%s%s)}' % (id_arg, email_arg)).replace('()', '')):
            yield data["userDeleted"]

    async def access_token_deleted(self, ):
        async for data in self.client.subscribe(('subscription{accessTokenDeleted()}' % ()).replace('()', '')):
            yield data["accessTokenDeleted"]

    async def notification_deleted(self, thing_id=undefined, id=undefined):
        thingId_arg = parse_arg("thingId", thing_id)
        id_arg = parse_arg("id", id)

        async for data in self.client.subscribe(('subscription{notificationDeleted(%s%s)}' % (thingId_arg, id_arg)).replace('()', '')):
            yield data["notificationDeleted"]

    async def keep_online(self, thing_id):
        thingId_arg = parse_arg("thingId", thing_id)

        async for data in self.client.subscribe(('subscription{keepOnline(%s)}' % (thingId_arg)).replace('()', '')):
            yield data["keepOnline"]
