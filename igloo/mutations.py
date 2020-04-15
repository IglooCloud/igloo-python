from igloo.models.user import User
from igloo.models.permanent_token import PermanentToken
from igloo.models.pending_environment_share import PendingEnvironmentShare
from igloo.models.environment import Environment
from igloo.models.thing import Thing
from igloo.models.value import Value
from igloo.models.float_value import FloatVariable
from igloo.models.pending_owner_change import PendingOwnerChange
from igloo.models.notification import Notification
from igloo.models.boolean_value import BooleanVariable
from igloo.models.string_value import StringVariable
from igloo.models.float_series_value import FloatSeriesVariable
from igloo.models.category_series_value import CategorySeriesVariable
from igloo.models.category_series_node import CategorySeriesNode
from igloo.models.file_value import FileVariable
from igloo.models.float_series_node import FloatSeriesNode
from igloo.utils import parse_arg


async def _asyncWrapWith(res, wrapper_fn):
    result = await res
    return wrapper_fn(result["id"])


def wrapById(res, wrapper_fn):
    if isinstance(res, dict):
        return wrapper_fn(res["id"])
    else:
        return _asyncWrapWith(res, wrapper_fn)


def wrapWith(res, wrapper_fn):
    if isinstance(res, dict):
        return wrapper_fn(res)
    else:
        return _asyncWrapWith(res, wrapper_fn)


