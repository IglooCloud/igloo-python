from igloo.models.user import User
from igloo.models.access_token import AccessToken
from igloo.models.pending_share import PendingShare
from igloo.models.environment import Environment
from igloo.models.thing import Thing
from igloo.models.float_variable import FloatVariable
from igloo.models.variable import Variable
from igloo.models.pending_transfer import PendingTransfer
from igloo.models.notification import Notification
from igloo.models.boolean_variable import BooleanVariable
from igloo.models.string_variable import StringVariable
from igloo.models.float_series_variable import FloatSeriesVariable
from igloo.models.category_series_variable import CategorySeriesVariable
from igloo.models.category_series_node import CategorySeriesNode
from igloo.models.file_variable import FileVariable
from igloo.models.float_series_node import FloatSeriesNode
from igloo.utils import undefined, parse_arg


class QueryRoot:
    def __init__(self, client):
        self.client = client

    @property
    def user(self, id=None, email=None):
        return User(self.client, id=id, email=email)

    def environment(self, id):
        return Environment(self.client, id)

    def thing(self, id):
        return Thing(self.client, id)

    def variable(self, id):
        return Variable(self.client, id)

    def float_variable(self, id):
        return FloatVariable(self.client, id)

    def string_variable(self, id):
        return StringVariable(self.client, id)

    def boolean_variable(self, id):
        return BooleanVariable(self.client, id)

    def file_variable(self, id):
        return FileVariable(self.client, id)

    def float_series_variable(self, id):
        return FloatSeriesVariable(self.client, id)

    def category_series_variable(self, id):
        return CategorySeriesVariable(self.client, id)

    def pending_share(self, id):
        return PendingShare(self.client, id)

    def pending_transfer(self, id):
        return PendingTransfer(self.client, id)

    def access_token(self, id):
        return AccessToken(self.client, id)

    def notification(self, id):
        return Notification(self.client, id)

    def float_series_node(self, id):
        return FloatSeriesNode(self.client, id)

    def category_series_node(self, id):
        return CategorySeriesNode(self.client, id)

    def get_new_totp_secret(self):
        return self.client.query("{getNewTotpSecret{secret,qrCode}}", keys=["getNewTotpSecret"])

    def verify_password(self, password, email=undefined):
        email_arg = parse_arg("email", email)
        return self.client.query('{verifyPassword(password:"%s" %s)}' % (password, email_arg), keys=["verifyPassword"])

    def verify_totp(self, code, email=undefined):
        email_arg = parse_arg("email", email)
        return self.client.query('{verifyTotp(code:"%s" %s)}' % (code, email_arg), keys=["verifyTotp"])

    def metadata(self):
        return self.client.query(
            """
            {
                metadata{
                    STANDARD_PLAN_MONTHLY_PRICE
                    STANDARD_PLAN_YEARLY_PRICE
                    EXTRA_STORAGE_MONTHLY_PRICE
                    EXTRA_THROUGHPUT_MONTHLY_PRICE
                    EXTRA_STORAGE_YEARLY_PRICE
                    EXTRA_THROUGHPUT_YEARLY_PRICE
                    CUSTOM_APPS_MONTHLY_PRICE
                    CUSTOM_APPS_YEARLY_PRICE
                }
            }
            """, keys=["metadata"])
