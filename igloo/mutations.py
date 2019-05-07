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

    def verifyPassword(self, email, password):
        email_arg = parse_arg("email", email)
        password_arg = parse_arg("password", password)

        return self.client.mutation('mutation{verifyPassword(%s%s)}' % (email_arg, password_arg))["verifyPassword"]

    def verifyWebAuthn(self, challengeResponse, jwtChallenge):
        challengeResponse_arg = parse_arg(
            "challengeResponse", challengeResponse)
        jwtChallenge_arg = parse_arg("jwtChallenge", jwtChallenge)

        return self.client.mutation('mutation{verifyWebAuthn(%s%s)}' % (challengeResponse_arg, jwtChallenge_arg))["verifyWebAuthn"]

    def verifyTotp(self, email, code):
        email_arg = parse_arg("email", email)
        code_arg = parse_arg("code", code)

        return self.client.mutation('mutation{verifyTotp(%s%s)}' % (email_arg, code_arg))["verifyTotp"]

    def verifyEmailToken(self, token):
        token_arg = parse_arg("token", token)

        return self.client.mutation('mutation{verifyEmailToken(%s)}' % (token_arg))["verifyEmailToken"]

    def sendConfirmationEmail(self, email, operation):
        email_arg = parse_arg("email", email)
        operation_arg = parse_arg("operation", operation, is_enum=True)

        return self.client.mutation('mutation{sendConfirmationEmail(%s%s)}' % (email_arg, operation_arg))["sendConfirmationEmail"]

    async def _wrapLogIn(self, res):
        resDict = await res
        self.client.set_token(resDict["token"])
        resDict["user"] = User(self.client)
        return resDict

    def logIn(self, passwordCertificate=None, webAuthnCertificate=None, totpCertificate=None, emailCertificate=None):
        passwordCertificate_arg = parse_arg(
            "passwordCertificate", passwordCertificate)
        webAuthnCertificate_arg = parse_arg(
            "webAuthnCertificate", webAuthnCertificate)
        totpCertificate_arg = parse_arg("totpCertificate", totpCertificate)
        emailCertificate_arg = parse_arg("emailCertificate", emailCertificate)

        res = self.client.mutation('mutation{logIn(%s%s%s%s){user{id} token}}' % (
            passwordCertificate_arg, webAuthnCertificate_arg, totpCertificate_arg, emailCertificate_arg))["logIn"]

        if isinstance(res, dict):
            self.client.set_token(res["token"])
            res["user"] = User(self.client)
            return res
        else:
            return self._wrapLogIn(res)

    def createToken(self, tokenType, passwordCertificate=None, webAuthnCertificate=None, totpCertificate=None, emailCertificate=None):
        tokenType_arg = parse_arg("tokenType", tokenType, is_enum=True)
        passwordCertificate_arg = parse_arg(
            "passwordCertificate", passwordCertificate)
        webAuthnCertificate_arg = parse_arg(
            "webAuthnCertificate", webAuthnCertificate)
        totpCertificate_arg = parse_arg("totpCertificate", totpCertificate)
        emailCertificate_arg = parse_arg("emailCertificate", emailCertificate)
        return self.client.mutation('mutation{createToken(%s%s%s%s%s)}' % (passwordCertificate_arg, webAuthnCertificate_arg, totpCertificate_arg, emailCertificate_arg, tokenType_arg))["createToken"]

    def createPermanentToken(self, name):
        name_arg = parse_arg("name", name)

        res = self.client.mutation('mutation{createPermanentToken(%s){id}}' % (name_arg))[
            "createPermanentToken"]

        def wrapper(id):
            return PermanentToken(self.client, id)

        return wrapById(res, wrapper)

    def regeneratePermanentToken(self, id):
        id_arg = parse_arg("id", id)

        return self.client.mutation('mutation{regeneratePermanentToken(%s)}' % (id_arg))["regeneratePermanentToken"]

    def deletePermanentToken(self, id):
        id_arg = parse_arg("id", id)

        return self.client.mutation('mutation{deletePermanentToken(%s)}' % (id_arg))["deletePermanentToken"]

    async def _wrapSignUp(self, res):
        result = await res
        result["user"] = User(self.client)

        return result

    def signUp(self, email, name):
        email_arg = parse_arg("email", email)
        name_arg = parse_arg("name", name)

        res = self.client.mutation('mutation{signUp(%s%s){user{id} changeAuthenticationToken}}' % (
            email_arg, name_arg))["signUp"]

        if isinstance(res, dict):
            res["user"] = User(self.client, res["user"]["id"])
            return res
        else:
            return self._wrapSignUp(res)

    def setPassword(self, password):
        password_arg = parse_arg("password", password)

        res = self.client.mutation(
            'mutation{setPassword(%s){token user{id}}}' % (password_arg))["setPassword"]

        def wrapper(res):
            res["user"] = User(self.client, res["user"]["id"])

            return res

        return wrapWith(res, wrapper)

    def setTotp(self, code, secret):

        code_arg = parse_arg("code", code)
        secret_arg = parse_arg("secret", secret)
        return self.client.mutation('mutation{setTotp(%s%s)}' % (code_arg, secret_arg))["setTotp"]

    def setWebAuthn(self, challengeResponse, jwtChallenge):

        challengeResponse_arg = parse_arg(
            "challengeResponse", challengeResponse)
        jwtChallenge_arg = parse_arg("jwtChallenge", jwtChallenge)
        res = self.client.mutation('mutation{setWebAuthn(%s%s){token user{id}}}' % (
            challengeResponse_arg, jwtChallenge_arg))["setWebAuthn"]

        def wrapper(res):
            res["user"] = User(self.client, res["user"]["id"])

            return res

        return wrapWith(res, wrapper)

    def changeAuthenticationSettings(self, primaryAuthenticationMethods, secondaryAuthenticationMethods):
        primaryAuthenticationMethods_arg = parse_arg(
            "primaryAuthenticationMethods", primaryAuthenticationMethods, is_enum=True)
        secondaryAuthenticationMethods_arg = parse_arg(
            "secondaryAuthenticationMethods", secondaryAuthenticationMethods, is_enum=True)

        res = self.client.mutation('mutation{changeAuthenticationSettings(%s%s){id}}' % (
            primaryAuthenticationMethods_arg, secondaryAuthenticationMethods_arg))["changeAuthenticationSettings"]

        def wrapper(id):
            return User(self.client)

        return wrapById(res, wrapper)

    def resendVerificationEmail(self, email):
        email_arg = parse_arg("email", email)

        return self.client.mutation('mutation{resendVerificationEmail(%s)}' % (email_arg))["resendVerificationEmail"]

    def shareEnvironment(self, environmentId, role, email=None, userId=None):
        environmentId_arg = parse_arg("environmentId", environmentId)
        role_arg = parse_arg("role", role, is_enum=True)
        email_arg = parse_arg("email", email)
        userId_arg = parse_arg("userId", userId)
        res = self.client.mutation('mutation{shareEnvironment(%s%s%s%s){id}}' % (
            environmentId_arg, email_arg, userId_arg, role_arg))["shareEnvironment"]

        def wrapper(id):
            return PendingEnvironmentShare(self.client, id)

        return wrapById(res, wrapper)

    def pendingEnvironmentShare(self, id, role):
        id_arg = parse_arg("id", id)
        role_arg = parse_arg("role", role, is_enum=True)

        res = self.client.mutation('mutation{pendingEnvironmentShare(%s%s){id}}' % (
            id_arg, role_arg))["pendingEnvironmentShare"]

        def wrapper(id):
            return PendingEnvironmentShare(self.client, id)

        return wrapById(res, wrapper)

    def revokePendingEnvironmentShare(self, pendingEnvironmentShareId):
        pendingEnvironmentShareId_arg = parse_arg(
            "pendingEnvironmentShareId", pendingEnvironmentShareId)

        return self.client.mutation('mutation{revokePendingEnvironmentShare(%s)}' % (pendingEnvironmentShareId_arg))["revokePendingEnvironmentShare"]

    def acceptPendingEnvironmentShare(self, pendingEnvironmentShareId):
        pendingEnvironmentShareId_arg = parse_arg(
            "pendingEnvironmentShareId", pendingEnvironmentShareId)

        res = self.client.mutation('mutation{acceptPendingEnvironmentShare(%s){sender{id} receiver{id} role environment{id}}}' % (
            pendingEnvironmentShareId_arg))["acceptPendingEnvironmentShare"]

        def wrapper(res):
            res["sender"] = User(self.client, res["sender"]["id"])
            res["receiver"] = User(self.client, res["receiver"]["id"])
            res["environment"] = Environment(
                self.client, res["environment"]["id"])

            return res

        return wrapWith(res, wrapper)

    def declinePendingEnvironmentShare(self, pendingEnvironmentShareId):
        pendingEnvironmentShareId_arg = parse_arg(
            "pendingEnvironmentShareId", pendingEnvironmentShareId)

        return self.client.mutation('mutation{declinePendingEnvironmentShare(%s)}' % (pendingEnvironmentShareId_arg))["declinePendingEnvironmentShare"]

    def stopSharingEnvironment(self, environmentId, email=None, userId=None):
        environmentId_arg = parse_arg("environmentId", environmentId)
        email_arg = parse_arg("email", email)
        userId_arg = parse_arg("userId", userId)
        res = self.client.mutation('mutation{stopSharingEnvironment(%s%s%s){id}}' % (
            environmentId_arg, email_arg, userId_arg))["stopSharingEnvironment"]

        def wrapper(id):
            return Environment(self.client, id)

        return wrapById(res, wrapper)

    def leaveEnvironment(self, environmentId):
        environmentId_arg = parse_arg("environmentId", environmentId)

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

    def createDevice(self, deviceType=None, firmware=None):
        deviceType_arg = parse_arg("deviceType", deviceType)
        firmware_arg = parse_arg("firmware", firmware)
        res = self.client.mutation('mutation{createDevice(%s%s){id}}' % (
            deviceType_arg, firmware_arg))["createDevice"]

        def wrapper(id):
            return Device(self.client, id)

        return wrapById(res, wrapper)

    def claimDevice(self, deviceId, name, environmentId, index=None, muted=None):
        deviceId_arg = parse_arg("deviceId", deviceId)
        name_arg = parse_arg("name", name)
        environmentId_arg = parse_arg("environmentId", environmentId)
        index_arg = parse_arg("index", index)
        muted_arg = parse_arg("muted", muted)
        res = self.client.mutation('mutation{claimDevice(%s%s%s%s%s){id}}' % (
            deviceId_arg, name_arg, index_arg, environmentId_arg, muted_arg))["claimDevice"]

        def wrapper(id):
            return Device(self.client, id)

        return wrapById(res, wrapper)

    def createNotification(self, deviceId, content, date=None):
        deviceId_arg = parse_arg("deviceId", deviceId)
        content_arg = parse_arg("content", content)
        date_arg = parse_arg("date", date)
        res = self.client.mutation('mutation{createNotification(%s%s%s){id}}' % (
            deviceId_arg, content_arg, date_arg))["createNotification"]

        def wrapper(id):
            return Notification(self.client, id)

        return wrapById(res, wrapper)

    def createFloatValue(self, deviceId, permission, name, private=None, hidden=None, unitOfMeasurement=None, value=None, precision=None, min=None, max=None, cardSize=None, index=None):
        deviceId_arg = parse_arg("deviceId", deviceId)
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
        cardSize_arg = parse_arg("cardSize", cardSize, is_enum=True)
        index_arg = parse_arg("index", index)
        res = self.client.mutation('mutation{createFloatValue(%s%s%s%s%s%s%s%s%s%s%s%s){id}}' % (deviceId_arg, permission_arg, private_arg, hidden_arg,
                                                                                                 unitOfMeasurement_arg, value_arg, precision_arg, min_arg, max_arg, name_arg, cardSize_arg, index_arg))["createFloatValue"]

        def wrapper(id):
            return FloatValue(self.client, id)

        return wrapById(res, wrapper)

    def createStringValue(self, deviceId, permission, name, private=None, hidden=None, value=None, maxChars=None, cardSize=None, allowedValues=None, index=None):
        deviceId_arg = parse_arg("deviceId", deviceId)
        permission_arg = parse_arg("permission", permission, is_enum=True)
        name_arg = parse_arg("name", name)
        private_arg = parse_arg("private", private)
        hidden_arg = parse_arg("hidden", hidden)
        value_arg = parse_arg("value", value)
        maxChars_arg = parse_arg("maxChars", maxChars)
        cardSize_arg = parse_arg("cardSize", cardSize, is_enum=True)
        allowedValues_arg = parse_arg("allowedValues", allowedValues)
        index_arg = parse_arg("index", index)
        res = self.client.mutation('mutation{createStringValue(%s%s%s%s%s%s%s%s%s%s){id}}' % (
            deviceId_arg, permission_arg, private_arg, hidden_arg, value_arg, maxChars_arg, name_arg, cardSize_arg, allowedValues_arg, index_arg))["createStringValue"]

        def wrapper(id):
            return StringValue(self.client, id)

        return wrapById(res, wrapper)

    def createBooleanValue(self, deviceId, permission, name, private=None, hidden=None, value=None, cardSize=None, index=None):
        deviceId_arg = parse_arg("deviceId", deviceId)
        permission_arg = parse_arg("permission", permission, is_enum=True)
        name_arg = parse_arg("name", name)
        private_arg = parse_arg("private", private)
        hidden_arg = parse_arg("hidden", hidden)
        value_arg = parse_arg("value", value)
        cardSize_arg = parse_arg("cardSize", cardSize, is_enum=True)
        index_arg = parse_arg("index", index)
        res = self.client.mutation('mutation{createBooleanValue(%s%s%s%s%s%s%s%s){id}}' % (
            deviceId_arg, permission_arg, private_arg, hidden_arg, value_arg, name_arg, cardSize_arg, index_arg))["createBooleanValue"]

        def wrapper(id):
            return BooleanValue(self.client, id)

        return wrapById(res, wrapper)

    def createFloatSeriesValue(self, deviceId, name, private=None, hidden=None, unitOfMeasurement=None, precision=None, min=None, max=None, cardSize=None, threshold=None, index=None):
        deviceId_arg = parse_arg("deviceId", deviceId)
        name_arg = parse_arg("name", name)
        private_arg = parse_arg("private", private)
        hidden_arg = parse_arg("hidden", hidden)
        unitOfMeasurement_arg = parse_arg(
            "unitOfMeasurement", unitOfMeasurement)
        precision_arg = parse_arg("precision", precision)
        min_arg = parse_arg("min", min)
        max_arg = parse_arg("max", max)
        cardSize_arg = parse_arg("cardSize", cardSize, is_enum=True)
        threshold_arg = parse_arg("threshold", threshold)
        index_arg = parse_arg("index", index)
        res = self.client.mutation('mutation{createFloatSeriesValue(%s%s%s%s%s%s%s%s%s%s%s){id}}' % (
            deviceId_arg, private_arg, hidden_arg, unitOfMeasurement_arg, precision_arg, min_arg, max_arg, name_arg, cardSize_arg, threshold_arg, index_arg))["createFloatSeriesValue"]

        def wrapper(id):
            return FloatSeriesValue(self.client, id)

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

    def createCategorySeriesValue(self, deviceId, name, private=None, hidden=None, cardSize=None, allowedValues=None, index=None):
        deviceId_arg = parse_arg("deviceId", deviceId)
        name_arg = parse_arg("name", name)
        private_arg = parse_arg("private", private)
        hidden_arg = parse_arg("hidden", hidden)
        cardSize_arg = parse_arg("cardSize", cardSize, is_enum=True)
        allowedValues_arg = parse_arg("allowedValues", allowedValues)
        index_arg = parse_arg("index", index)
        res = self.client.mutation('mutation{createCategorySeriesValue(%s%s%s%s%s%s%s){id}}' % (
            deviceId_arg, private_arg, hidden_arg, name_arg, cardSize_arg, allowedValues_arg, index_arg))["createCategorySeriesValue"]

        def wrapper(id):
            return CategorySeriesValue(self.client, id)

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

    def user(self, quietMode=None, devMode=None, paymentPlan=None, name=None, profileIcon=None):

        quietMode_arg = parse_arg("quietMode", quietMode)
        devMode_arg = parse_arg("devMode", devMode)
        paymentPlan_arg = parse_arg("paymentPlan", paymentPlan)
        name_arg = parse_arg("name", name)
        profileIcon_arg = parse_arg("profileIcon", profileIcon)
        res = self.client.mutation('mutation{user(%s%s%s%s%s){id}}' % (
            quietMode_arg, devMode_arg, paymentPlan_arg, name_arg, profileIcon_arg))["user"]

        def wrapper(id):
            return User(self.client)

        return wrapById(res, wrapper)

    def changeEmail(self, newEmail):
        newEmail_arg = parse_arg("newEmail", newEmail)

        return self.client.mutation('mutation{changeEmail(%s)}' % (newEmail_arg))["changeEmail"]

    def settings(self, language=None, lengthAndMass=None, temperature=None, dateFormat=None, timeFormat=None, passwordChangeEmail=None, pendingOwnerChangeReceivedEmail=None, pendingEnvironmentShareReceivedEmail=None, pendingOwnerChangeAcceptedEmail=None, pendingEnvironmentShareAcceptedEmail=None, permanentTokenCreatedEmail=None):

        language_arg = parse_arg("language", language)
        lengthAndMass_arg = parse_arg(
            "lengthAndMass", lengthAndMass, is_enum=True)
        temperature_arg = parse_arg("temperature", temperature, is_enum=True)
        dateFormat_arg = parse_arg("dateFormat", dateFormat, is_enum=True)
        timeFormat_arg = parse_arg("timeFormat", timeFormat, is_enum=True)
        passwordChangeEmail_arg = parse_arg(
            "passwordChangeEmail", passwordChangeEmail)
        pendingOwnerChangeReceivedEmail_arg = parse_arg(
            "pendingOwnerChangeReceivedEmail", pendingOwnerChangeReceivedEmail)
        pendingEnvironmentShareReceivedEmail_arg = parse_arg(
            "pendingEnvironmentShareReceivedEmail", pendingEnvironmentShareReceivedEmail)
        pendingOwnerChangeAcceptedEmail_arg = parse_arg(
            "pendingOwnerChangeAcceptedEmail", pendingOwnerChangeAcceptedEmail)
        pendingEnvironmentShareAcceptedEmail_arg = parse_arg(
            "pendingEnvironmentShareAcceptedEmail", pendingEnvironmentShareAcceptedEmail)
        permanentTokenCreatedEmail_arg = parse_arg(
            "permanentTokenCreatedEmail", permanentTokenCreatedEmail)

        return self.client.mutation('mutation{settings(%s%s%s%s%s%s%s%s%s%s%s){id lengthAndMass temperature timeFormat dateFormat language passwordChangeEmail pendingOwnerChangeReceivedEmail pendingEnvironmentShareReceivedEmail pendingOwnerChangeAcceptedEmail pendingEnvironmentShareAcceptedEmail permanentTokenCreatedEmail}}' % (language_arg, lengthAndMass_arg, temperature_arg, dateFormat_arg, timeFormat_arg, passwordChangeEmail_arg, pendingOwnerChangeReceivedEmail_arg, pendingEnvironmentShareReceivedEmail_arg, pendingOwnerChangeAcceptedEmail_arg, pendingEnvironmentShareAcceptedEmail_arg, permanentTokenCreatedEmail_arg))["settings"]

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

    def device(self, id, deviceType=None, name=None, index=None, signalStatus=None, batteryStatus=None, batteryCharging=None, firmware=None, muted=None, starred=None):
        id_arg = parse_arg("id", id)
        deviceType_arg = parse_arg("deviceType", deviceType)
        name_arg = parse_arg("name", name)
        index_arg = parse_arg("index", index)
        signalStatus_arg = parse_arg("signalStatus", signalStatus)
        batteryStatus_arg = parse_arg("batteryStatus", batteryStatus)
        batteryCharging_arg = parse_arg("batteryCharging", batteryCharging)
        firmware_arg = parse_arg("firmware", firmware)
        muted_arg = parse_arg("muted", muted)
        starred_arg = parse_arg("starred", starred)
        res = self.client.mutation('mutation{device(%s%s%s%s%s%s%s%s%s%s){id}}' % (
            id_arg, deviceType_arg, name_arg, index_arg, signalStatus_arg, batteryStatus_arg, batteryCharging_arg, firmware_arg, muted_arg, starred_arg))["device"]

        def wrapper(id):
            return Device(self.client, id)

        return wrapById(res, wrapper)

    def value(self, id, private=None, hidden=None, cardSize=None, name=None, index=None):
        id_arg = parse_arg("id", id)
        private_arg = parse_arg("private", private)
        hidden_arg = parse_arg("hidden", hidden)
        cardSize_arg = parse_arg("cardSize", cardSize, is_enum=True)
        name_arg = parse_arg("name", name)
        index_arg = parse_arg("index", index)
        res = self.client.mutation('mutation{value(%s%s%s%s%s%s){id __typename}}' % (
            id_arg, private_arg, hidden_arg, cardSize_arg, name_arg, index_arg))["value"]

        def wrapper(res):
            if res["__typename"] == "FloatValue":
                return FloatValue(self.client, res["id"])
            elif res["__typename"] == "StringValue":
                return StringValue(self.client, res["id"])
            elif res["__typename"] == "BooleanValue":
                return BooleanValue(self.client, res["id"])
            elif res["__typename"] == "FloatSeriesValue":
                return FloatSeriesValue(self.client, res["id"])
            elif res["__typename"] == "CategorySeriesValue":
                return CategorySeriesValue(self.client, res["id"])
            elif res["__typename"] == "FileValue":
                return FileValue(self.client, res["id"])
            else:
                return res

        return wrapWith(res, wrapper)

    def moveDevice(self, deviceId, newEnvironmentId):
        deviceId_arg = parse_arg("deviceId", deviceId)
        newEnvironmentId_arg = parse_arg("newEnvironmentId", newEnvironmentId)

        res = self.client.mutation('mutation{moveDevice(%s%s){id}}' % (
            deviceId_arg, newEnvironmentId_arg))["moveDevice"]

        def wrapper(id):
            return Device(self.client, id)

        return wrapById(res, wrapper)

    def resetOnlineState(self, deviceId):
        deviceId_arg = parse_arg("deviceId", deviceId)

        res = self.client.mutation('mutation{resetOnlineState(%s){id}}' % (deviceId_arg))[
            "resetOnlineState"]

        def wrapper(id):
            return Device(self.client, id)

        return wrapById(res, wrapper)

    def floatValue(self, id, permission=None, private=None, hidden=None, unitOfMeasurement=None, value=None, precision=None, min=None, max=None, name=None, cardSize=None, index=None):
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
        cardSize_arg = parse_arg("cardSize", cardSize, is_enum=True)
        index_arg = parse_arg("index", index)
        res = self.client.mutation('mutation{floatValue(%s%s%s%s%s%s%s%s%s%s%s%s){id}}' % (
            id_arg, permission_arg, private_arg, hidden_arg, unitOfMeasurement_arg, value_arg, precision_arg, min_arg, max_arg, name_arg, cardSize_arg, index_arg))["floatValue"]

        def wrapper(id):
            return FloatValue(self.client, id)

        return wrapById(res, wrapper)

    def atomicUpdateFloat(self, id, incrementBy):
        id_arg = parse_arg("id", id)
        incrementBy_arg = parse_arg("incrementBy", incrementBy)

        res = self.client.mutation('mutation{atomicUpdateFloat(%s%s){id}}' % (
            id_arg, incrementBy_arg))["atomicUpdateFloat"]

        def wrapper(id):
            return FloatValue(self.client, id)

        return wrapById(res, wrapper)

    def stringValue(self, id, permission=None, private=None, hidden=None, value=None, maxChars=None, name=None, cardSize=None, allowedValues=None, index=None):
        id_arg = parse_arg("id", id)
        permission_arg = parse_arg("permission", permission, is_enum=True)
        private_arg = parse_arg("private", private)
        hidden_arg = parse_arg("hidden", hidden)
        value_arg = parse_arg("value", value)
        maxChars_arg = parse_arg("maxChars", maxChars)
        name_arg = parse_arg("name", name)
        cardSize_arg = parse_arg("cardSize", cardSize, is_enum=True)
        allowedValues_arg = parse_arg("allowedValues", allowedValues)
        index_arg = parse_arg("index", index)
        res = self.client.mutation('mutation{stringValue(%s%s%s%s%s%s%s%s%s%s){id}}' % (
            id_arg, permission_arg, private_arg, hidden_arg, value_arg, maxChars_arg, name_arg, cardSize_arg, allowedValues_arg, index_arg))["stringValue"]

        def wrapper(id):
            return StringValue(self.client, id)

        return wrapById(res, wrapper)

    def booleanValue(self, id, permission=None, private=None, hidden=None, value=None, name=None, cardSize=None, index=None):
        id_arg = parse_arg("id", id)
        permission_arg = parse_arg("permission", permission, is_enum=True)
        private_arg = parse_arg("private", private)
        hidden_arg = parse_arg("hidden", hidden)
        value_arg = parse_arg("value", value)
        name_arg = parse_arg("name", name)
        cardSize_arg = parse_arg("cardSize", cardSize, is_enum=True)
        index_arg = parse_arg("index", index)
        res = self.client.mutation('mutation{booleanValue(%s%s%s%s%s%s%s%s){id}}' % (
            id_arg, permission_arg, private_arg, hidden_arg, value_arg, name_arg, cardSize_arg, index_arg))["booleanValue"]

        def wrapper(id):
            return BooleanValue(self.client, id)

        return wrapById(res, wrapper)

    def floatSeriesValue(self, id, private=None, hidden=None, unitOfMeasurement=None, precision=None, min=None, max=None, name=None, cardSize=None, threshold=None, index=None):
        id_arg = parse_arg("id", id)
        private_arg = parse_arg("private", private)
        hidden_arg = parse_arg("hidden", hidden)
        unitOfMeasurement_arg = parse_arg(
            "unitOfMeasurement", unitOfMeasurement)
        precision_arg = parse_arg("precision", precision)
        min_arg = parse_arg("min", min)
        max_arg = parse_arg("max", max)
        name_arg = parse_arg("name", name)
        cardSize_arg = parse_arg("cardSize", cardSize, is_enum=True)
        threshold_arg = parse_arg("threshold", threshold)
        index_arg = parse_arg("index", index)
        res = self.client.mutation('mutation{floatSeriesValue(%s%s%s%s%s%s%s%s%s%s%s){id}}' % (
            id_arg, private_arg, hidden_arg, unitOfMeasurement_arg, precision_arg, min_arg, max_arg, name_arg, cardSize_arg, threshold_arg, index_arg))["floatSeriesValue"]

        def wrapper(id):
            return FloatSeriesValue(self.client, id)

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

    def categorySeriesValue(self, id, private=None, hidden=None, name=None, cardSize=None, allowedValues=None, index=None):
        id_arg = parse_arg("id", id)
        private_arg = parse_arg("private", private)
        hidden_arg = parse_arg("hidden", hidden)
        name_arg = parse_arg("name", name)
        cardSize_arg = parse_arg("cardSize", cardSize, is_enum=True)
        allowedValues_arg = parse_arg("allowedValues", allowedValues)
        index_arg = parse_arg("index", index)
        res = self.client.mutation('mutation{categorySeriesValue(%s%s%s%s%s%s%s){id}}' % (
            id_arg, private_arg, hidden_arg, name_arg, cardSize_arg, allowedValues_arg, index_arg))["categorySeriesValue"]

        def wrapper(id):
            return CategorySeriesValue(self.client, id)

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

    def deleteDevice(self, id):
        id_arg = parse_arg("id", id)

        return self.client.mutation('mutation{deleteDevice(%s)}' % (id_arg))["deleteDevice"]

    def unclaimDevice(self, id):
        id_arg = parse_arg("id", id)

        return self.client.mutation('mutation{unclaimDevice(%s){id}}' % (id_arg))["unclaimDevice"]

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
