from igloo.models.user import User
from igloo.models.permanent_token import PermanentToken
from igloo.models.pending_environment_share import PendingEnvironmentShare
from igloo.models.environment import Environment
from igloo.models.device import Device
from igloo.models.float_value import FloatValue
from igloo.models.pending_owner_change import PendingOwnerChange
from igloo.models.notification import Notification
from igloo.models.boolean_value import BooleanValue
from igloo.models.string_value import StringValue
from igloo.models.float_series_value import FloatSeriesValue
from igloo.models.category_series_value import CategorySeriesValue
from igloo.models.category_series_node import CategorySeriesNode
from igloo.models.file_value import FileValue
from igloo.models.float_series_node import FloatSeriesNode


class QueryRoot:
    def __init__(self, client):
        self.client = client

    @property
    def user(self):
        return User(self.client)

    def environment(self, id):
        return Environment(self.client, id)

    def device(self, id):
        return Device(self.client, id)

    def floatValue(self, id):
        return FloatValue(self.client, id)

    def stringValue(self, id):
        return StringValue(self.client, id)

    def booleanValue(self, id):
        return BooleanValue(self.client, id)

    def fileValue(self, id):
        return FileValue(self.client, id)

    def floatSeriesValue(self, id):
        return FloatSeriesValue(self.client, id)

    def categorySeriesValue(self, id):
        return CategorySeriesValue(self.client, id)

    def pendingEnvironmentShare(self, id):
        return PendingEnvironmentShare(self.client, id)

    def pendingOwnerChange(self, id):
        return PendingOwnerChange(self.client, id)

    def permanentToken(self, id):
        return PermanentToken(self.client, id)

    def notification(self, id):
        return Notification(self.client, id)

    def floatSeriesNode(self, id):
        return FloatSeriesNode(self.client, id)

    def categorySeriesNode(self, id):
        return CategorySeriesNode(self.client, id)

    def getNewTotpSecret(self):
        return self.client.query("{getNewTotpSecret{secret,qrCode}}", keys=["getNewTotpSecret"])

    def getWebAuthnEnableChallenge(self):
        return self.client.query("{getWebAuthnEnableChallenge{publicKeyOptions,jwtChallenge}}", keys=["getWebAuthnEnableChallenge"])

    def getWebAuthnLogInChallenge(self, email):
        return self.client.query('{getWebAuthnLogInChallenge(email:"%s"){publicKeyOptions,jwtChallenge}}' % email, keys=["getWebAuthnLogInChallenge"])
