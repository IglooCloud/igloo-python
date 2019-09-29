from igloo.models.user import User
from igloo.models.permanent_token import PermanentToken
from igloo.models.pending_environment_share import PendingEnvironmentShare
from igloo.models.environment import Environment
from igloo.models.thing import Thing
from igloo.models.float_value import FloatVariable
from igloo.models.value import Value
from igloo.models.pending_owner_change import PendingOwnerChange
from igloo.models.notification import Notification
from igloo.models.boolean_value import BooleanVariable
from igloo.models.string_value import StringVariable
from igloo.models.float_series_value import FloatSeriesVariable
from igloo.models.category_series_value import CategorySeriesVariable
from igloo.models.category_series_node import CategorySeriesNode
from igloo.models.file_value import FileVariable
from igloo.models.float_series_node import FloatSeriesNode


class QueryRoot:
    def __init__(self, client):
        self.client = client

    @property
    def user(self):
        return User(self.client)

    def environment(self, id):
        return Environment(self.client, id)

    def thing(self, id):
        return Thing(self.client, id)

    def value(self, id):
        return Value(self.client, id)

    def floatVariable(self, id):
        return FloatVariable(self.client, id)

    def stringVariable(self, id):
        return StringVariable(self.client, id)

    def booleanVariable(self, id):
        return BooleanVariable(self.client, id)

    def fileVariable(self, id):
        return FileVariable(self.client, id)

    def floatSeriesVariable(self, id):
        return FloatSeriesVariable(self.client, id)

    def categorySeriesVariable(self, id):
        return CategorySeriesVariable(self.client, id)

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