class MutationRoot:
    def __init__(self, client):
        self.client = client

    def sendConfirmationEmail(self, email, operation):
        email_arg = parse_arg("email", email)
        operation_arg = parse_arg("operation", operation, is_enum=True)

        return self.client.mutation('mutation{sendConfirmationEmail(%s%s)}' % (email_arg, operation_arg))["sendConfirmationEmail"]

    async def _wrapLogIn(self, res):
        resDict = await res
        resDict["user"] = User(self.client)
        return resDict

    def log_in(self, email, password, totp=None, private_cloud=None):
        email_arg = parse_arg("email", email)
        password_arg = parse_arg("password", password)
        totp_arg = parse_arg("totp", totp)
        privateCloud_arg = parse_arg("privateCloud", private_cloud)

        res = self.client.mutation('mutation{logIn(%s%s%s%s){user{id} token}}' % (email_arg,
                                                                                  password_arg,
                                                                                  totp_arg,
                                                                                  privateCloud_arg))["logIn"]

        if isinstance(res, dict):
            self.client.set_token(res["token"])
            res["user"] = User(self.client)
            return res
        else:
            return self._wrapLogIn(res)

    def create_access_token(self, name, password):
        name_arg = parse_arg("name", name)
        password_arg = parse_arg("password", password)
        return self.client.mutation('mutation{createAccessToken(%s%s)}' % (name_arg, password_arg))["createAccessToken"]

    def regenerate_access_token(self, id, password):
        id_arg = parse_arg("id", id)
        password_arg = parse_arg("password", password)

        return self.client.mutation('mutation{regenerateAccessToken(%s%s)}' % (id_arg, password_arg))["regenerateAccessToken"]

    def delete_access_token(self, id, password):
        id_arg = parse_arg("id", id)
        password_arg = parse_arg("password", password)

        return self.client.mutation('mutation{deleteAccessToken(%s%s)}' % (id_arg, password_arg))["deleteAccessToken"]

    async def _wrapSignUp(self, res):
        result = await res
        result["user"] = User(self.client)

        return result

    def sign_up(self, email, name, password, accept_privacy_policy_and_EULA, company_name=None, private_cloud=None):
        email_arg = parse_arg("email", email)
        name_arg = parse_arg("name", name)
        password_arg = parse_arg("password", password)
        companyName_arg = parse_arg("companyName", company_name)
        privateCloud_arg = parse_arg("privateCloud", private_cloud)
        acceptPrivacyPolicyAndEULA_arg = parse_arg(
            "acceptPrivacyPolicyAndEULA", accept_privacy_policy_and_EULA)

        res = self.client.mutation('mutation{signUp(%s%s%s%s%s%s){user{id} token}}' % (
            email_arg,
            name_arg,
            password_arg,
            companyName_arg,
            privateCloud_arg,
            acceptPrivacyPolicyAndEULA_arg))["signUp"]

        if isinstance(res, dict):
            res["user"] = User(self.client, res["user"]["id"])
            return res
        else:
            return self._wrapSignUp(res)

    def initiate_billing_setup(self):
        res = self.client.mutation("mutation{initiateBillingSetup }")[
            "initiateBillingSetup"]

        return res

    def update_billing_info(self, stripe_payment_method):
        stripePaymentMethod_arg = parse_arg(
            "stripePaymentMethod", stripe_payment_method)
        res = self.client.mutation("mutation{updateBillingInfo(%s) }" % stripePaymentMethod_arg)[
            "updateBillingInfo"]

        return res

    def confirm_payment_execution(self):
        res = self.client.mutation("mutation{confirmPaymentExecution }")[
            "confirmPaymentExecution"]

        return res

    def retry_payment(self):
        res = self.client.mutation("mutation{retryPayment }")[
            "retryPayment"]

        return res

    def change_billing_plan(self, billing_plan, billing_cycle, extra_storage, extra_throughput, custom_apps):
        billingPlan_arg = parse_arg("billingPlan", billing_plan, is_enum=True)
        billingCycle_arg = parse_arg(
            "billingCycle", billing_cycle, is_enum=True)
        extraStorage_arg = parse_arg("extraStorage", extra_storage)
        extraThroughput_arg = parse_arg("extraThroughput", extra_throughput)
        customApps_arg = parse_arg("customApps", custom_apps)

        res = self.client.mutation("mutation{changeBillingPlan(%s%s%s%s%s) }" % (
            billingPlan_arg,
            billingCycle_arg,
            extraStorage_arg,
            extraThroughput_arg,
            customApps_arg
        ))[
            "changeBillingPlan"]

        return res

    def change_password(self, new_password, old_password):
        new_password_arg = parse_arg("newPassword", new_password)
        old_password_arg = parse_arg("oldPassword", old_password)

        res = self.client.mutation(
            'mutation{changePassword(%s%s)}' % (new_password_arg, old_password_arg))["changePassword"]

        return res

    def set_totp(self, code, secret, password):
        code_arg = parse_arg("code", code)
        secret_arg = parse_arg("secret", secret)
        password_arg = parse_arg("password", password)
        return self.client.mutation('mutation{setTotp(%s%s%s)}' % (code_arg, secret_arg, password_arg))["setTotp"]

    def disable_totp(self, password):
        password_arg = parse_arg("password", password)
        return self.client.mutation('mutation{disableTotp(%s%s%s)}' % password_arg)["disableTotp"]

    def send_disable_totp_email(self, email, redirect_to):
        email_arg = parse_arg("email", email)
        redirect_to_arg = parse_arg("redirectTo", redirect_to, is_enum=True)
        return self.client.mutation('mutation{sendDisableTotpEmail(%s%s)}' % (email_arg, redirect_to_arg))["sendDisableTotpEmail"]

    def send_verification_email(self, redirect_to):
        redirect_to_arg = parse_arg("redirectTo", redirect_to, is_enum=True)

        return self.client.mutation('mutation{sendVerificationEmail(%s)}' % (redirect_to_arg))["sendVerificationEmail"]

    def send_password_recovery_email(self, email, redirect_to):
        email_arg = parse_arg("email", email)
        redirect_to_arg = parse_arg("redirectTo", redirect_to, is_enum=True)
        return self.client.mutation('mutation{sendPasswordRecoveryEmail(%s%s)}' % (email_arg, redirect_to_arg))["sendPasswordRecoveryEmail"]

    def reset_password(self, recovery_token, new_password):
        recovery_token_arg = parse_arg("recoveryToken", recovery_token)
        new_password_arg = parse_arg("newPassword", new_password)
        return self.client.mutation('mutation{resetPassword(%s%s)}' % (recovery_token_arg, new_password_arg))["resetPassword"]

    def share_environment(self, environment_id, role, email=None, user_id=None):
        environmentId_arg = parse_arg("environmentId", environment_id)
        role_arg = parse_arg("role", role, is_enum=True)
        email_arg = parse_arg("email", email)
        userId_arg = parse_arg("userId", user_id)
        res = self.client.mutation('mutation{shareEnvironment(%s%s%s%s){id}}' % (
            environmentId_arg, email_arg, userId_arg, role_arg))["shareEnvironment"]

        def wrapper(id):
            return PendingEnvironmentShare(self.client, id)

        return wrapById(res, wrapper)

    def pending_share(self, id, role):
        id_arg = parse_arg("id", id)
        role_arg = parse_arg("role", role, is_enum=True)

        res = self.client.mutation('mutation{pendingShare(%s%s){id}}' % (
            id_arg, role_arg))["pendingShare"]

        def wrapper(id):
            return PendingEnvironmentShare(self.client, id)

        return wrapById(res, wrapper)

    def revoke_pending_share(self, pending_share_id):
        pendingEnvironmentShareId_arg = parse_arg(
            "pendingShareId", pending_share_id)

        return self.client.mutation('mutation{revokePendingShare(%s)}' % (pendingEnvironmentShareId_arg))["revokePendingShare"]

    def accept_pending_share(self, pending_share_id):
        pendingEnvironmentShareId_arg = parse_arg(
            "pendingShareId", pending_share_id)

        res = self.client.mutation('mutation{acceptPendingShare(%s){sender{id} receiver{id} role environment{id}}}' % (
            pendingEnvironmentShareId_arg))["acceptPendingShare"]

        def wrapper(res):
            res["sender"] = User(self.client, res["sender"]["id"])
            res["receiver"] = User(self.client, res["receiver"]["id"])
            res["environment"] = Environment(
                self.client, res["environment"]["id"])

            return res

        return wrapWith(res, wrapper)

    def decline_pending_share(self, pending_share_id):
        pendingEnvironmentShareId_arg = parse_arg(
            "pendingShareId", pending_share_id)

        return self.client.mutation('mutation{declinePendingShare(%s)}' % (pendingEnvironmentShareId_arg))["declinePendingShare"]

    def stop_sharing_environment(self, environment_id, email=None, user_id=None):
        environmentId_arg = parse_arg("environmentId", environment_id)
        email_arg = parse_arg("email", email)
        userId_arg = parse_arg("userId", user_id)
        res = self.client.mutation('mutation{stopSharingEnvironment(%s%s%s){id}}' % (
            environmentId_arg, email_arg, userId_arg))["stopSharingEnvironment"]

        def wrapper(id):
            return Environment(self.client, id)

        return wrapById(res, wrapper)

    def leave_environment(self, environment_id):
        environmentId_arg = parse_arg("environmentId", environment_id)

        return self.client.mutation('mutation{leaveEnvironment(%s)}' % (environmentId_arg))["leaveEnvironment"]

    def changeOwner(self, environmentId, email=None, userId=None):
        environmentId_arg = parse_arg("environmentId", environmentId)
        email_arg = parse_arg("email", email)
        userId_arg = parse_arg("userId", userId)
        res = self.client.mutation('mutation{changeOwner(%s%s%s){id}}' % (
            environmentId_arg, email_arg, userId_arg))["changeOwner"]

        def wrapper(id):
            return PendingOwnerChange(self.client, id)

        return wrapById(res, wrapper)

    def revokePendingOwnerChange(self, pendingOwnerChangeId):
        pendingOwnerChangeId_arg = parse_arg(
            "pendingOwnerChangeId", pendingOwnerChangeId)

        return self.client.mutation('mutation{revokePendingOwnerChange(%s)}' % (pendingOwnerChangeId_arg))["revokePendingOwnerChange"]

    def acceptPendingOwnerChange(self, pendingOwnerChangeId):
        pendingOwnerChangeId_arg = parse_arg(
            "pendingOwnerChangeId", pendingOwnerChangeId)

        res = self.client.mutation('mutation{acceptPendingOwnerChange(%s){sender{id} receiver{id} environment{id}}}' % (
            pendingOwnerChangeId_arg))["acceptPendingOwnerChange"]

        def wrapper(res):
            res["sender"] = User(self.client, res["sender"]["id"])
            res["receiver"] = User(self.client, res["receiver"]["id"])
            res["environment"] = Environment(
                self.client, res["environment"]["id"])

            return res

        return wrapWith(res, wrapper)

    def declinePendingOwnerChange(self, pendingOwnerChangeId):
        pendingOwnerChangeId_arg = parse_arg(
            "pendingOwnerChangeId", pendingOwnerChangeId)

        return self.client.mutation('mutation{declinePendingOwnerChange(%s)}' % (pendingOwnerChangeId_arg))["declinePendingOwnerChange"]

    def changeRole(self, environmentId, email, newRole):
        environmentId_arg = parse_arg("environmentId", environmentId)
        email_arg = parse_arg("email", email)
        newRole_arg = parse_arg("newRole", newRole)

        res = self.client.mutation('mutation{changeRole(%s%s%s){id}}' % (
            environmentId_arg, email_arg, newRole_arg))["changeRole"]

        def wrapper(id):
            return Environment(self.client, id)

        return wrapById(res, wrapper)

    def createEnvironment(self, name, picture=None, index=None, muted=None):
        name_arg = parse_arg("name", name)
        picture_arg = parse_arg("picture", picture, is_enum=True)
        index_arg = parse_arg("index", index)
        muted_arg = parse_arg("muted", muted)
        res = self.client.mutation('mutation{createEnvironment(%s%s%s%s){id}}' % (
            name_arg, picture_arg, index_arg, muted_arg))["createEnvironment"]

        def wrapper(id):
            return Environment(self.client, id)

        return wrapById(res, wrapper)

    def createThing(self, thingType=None, firmware=None):
        thingType_arg = parse_arg("thingType", thingType)
        firmware_arg = parse_arg("firmware", firmware)
        res = self.client.mutation('mutation{createThing(%s%s){id}}' % (
            thingType_arg, firmware_arg))["createThing"]

        def wrapper(id):
            return Thing(self.client, id)

        return wrapById(res, wrapper)

    def claimThing(self, claimCode, name, environmentId, index=None, muted=None):
        claimCode_arg = parse_arg("claimCode", claimCode)
        name_arg = parse_arg("name", name)
        environmentId_arg = parse_arg("environmentId", environmentId)
        index_arg = parse_arg("index", index)
        muted_arg = parse_arg("muted", muted)
        res = self.client.mutation('mutation{claimThing(%s%s%s%s%s){id}}' % (
            claimCode_arg, name_arg, index_arg, environmentId_arg, muted_arg))["claimThing"]

        def wrapper(id):
            return Thing(self.client, id)

        return wrapById(res, wrapper)

    def createNotification(self, thingId, content, date=None):
        thingId_arg = parse_arg("thingId", thingId)
        content_arg = parse_arg("content", content)
        date_arg = parse_arg("date", date)
        res = self.client.mutation('mutation{createNotification(%s%s%s){id}}' % (
            thingId_arg, content_arg, date_arg))["createNotification"]

        def wrapper(id):
            return Notification(self.client, id)

        return wrapById(res, wrapper)

    def createFloatVariable(self, thingId, permission, name, private=None, hidden=None, unitOfMeasurement=None, value=None, precision=None, min=None, max=None, index=None):
        thingId_arg = parse_arg("thingId", thingId)
        permission_arg = parse_arg("permission", permission, is_enum=True)
        name_arg = parse_arg("name", name)
        private_arg = parse_arg("private", private)
        hidden_arg = parse_arg("hidden", hidden)
        unitOfMeasurement_arg = parse_arg(
            "unitOfMeasurement", unitOfMeasurement)
        value_arg = parse_arg("value", value)
        precision_arg = parse_arg("precision", precision)
        min_arg = parse_arg("min", min)
        max_arg = parse_arg("max", max)

        index_arg = parse_arg("index", index)
        res = self.client.mutation('mutation{createFloatVariable(%s%s%s%s%s%s%s%s%s%s%s){id}}' % (thingId_arg, permission_arg, private_arg, hidden_arg,
                                                                                                  unitOfMeasurement_arg, value_arg, precision_arg, min_arg, max_arg, name_arg, index_arg))["createFloatVariable"]

        def wrapper(id):
            return FloatVariable(self.client, id)

        return wrapById(res, wrapper)

    def createStringVariable(self, thingId, permission, name, private=None, hidden=None, value=None, maxChars=None, allowedValues=None, index=None):
        thingId_arg = parse_arg("thingId", thingId)
        permission_arg = parse_arg("permission", permission, is_enum=True)
        name_arg = parse_arg("name", name)
        private_arg = parse_arg("private", private)
        hidden_arg = parse_arg("hidden", hidden)
        value_arg = parse_arg("value", value)
        maxChars_arg = parse_arg("maxChars", maxChars)

        allowedValues_arg = parse_arg("allowedValues", allowedValues)
        index_arg = parse_arg("index", index)
        res = self.client.mutation('mutation{createStringVariable(%s%s%s%s%s%s%s%s%s){id}}' % (
            thingId_arg, permission_arg, private_arg, hidden_arg, value_arg, maxChars_arg, name_arg, allowedValues_arg, index_arg))["createStringVariable"]

        def wrapper(id):
            return StringVariable(self.client, id)

        return wrapById(res, wrapper)

    def createBooleanVariable(self, thingId, permission, name, private=None, hidden=None, value=None, index=None):
        thingId_arg = parse_arg("thingId", thingId)
        permission_arg = parse_arg("permission", permission, is_enum=True)
        name_arg = parse_arg("name", name)
        private_arg = parse_arg("private", private)
        hidden_arg = parse_arg("hidden", hidden)
        value_arg = parse_arg("value", value)

        index_arg = parse_arg("index", index)
        res = self.client.mutation('mutation{createBooleanVariable(%s%s%s%s%s%s%s){id}}' % (
            thingId_arg, permission_arg, private_arg, hidden_arg, value_arg, name_arg, index_arg))["createBooleanVariable"]

        def wrapper(id):
            return BooleanVariable(self.client, id)

        return wrapById(res, wrapper)

    def createFloatSeriesVariable(self, thingId, name, private=None, hidden=None, unitOfMeasurement=None, precision=None, min=None, max=None, index=None):
        thingId_arg = parse_arg("thingId", thingId)
        name_arg = parse_arg("name", name)
        private_arg = parse_arg("private", private)
        hidden_arg = parse_arg("hidden", hidden)
        unitOfMeasurement_arg = parse_arg(
            "unitOfMeasurement", unitOfMeasurement)
        precision_arg = parse_arg("precision", precision)
        min_arg = parse_arg("min", min)
        max_arg = parse_arg("max", max)

        index_arg = parse_arg("index", index)
        res = self.client.mutation('mutation{createFloatSeriesVariable(%s%s%s%s%s%s%s%s%s){id}}' % (
            thingId_arg, private_arg, hidden_arg, unitOfMeasurement_arg, precision_arg, min_arg, max_arg, name_arg, index_arg))["createFloatSeriesVariable"]

        def wrapper(id):
            return FloatSeriesVariable(self.client, id)

        return wrapById(res, wrapper)

    def createFloatSeriesNode(self, seriesId, value, timestamp=None):
        seriesId_arg = parse_arg("seriesId", seriesId)
        value_arg = parse_arg("value", value)
        timestamp_arg = parse_arg("timestamp", timestamp)
        res = self.client.mutation('mutation{createFloatSeriesNode(%s%s%s){id}}' % (
            seriesId_arg, timestamp_arg, value_arg))["createFloatSeriesNode"]

        def wrapper(id):
            return FloatSeriesNode(self.client, id)

        return wrapById(res, wrapper)

    def createCategorySeriesVariable(self, thingId, name, private=None, hidden=None, allowedValues=None, index=None):
        thingId_arg = parse_arg("thingId", thingId)
        name_arg = parse_arg("name", name)
        private_arg = parse_arg("private", private)
        hidden_arg = parse_arg("hidden", hidden)

        allowedValues_arg = parse_arg("allowedValues", allowedValues)
        index_arg = parse_arg("index", index)
        res = self.client.mutation('mutation{createCategorySeriesVariable(%s%s%s%s%s%s){id}}' % (
            thingId_arg, private_arg, hidden_arg, name_arg, allowedValues_arg, index_arg))["createCategorySeriesVariable"]

        def wrapper(id):
            return CategorySeriesVariable(self.client, id)

        return wrapById(res, wrapper)

    def createCategorySeriesNode(self, seriesId, value, timestamp=None):
        seriesId_arg = parse_arg("seriesId", seriesId)
        value_arg = parse_arg("value", value)
        timestamp_arg = parse_arg("timestamp", timestamp)
        res = self.client.mutation('mutation{createCategorySeriesNode(%s%s%s){id}}' % (
            seriesId_arg, timestamp_arg, value_arg))["createCategorySeriesNode"]

        def wrapper(id):
            return CategorySeriesNode(self.client, id)

        return wrapById(res, wrapper)

    def user(self, quietMode=None, paymentPlan=None, name=None, profileIcon=None):

        quietMode_arg = parse_arg("quietMode", quietMode)
        paymentPlan_arg = parse_arg("paymentPlan", paymentPlan)
        name_arg = parse_arg("name", name)
        profileIcon_arg = parse_arg("profileIcon", profileIcon)
        res = self.client.mutation('mutation{user(%s%s%s%s){id}}' % (
            quietMode_arg, paymentPlan_arg, name_arg, profileIcon_arg))["user"]

        def wrapper(id):
            return User(self.client)

        return wrapById(res, wrapper)

    def changeEmail(self, newEmail):
        newEmail_arg = parse_arg("newEmail", newEmail)

        return self.client.mutation('mutation{changeEmail(%s)}' % (newEmail_arg))["changeEmail"]

    def settings(self, language=None, lengthAndMass=None, temperature=None, dateFormat=None, timeFormat=None, passwordChangeEmail=None, environmentSharesEmail=None, permanentTokenCreatedEmail=None):

        language_arg = parse_arg("language", language)
        lengthAndMass_arg = parse_arg(
            "lengthAndMass", lengthAndMass, is_enum=True)
        temperature_arg = parse_arg("temperature", temperature, is_enum=True)
        dateFormat_arg = parse_arg("dateFormat", dateFormat, is_enum=True)
        timeFormat_arg = parse_arg("timeFormat", timeFormat, is_enum=True)
        passwordChangeEmail_arg = parse_arg(
            "passwordChangeEmail", passwordChangeEmail)
        environmentSharesEmail_arg = parse_arg(
            "environmentSharesEmail", environmentSharesEmail)
        permanentTokenCreatedEmail_arg = parse_arg(
            "permanentTokenCreatedEmail", permanentTokenCreatedEmail)

        return self.client.mutation('mutation{settings(%s%s%s%s%s%s%s%s){id lengthAndMass temperature timeFormat dateFormat language passwordChangeEmail environmentSharesEmail permanentTokenCreatedEmail}}' % (language_arg, lengthAndMass_arg, temperature_arg, dateFormat_arg, timeFormat_arg, passwordChangeEmail_arg, environmentSharesEmail_arg, permanentTokenCreatedEmail_arg))["settings"]

    def updatePaymentInfo(self, stripeToken):
        stripeToken_arg = parse_arg("stripeToken", stripeToken)

        return self.client.mutation('mutation{updatePaymentInfo(%s)}' % (stripeToken_arg))["updatePaymentInfo"]

    def environment(self, id, name=None, picture=None, index=None, muted=None):
        id_arg = parse_arg("id", id)
        name_arg = parse_arg("name", name)
        picture_arg = parse_arg("picture", picture, is_enum=True)
        index_arg = parse_arg("index", index)
        muted_arg = parse_arg("muted", muted)
        res = self.client.mutation('mutation{environment(%s%s%s%s%s){id}}' % (
            id_arg, name_arg, picture_arg, index_arg, muted_arg))["environment"]

        def wrapper(id):
            return Environment(self.client, id)

        return wrapById(res, wrapper)

    def thing(self, id, thingType=None, name=None, index=None, signalStatus=None, batteryStatus=None, batteryCharging=None, firmware=None, muted=None, starred=None):
        id_arg = parse_arg("id", id)
        thingType_arg = parse_arg("thingType", thingType)
        name_arg = parse_arg("name", name)
        index_arg = parse_arg("index", index)
        signalStatus_arg = parse_arg("signalStatus", signalStatus)
        batteryStatus_arg = parse_arg("batteryStatus", batteryStatus)
        batteryCharging_arg = parse_arg("batteryCharging", batteryCharging)
        firmware_arg = parse_arg("firmware", firmware)
        muted_arg = parse_arg("muted", muted)
        starred_arg = parse_arg("starred", starred)
        res = self.client.mutation('mutation{thing(%s%s%s%s%s%s%s%s%s%s){id}}' % (
            id_arg, thingType_arg, name_arg, index_arg, signalStatus_arg, batteryStatus_arg, batteryCharging_arg, firmware_arg, muted_arg, starred_arg))["thing"]

        def wrapper(id):
            return Thing(self.client, id)

        return wrapById(res, wrapper)

    def value(self, id, private=None, hidden=None, name=None, index=None):
        id_arg = parse_arg("id", id)
        private_arg = parse_arg("private", private)
        hidden_arg = parse_arg("hidden", hidden)

        name_arg = parse_arg("name", name)
        index_arg = parse_arg("index", index)
        res = self.client.mutation('mutation{value(%s%s%s%s%s){id __typename}}' % (
            id_arg, private_arg, hidden_arg, name_arg, index_arg))["value"]

        def wrapper(res):
            return Value(self.client, res["id"], res["__typename"])

        return wrapWith(res, wrapper)

    def moveThing(self, thingId, newEnvironmentId):
        thingId_arg = parse_arg("thingId", thingId)
        newEnvironmentId_arg = parse_arg("newEnvironmentId", newEnvironmentId)

        res = self.client.mutation('mutation{moveThing(%s%s){id}}' % (
            thingId_arg, newEnvironmentId_arg))["moveThing"]

        def wrapper(id):
            return Thing(self.client, id)

        return wrapById(res, wrapper)

    def resetOnlineState(self, thingId):
        thingId_arg = parse_arg("thingId", thingId)

        res = self.client.mutation('mutation{resetOnlineState(%s){id}}' % (thingId_arg))[
            "resetOnlineState"]

        def wrapper(id):
            return Thing(self.client, id)

        return wrapById(res, wrapper)

    def floatVariable(self, id, permission=None, private=None, hidden=None, unitOfMeasurement=None, value=None, precision=None, min=None, max=None, name=None, index=None):
        id_arg = parse_arg("id", id)
        permission_arg = parse_arg("permission", permission, is_enum=True)
        private_arg = parse_arg("private", private)
        hidden_arg = parse_arg("hidden", hidden)
        unitOfMeasurement_arg = parse_arg(
            "unitOfMeasurement", unitOfMeasurement)
        value_arg = parse_arg("value", value)
        precision_arg = parse_arg("precision", precision)
        min_arg = parse_arg("min", min)
        max_arg = parse_arg("max", max)
        name_arg = parse_arg("name", name)

        index_arg = parse_arg("index", index)
        res = self.client.mutation('mutation{floatVariable(%s%s%s%s%s%s%s%s%s%s%s){id}}' % (
            id_arg, permission_arg, private_arg, hidden_arg, unitOfMeasurement_arg, value_arg, precision_arg, min_arg, max_arg, name_arg, index_arg))["floatVariable"]

        def wrapper(id):
            return FloatVariable(self.client, id)

        return wrapById(res, wrapper)

    def atomicUpdateFloat(self, id, incrementBy):
        id_arg = parse_arg("id", id)
        incrementBy_arg = parse_arg("incrementBy", incrementBy)

        res = self.client.mutation('mutation{atomicUpdateFloat(%s%s){id}}' % (
            id_arg, incrementBy_arg))["atomicUpdateFloat"]

        def wrapper(id):
            return FloatVariable(self.client, id)

        return wrapById(res, wrapper)

    def stringVariable(self, id, permission=None, private=None, hidden=None, value=None, maxChars=None, name=None, allowedValues=None, index=None):
        id_arg = parse_arg("id", id)
        permission_arg = parse_arg("permission", permission, is_enum=True)
        private_arg = parse_arg("private", private)
        hidden_arg = parse_arg("hidden", hidden)
        value_arg = parse_arg("value", value)
        maxChars_arg = parse_arg("maxChars", maxChars)
        name_arg = parse_arg("name", name)

        allowedValues_arg = parse_arg("allowedValues", allowedValues)
        index_arg = parse_arg("index", index)
        res = self.client.mutation('mutation{stringVariable(%s%s%s%s%s%s%s%s%s){id}}' % (
            id_arg, permission_arg, private_arg, hidden_arg, value_arg, maxChars_arg, name_arg, allowedValues_arg, index_arg))["stringVariable"]

        def wrapper(id):
            return StringVariable(self.client, id)

        return wrapById(res, wrapper)

    def booleanVariable(self, id, permission=None, private=None, hidden=None, value=None, name=None, index=None):
        id_arg = parse_arg("id", id)
        permission_arg = parse_arg("permission", permission, is_enum=True)
        private_arg = parse_arg("private", private)
        hidden_arg = parse_arg("hidden", hidden)
        value_arg = parse_arg("value", value)
        name_arg = parse_arg("name", name)

        index_arg = parse_arg("index", index)
        res = self.client.mutation('mutation{booleanVariable(%s%s%s%s%s%s%s){id}}' % (
            id_arg, permission_arg, private_arg, hidden_arg, value_arg, name_arg, index_arg))["booleanVariable"]

        def wrapper(id):
            return BooleanVariable(self.client, id)

        return wrapById(res, wrapper)

    def floatSeriesVariable(self, id, private=None, hidden=None, unitOfMeasurement=None, precision=None, min=None, max=None, name=None, index=None):
        id_arg = parse_arg("id", id)
        private_arg = parse_arg("private", private)
        hidden_arg = parse_arg("hidden", hidden)
        unitOfMeasurement_arg = parse_arg(
            "unitOfMeasurement", unitOfMeasurement)
        precision_arg = parse_arg("precision", precision)
        min_arg = parse_arg("min", min)
        max_arg = parse_arg("max", max)
        name_arg = parse_arg("name", name)

        index_arg = parse_arg("index", index)
        res = self.client.mutation('mutation{floatSeriesVariable(%s%s%s%s%s%s%s%s%s){id}}' % (
            id_arg, private_arg, hidden_arg, unitOfMeasurement_arg, precision_arg, min_arg, max_arg, name_arg, index_arg))["floatSeriesVariable"]

        def wrapper(id):
            return FloatSeriesVariable(self.client, id)

        return wrapById(res, wrapper)

    def floatSeriesNode(self, id, value=None, timestamp=None):
        id_arg = parse_arg("id", id)
        value_arg = parse_arg("value", value)
        timestamp_arg = parse_arg("timestamp", timestamp)
        res = self.client.mutation('mutation{floatSeriesNode(%s%s%s){id}}' % (
            id_arg, value_arg, timestamp_arg))["floatSeriesNode"]

        def wrapper(id):
            return FloatSeriesNode(self.client, id)

        return wrapById(res, wrapper)

    def categorySeriesVariable(self, id, private=None, hidden=None, name=None, allowedValues=None, index=None):
        id_arg = parse_arg("id", id)
        private_arg = parse_arg("private", private)
        hidden_arg = parse_arg("hidden", hidden)
        name_arg = parse_arg("name", name)

        allowedValues_arg = parse_arg("allowedValues", allowedValues)
        index_arg = parse_arg("index", index)
        res = self.client.mutation('mutation{categorySeriesVariable(%s%s%s%s%s%s){id}}' % (
            id_arg, private_arg, hidden_arg, name_arg, allowedValues_arg, index_arg))["categorySeriesVariable"]

        def wrapper(id):
            return CategorySeriesVariable(self.client, id)

        return wrapById(res, wrapper)

    def categorySeriesNode(self, id, value=None, timestamp=None):
        id_arg = parse_arg("id", id)
        value_arg = parse_arg("value", value)
        timestamp_arg = parse_arg("timestamp", timestamp)
        res = self.client.mutation('mutation{categorySeriesNode(%s%s%s){id}}' % (
            id_arg, value_arg, timestamp_arg))["categorySeriesNode"]

        def wrapper(id):
            return CategorySeriesNode(self.client, id)

        return wrapById(res, wrapper)

    def notification(self, id, content=None, read=None):
        id_arg = parse_arg("id", id)
        content_arg = parse_arg("content", content)
        read_arg = parse_arg("read", read)
        res = self.client.mutation('mutation{notification(%s%s%s){id}}' % (
            id_arg, content_arg, read_arg))["notification"]

        def wrapper(id):
            return Notification(self.client, id)

        return wrapById(res, wrapper)

    def deleteNotification(self, id):
        id_arg = parse_arg("id", id)

        return self.client.mutation('mutation{deleteNotification(%s)}' % (id_arg))["deleteNotification"]

    def deleteValue(self, id):
        id_arg = parse_arg("id", id)

        return self.client.mutation('mutation{deleteValue(%s)}' % (id_arg))["deleteValue"]

    def deleteThing(self, id):
        id_arg = parse_arg("id", id)

        return self.client.mutation('mutation{deleteThing(%s)}' % (id_arg))["deleteThing"]

    def unclaimThing(self, id):
        id_arg = parse_arg("id", id)

        return self.client.mutation('mutation{unclaimThing(%s){id}}' % (id_arg))["unclaimThing"]

    def deleteEnvironment(self, id):
        id_arg = parse_arg("id", id)

        return self.client.mutation('mutation{deleteEnvironment(%s)}' % (id_arg))["deleteEnvironment"]

    def deleteUser(self, ):

        return self.client.mutation('mutation{deleteUser()}' % ())["deleteUser"]

    def deleteFloatSeriesNode(self, id):
        id_arg = parse_arg("id", id)

        return self.client.mutation('mutation{deleteFloatSeriesNode(%s)}' % (id_arg))["deleteFloatSeriesNode"]

    def deleteCategorySeriesNode(self, id):
        id_arg = parse_arg("id", id)

        return self.client.mutation('mutation{deleteCategorySeriesNode(%s)}' % (id_arg))["deleteCategorySeriesNode"]
