# programmatically generated file
from .models.user import User
from .models.permanent_token import PermanentToken
from .models.pending_environment_share import PendingEnvironmentShare
from .models.environment import Environment
from .models.device import Device
from .models.float_value import FloatValue
from .models.pending_owner_change import PendingOwnerChange
from .models.notification import Notification
from .models.boolean_value import BooleanValue
from .models.string_value import StringValue
from .models.float_series_value import FloatSeriesValue
from .models.category_series_value import CategorySeriesValue
from .models.category_series_node import CategorySeriesNode
from .models.file_value import FileValue
from .models.float_series_node import FloatSeriesNode
from .utils import parse_arg


class SubscriptionRoot:
    def __init__(self, client):
        self.client = client

    async def deviceCreated(self, environmentId=None):
        environmentId_arg = parse_arg("environmentId", environmentId)

        async for data in self.client.subscribe(('subscription{deviceCreated(%s){id}}' % (environmentId_arg)).replace('()', '')):
            yield Device(self.client, data["deviceCreated"]["id"])

    async def deviceClaimed(self, environmentId=None, id=None):
        environmentId_arg = parse_arg("environmentId", environmentId)
        id_arg = parse_arg("id", id)

        async for data in self.client.subscribe(('subscription{deviceClaimed(%s%s){id}}' % (environmentId_arg, id_arg)).replace('()', '')):
            yield Device(self.client, data["deviceClaimed"]["id"])

    async def environmentCreated(self, ):
        async for data in self.client.subscribe(('subscription{environmentCreated(){id}}' % ()).replace('()', '')):
            yield Environment(self.client, data["environmentCreated"]["id"])

    async def valueCreated(self, deviceId=None, hidden=None):
        deviceId_arg = parse_arg("deviceId", deviceId)
        hidden_arg = parse_arg("hidden", hidden)

        async for data in self.client.subscribe(('subscription{valueCreated(%s%s){id __typename}}' % (deviceId_arg, hidden_arg)).replace('()', '')):
            yield Value(self.client, data["valueCreated"]["id"])

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

    async def deviceMoved(self, environmentId=None, id=None):
        environmentId_arg = parse_arg("environmentId", environmentId)
        id_arg = parse_arg("id", id)

        async for data in self.client.subscribe(('subscription{deviceMoved(%s%s){id}}' % (environmentId_arg, id_arg)).replace('()', '')):
            yield Device(self.client, data["deviceMoved"]["id"])

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

    async def pendingOwnerChangeReceived(self, ):
        async for data in self.client.subscribe(('subscription{pendingOwnerChangeReceived(){id}}' % ()).replace('()', '')):
            yield PendingOwnerChange(self.client, data["pendingOwnerChangeReceived"]["id"])

    async def pendingOwnerChangeUpdated(self, ):
        async for data in self.client.subscribe(('subscription{pendingOwnerChangeUpdated(){id}}' % ()).replace('()', '')):
            yield PendingOwnerChange(self.client, data["pendingOwnerChangeUpdated"]["id"])

    async def pendingOwnerChangeAccepted(self, ):
        async for data in self.client.subscribe(('subscription{pendingOwnerChangeAccepted(){id sender receiver environment}}' % ()).replace('()', '')):
            yield data["pendingOwnerChangeAccepted"]

    async def pendingOwnerChangeDeclined(self, ):
        async for data in self.client.subscribe(('subscription{pendingOwnerChangeDeclined()}' % ()).replace('()', '')):
            yield data["pendingOwnerChangeDeclined"]

    async def pendingOwnerChangeRevoked(self, ):
        async for data in self.client.subscribe(('subscription{pendingOwnerChangeRevoked()}' % ()).replace('()', '')):
            yield data["pendingOwnerChangeRevoked"]

    async def environmentStoppedSharingWithYou(self, ):
        async for data in self.client.subscribe(('subscription{environmentStoppedSharingWithYou()}' % ()).replace('()', '')):
            yield data["environmentStoppedSharingWithYou"]

    async def userUpdated(self, id=None):
        id_arg = parse_arg("id", id)

        async for data in self.client.subscribe(('subscription{userUpdated(%s){id}}' % (id_arg)).replace('()', '')):
            yield User(self.client, data["userUpdated"]["id"])

    async def deviceUpdated(self, environmentId=None, id=None):
        environmentId_arg = parse_arg("environmentId", environmentId)
        id_arg = parse_arg("id", id)

        async for data in self.client.subscribe(('subscription{deviceUpdated(%s%s){id}}' % (environmentId_arg, id_arg)).replace('()', '')):
            yield Device(self.client, data["deviceUpdated"]["id"])

    async def environmentUpdated(self, id=None):
        id_arg = parse_arg("id", id)

        async for data in self.client.subscribe(('subscription{environmentUpdated(%s){id}}' % (id_arg)).replace('()', '')):
            yield Environment(self.client, data["environmentUpdated"]["id"])

    async def valueUpdated(self, deviceId=None, id=None, hidden=None):
        deviceId_arg = parse_arg("deviceId", deviceId)
        id_arg = parse_arg("id", id)
        hidden_arg = parse_arg("hidden", hidden)

        async for data in self.client.subscribe(('subscription{valueUpdated(%s%s%s){id __typename}}' % (deviceId_arg, id_arg, hidden_arg)).replace('()', '')):
            yield Value(self.client, data["valueUpdated"]["id"])

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

    async def notificationUpdated(self, deviceId=None, id=None)
    deviceId_arg = parse_arg("deviceId", deviceId)
    id_arg = parse_arg("id", id)

    async for data in self.client.subscribe(('subscription{notificationUpdated(%s%s){id}}' % (deviceId_arg, id_arg)).replace('()', '')):
            yield Notification(self.client, data["notificationUpdated"]["id"])

    async def valueDeleted(self, deviceId=None, id=None, hidden=None)
    deviceId_arg = parse_arg("deviceId", deviceId)
    id_arg = parse_arg("id", id)
    hidden_arg = parse_arg("hidden", hidden)

    async for data in self.client.subscribe(('subscription{valueDeleted(%s%s%s)}' % (deviceId_arg, id_arg, hidden_arg)).replace('()', '')):
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

    async def deviceDeleted(self, environmentId=None, id=None):
        environmentId_arg = parse_arg("environmentId", environmentId)
        id_arg = parse_arg("id", id)

        async for data in self.client.subscribe(('subscription{deviceDeleted(%s%s)}' % (environmentId_arg, id_arg)).replace('()', '')):
            yield data["deviceDeleted"]

    async def deviceUnclaimed(self, environmentId=None, id=None):
        environmentId_arg = parse_arg("environmentId", environmentId)
        id_arg = parse_arg("id", id)

        async for data in self.client.subscribe(('subscription{deviceUnclaimed(%s%s)}' % (environmentId_arg, id_arg)).replace('()', '')):
            yield data["deviceUnclaimed"]

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

    async def notificationDeleted(self, deviceId=None, id=None)
    deviceId_arg = parse_arg("deviceId", deviceId)
    id_arg = parse_arg("id", id)

    async for data in self.client.subscribe(('subscription{notificationDeleted(%s%s)}' % (deviceId_arg, id_arg)).replace('()', '')):
            yield data["notificationDeleted"]

    async def keepOnline(self, deviceId):
        deviceId_arg = parse_arg("deviceId", deviceId)

        async for data in self.client.subscribe(('subscription{keepOnline(%s)}' % (deviceId_arg)).replace('()', '')):
            yield data["keepOnline"]
