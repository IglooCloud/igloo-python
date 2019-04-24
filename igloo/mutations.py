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
        email_arg = 'email:"%s",' % email
        password_arg = 'password:"%s",' % password

        return self.client.mutation('mutation{verifyPassword(%s%s)}' % (email_arg, password_arg))["verifyPassword"]

    def verifyWebAuthn(self, challengeResponse, jwtChallenge):
        challengeResponse_arg = 'challengeResponse:"%s",' % challengeResponse
        jwtChallenge_arg = 'jwtChallenge:"%s",' % jwtChallenge

        return self.client.mutation('mutation{verifyWebAuthn(%s%s)}' % (challengeResponse_arg, jwtChallenge_arg))["verifyWebAuthn"]

    def verifyTotp(self, email=None, code=None):

        email_arg = 'email:"%s",' % email if email is not None else ''
        code_arg = 'code:"%s",' % code if code is not None else ''
        return self.client.mutation('mutation{verifyTotp(%s%s)}' % (email_arg, code_arg))["verifyTotp"]

    def verifyEmailToken(self, token):
        token_arg = 'token:"%s",' % token

        return self.client.mutation('mutation{verifyEmailToken(%s)}' % (token_arg))["verifyEmailToken"]

    def sendConfirmationEmail(self, email, operation):
        email_arg = 'email:"%s",' % email
        operation_arg = 'operation:%s,' % operation

        return self.client.mutation('mutation{sendConfirmationEmail(%s%s)}' % (email_arg, operation_arg))["sendConfirmationEmail"]

    async def _wrapLogIn(self, res):
        resDict = await res
        self.client.set_token(resDict["token"])
        resDict["user"] = User(self.client)
        return resDict

    def logIn(self, passwordCertificate=None, webAuthnCertificate=None, totpCertificate=None, emailCertificate=None):

        passwordCertificate_arg = 'passwordCertificate:"%s",' % passwordCertificate if passwordCertificate is not None else ''
        webAuthnCertificate_arg = 'webAuthnCertificate:"%s",' % webAuthnCertificate if webAuthnCertificate is not None else ''
        totpCertificate_arg = 'totpCertificate:"%s",' % totpCertificate if totpCertificate is not None else ''
        emailCertificate_arg = 'emailCertificate:"%s",' % emailCertificate if emailCertificate is not None else ''

        res = self.client.mutation('mutation{logIn(%s%s%s%s){user{id} token}}' % (
            passwordCertificate_arg, webAuthnCertificate_arg, totpCertificate_arg, emailCertificate_arg))["logIn"]

        if isinstance(res, dict):
            self.client.set_token(res["token"])
            res["user"] = User(self.client)
            return res
        else:
            return self._wrapLogIn(res)

    def createToken(self, tokenType, passwordCertificate=None, webAuthnCertificate=None, totpCertificate=None, emailCertificate=None):
        tokenType_arg = 'tokenType:%s,' % tokenType
        passwordCertificate_arg = 'passwordCertificate:"%s",' % passwordCertificate if passwordCertificate is not None else ''
        webAuthnCertificate_arg = 'webAuthnCertificate:"%s",' % webAuthnCertificate if webAuthnCertificate is not None else ''
        totpCertificate_arg = 'totpCertificate:"%s",' % totpCertificate if totpCertificate is not None else ''
        emailCertificate_arg = 'emailCertificate:"%s",' % emailCertificate if emailCertificate is not None else ''
        return self.client.mutation('mutation{createToken(%s%s%s%s%s)}' % (passwordCertificate_arg, webAuthnCertificate_arg, totpCertificate_arg, emailCertificate_arg, tokenType_arg))["createToken"]

    def createPermanentToken(self, name):
        name_arg = 'name:"%s",' % name

        res = self.client.mutation('mutation{createPermanentToken(%s){id}}' % (name_arg))[
            "createPermanentToken"]

        def wrapper(id):
            return PermanentToken(self.client, id)

        return wrapById(res, wrapper)

    def regeneratePermanentToken(self, id):
        id_arg = 'id:"%s",' % id

        return self.client.mutation('mutation{regeneratePermanentToken(%s)}' % (id_arg))["regeneratePermanentToken"]

    def deletePermanentToken(self, id):
        id_arg = 'id:"%s",' % id

        return self.client.mutation('mutation{deletePermanentToken(%s)}' % (id_arg))["deletePermanentToken"]

    async def _wrapSignUp(self, res):
        result = await res
        result["user"] = User(self.client)

        return result

    def signUp(self, email, name):
        email_arg = 'email:"%s",' % email
        name_arg = 'name:"%s",' % name

        res = self.client.mutation('mutation{signUp(%s%s){user{id} changeAuthenticationToken}}' % (
            email_arg, name_arg))["signUp"]

        if isinstance(res, dict):
            res["user"] = User(self.client, res["user"]["id"])
            return res
        else:
            return self._wrapSignUp(res)

    def setPassword(self, password):
        password_arg = 'password:"%s",' % password

        res = self.client.mutation(
            'mutation{setPassword(%s){token user{id}}}' % (password_arg))["setPassword"]

        def wrapper(res):
            res["user"] = User(self.client, res["user"]["id"])

            return res

        return wrapWith(res, wrapper)

    def setTotp(self, code=None, secret=None):

        code_arg = 'code:"%s",' % code if code is not None else ''
        secret_arg = 'secret:"%s",' % secret if secret is not None else ''
        return self.client.mutation('mutation{setTotp(%s%s)}' % (code_arg, secret_arg))["setTotp"]

    def setWebAuthn(self, challengeResponse=None, jwtChallenge=None):

        challengeResponse_arg = 'challengeResponse:"%s",' % challengeResponse if challengeResponse is not None else ''
        jwtChallenge_arg = 'jwtChallenge:"%s",' % jwtChallenge if jwtChallenge is not None else ''
        res = self.client.mutation('mutation{setWebAuthn(%s%s){token user{id}}}' % (
            challengeResponse_arg, jwtChallenge_arg))["setWebAuthn"]

        def wrapper(res):
            res["user"] = User(self.client, res["user"]["id"])

            return res

        return wrapWith(res, wrapper)

    def changeAuthenticationSettings(self, primaryAuthenticationMethods, secondaryAuthenticationMethods):
        primaryAuthenticationMethods_arg = 'primaryAuthenticationMethods:%s,' % primaryAuthenticationMethods
        secondaryAuthenticationMethods_arg = 'secondaryAuthenticationMethods:%s,' % secondaryAuthenticationMethods

        res = self.client.mutation('mutation{changeAuthenticationSettings(%s%s){id}}' % (
            primaryAuthenticationMethods_arg, secondaryAuthenticationMethods_arg))["changeAuthenticationSettings"]

        def wrapper(id):
            return User(self.client)

        return wrapById(res, wrapper)

    def resendVerificationEmail(self, email):
        email_arg = 'email:"%s",' % email

        return self.client.mutation('mutation{resendVerificationEmail(%s)}' % (email_arg))["resendVerificationEmail"]

    def shareEnvironment(self, environmentId, role, email=None, userId=None):
        environmentId_arg = 'environmentId:"%s",' % environmentId
        role_arg = 'role:%s,' % role
        email_arg = 'email:"%s",' % email if email is not None else ''
        userId_arg = 'userId:"%s",' % userId if userId is not None else ''
        res = self.client.mutation('mutation{shareEnvironment(%s%s%s%s){id}}' % (
            environmentId_arg, email_arg, userId_arg, role_arg))["shareEnvironment"]

        def wrapper(id):
            return PendingEnvironmentShare(self.client, id)

        return wrapById(res, wrapper)

    def pendingEnvironmentShare(self, id, role):
        id_arg = 'id:"%s",' % id
        role_arg = 'role:%s,' % role

        res = self.client.mutation('mutation{pendingEnvironmentShare(%s%s){id}}' % (
            id_arg, role_arg))["pendingEnvironmentShare"]

        def wrapper(id):
            return PendingEnvironmentShare(self.client, id)

        return wrapById(res, wrapper)

    def revokePendingEnvironmentShare(self, pendingEnvironmentShareId):
        pendingEnvironmentShareId_arg = 'pendingEnvironmentShareId:"%s",' % pendingEnvironmentShareId

        return self.client.mutation('mutation{revokePendingEnvironmentShare(%s)}' % (pendingEnvironmentShareId_arg))["revokePendingEnvironmentShare"]

    def acceptPendingEnvironmentShare(self, pendingEnvironmentShareId):
        pendingEnvironmentShareId_arg = 'pendingEnvironmentShareId:"%s",' % pendingEnvironmentShareId

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
        pendingEnvironmentShareId_arg = 'pendingEnvironmentShareId:"%s",' % pendingEnvironmentShareId

        return self.client.mutation('mutation{declinePendingEnvironmentShare(%s)}' % (pendingEnvironmentShareId_arg))["declinePendingEnvironmentShare"]

    def stopSharingEnvironment(self, environmentId, email=None, userId=None):
        environmentId_arg = 'environmentId:"%s",' % environmentId
        email_arg = 'email:"%s",' % email if email is not None else ''
        userId_arg = 'userId:"%s",' % userId if userId is not None else ''
        res = self.client.mutation('mutation{stopSharingEnvironment(%s%s%s){id}}' % (
            environmentId_arg, email_arg, userId_arg))["stopSharingEnvironment"]

        def wrapper(id):
            return Environment(self.client, id)

        return wrapById(res, wrapper)

    def leaveEnvironment(self, environmentId):
        environmentId_arg = 'environmentId:"%s",' % environmentId

        return self.client.mutation('mutation{leaveEnvironment(%s)}' % (environmentId_arg))["leaveEnvironment"]

    def changeOwner(self, environmentId, email=None, userId=None):
        environmentId_arg = 'environmentId:"%s",' % environmentId
        email_arg = 'email:"%s",' % email if email is not None else ''
        userId_arg = 'userId:"%s",' % userId if userId is not None else ''
        res = self.client.mutation('mutation{changeOwner(%s%s%s){id}}' % (
            environmentId_arg, email_arg, userId_arg))["changeOwner"]

        def wrapper(id):
            return PendingOwnerChange(self.client, id)

        return wrapById(res, wrapper)

    def revokePendingOwnerChange(self, pendingOwnerChangeId):
        pendingOwnerChangeId_arg = 'pendingOwnerChangeId:"%s",' % pendingOwnerChangeId

        return self.client.mutation('mutation{revokePendingOwnerChange(%s)}' % (pendingOwnerChangeId_arg))["revokePendingOwnerChange"]

    def acceptPendingOwnerChange(self, pendingOwnerChangeId):
        pendingOwnerChangeId_arg = 'pendingOwnerChangeId:"%s",' % pendingOwnerChangeId

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
        pendingOwnerChangeId_arg = 'pendingOwnerChangeId:"%s",' % pendingOwnerChangeId

        return self.client.mutation('mutation{declinePendingOwnerChange(%s)}' % (pendingOwnerChangeId_arg))["declinePendingOwnerChange"]

    def changeRole(self, environmentId, email, newRole):
        environmentId_arg = 'environmentId:"%s",' % environmentId
        email_arg = 'email:"%s",' % email
        newRole_arg = 'newRole:%s,' % newRole

        res = self.client.mutation('mutation{changeRole(%s%s%s){id}}' % (
            environmentId_arg, email_arg, newRole_arg))["changeRole"]

        def wrapper(id):
            return Environment(self.client, id)

        return wrapById(res, wrapper)

    def createEnvironment(self, name, picture=None, index=None, muted=None):
        name_arg = 'name:"%s",' % name
        picture_arg = 'picture:%s,' % picture if picture is not None else ''
        index_arg = 'index:%s,' % index if index is not None else ''
        muted_arg = 'muted:%s,' % muted if muted is not None else ''
        res = self.client.mutation('mutation{createEnvironment(%s%s%s%s){id}}' % (
            name_arg, picture_arg, index_arg, muted_arg))["createEnvironment"]

        def wrapper(id):
            return Environment(self.client, id)

        return wrapById(res, wrapper)

    def createDevice(self, deviceType=None, firmware=None):
        deviceType_arg = 'deviceType:"%s",' % deviceType if deviceType is not None else ''
        firmware_arg = 'firmware:"%s",' % firmware if firmware is not None else ''
        res = self.client.mutation('mutation{createDevice(%s%s){id}}' % (
            deviceType_arg, firmware_arg))["createDevice"]

        def wrapper(id):
            return Device(self.client, id)

        return wrapById(res, wrapper)

    def claimDevice(self, deviceId, name, environmentId, index=None, muted=None):
        deviceId_arg = 'deviceId:"%s",' % deviceId
        name_arg = 'name:"%s",' % name
        environmentId_arg = 'environmentId:"%s",' % environmentId
        index_arg = 'index:%s,' % index if index is not None else ''
        muted_arg = 'muted:%s,' % muted if muted is not None else ''
        res = self.client.mutation('mutation{claimDevice(%s%s%s%s%s){id}}' % (
            deviceId_arg, name_arg, index_arg, environmentId_arg, muted_arg))["claimDevice"]

        def wrapper(id):
            return Device(self.client, id)

        return wrapById(res, wrapper)

    def createNotification(self, deviceId, content, date=None):
        deviceId_arg = 'deviceId:"%s",' % deviceId
        content_arg = 'content:"%s",' % content
        date_arg = 'date:%s,' % date if date is not None else ''
        res = self.client.mutation('mutation{createNotification(%s%s%s){id}}' % (
            deviceId_arg, content_arg, date_arg))["createNotification"]

        def wrapper(id):
            return Notification(self.client, id)

        return wrapById(res, wrapper)

    def createFloatValue(self, deviceId, permission, name, private=None, hidden=None, unitOfMeasurement=None, value=None, precision=None, min=None, max=None, cardSize=None, index=None):
        deviceId_arg = 'deviceId:"%s",' % deviceId
        permission_arg = 'permission:%s,' % permission
        name_arg = 'name:"%s",' % name
        private_arg = 'private:%s,' % private if private is not None else ''
        hidden_arg = 'hidden:%s,' % hidden if hidden is not None else ''
        unitOfMeasurement_arg = 'unitOfMeasurement:"%s",' % unitOfMeasurement if unitOfMeasurement is not None else ''
        value_arg = 'value:%s,' % value if value is not None else ''
        precision_arg = 'precision:%s,' % precision if precision is not None else ''
        min_arg = 'min:%s,' % min if min is not None else ''
        max_arg = 'max:%s,' % max if max is not None else ''
        cardSize_arg = 'cardSize:%s,' % cardSize if cardSize is not None else ''
        index_arg = 'index:%s,' % index if index is not None else ''
        res = self.client.mutation('mutation{createFloatValue(%s%s%s%s%s%s%s%s%s%s%s%s){id}}' % (deviceId_arg, permission_arg, private_arg, hidden_arg,
                                                                                                 unitOfMeasurement_arg, value_arg, precision_arg, min_arg, max_arg, name_arg, cardSize_arg, index_arg))["createFloatValue"]

        def wrapper(id):
            return FloatValue(self.client, id)

        return wrapById(res, wrapper)

    def createStringValue(self, deviceId, permission, name, private=None, hidden=None, value=None, maxChars=None, cardSize=None, allowedValues=None, index=None):
        deviceId_arg = 'deviceId:"%s",' % deviceId
        permission_arg = 'permission:%s,' % permission
        name_arg = 'name:"%s",' % name
        private_arg = 'private:%s,' % private if private is not None else ''
        hidden_arg = 'hidden:%s,' % hidden if hidden is not None else ''
        value_arg = 'value:"%s",' % value if value is not None else ''
        maxChars_arg = 'maxChars:%s,' % maxChars if maxChars is not None else ''
        cardSize_arg = 'cardSize:%s,' % cardSize if cardSize is not None else ''
        allowedValues_arg = 'allowedValues:%s,' % allowedValues if allowedValues is not None else ''
        index_arg = 'index:%s,' % index if index is not None else ''
        res = self.client.mutation('mutation{createStringValue(%s%s%s%s%s%s%s%s%s%s){id}}' % (
            deviceId_arg, permission_arg, private_arg, hidden_arg, value_arg, maxChars_arg, name_arg, cardSize_arg, allowedValues_arg, index_arg))["createStringValue"]

        def wrapper(id):
            return StringValue(self.client, id)

        return wrapById(res, wrapper)

    def createBooleanValue(self, deviceId, permission, name, private=None, hidden=None, value=None, cardSize=None, index=None):
        deviceId_arg = 'deviceId:"%s",' % deviceId
        permission_arg = 'permission:%s,' % permission
        name_arg = 'name:"%s",' % name
        private_arg = 'private:%s,' % private if private is not None else ''
        hidden_arg = 'hidden:%s,' % hidden if hidden is not None else ''
        value_arg = 'value:%s,' % value if value is not None else ''
        cardSize_arg = 'cardSize:%s,' % cardSize if cardSize is not None else ''
        index_arg = 'index:%s,' % index if index is not None else ''
        res = self.client.mutation('mutation{createBooleanValue(%s%s%s%s%s%s%s%s){id}}' % (
            deviceId_arg, permission_arg, private_arg, hidden_arg, value_arg, name_arg, cardSize_arg, index_arg))["createBooleanValue"]

        def wrapper(id):
            return BooleanValue(self.client, id)

        return wrapById(res, wrapper)

    def createFloatSeriesValue(self, deviceId, name, private=None, hidden=None, unitOfMeasurement=None, precision=None, min=None, max=None, cardSize=None, threshold=None, index=None):
        deviceId_arg = 'deviceId:"%s",' % deviceId
        name_arg = 'name:"%s",' % name
        private_arg = 'private:%s,' % private if private is not None else ''
        hidden_arg = 'hidden:%s,' % hidden if hidden is not None else ''
        unitOfMeasurement_arg = 'unitOfMeasurement:"%s",' % unitOfMeasurement if unitOfMeasurement is not None else ''
        precision_arg = 'precision:%s,' % precision if precision is not None else ''
        min_arg = 'min:%s,' % min if min is not None else ''
        max_arg = 'max:%s,' % max if max is not None else ''
        cardSize_arg = 'cardSize:%s,' % cardSize if cardSize is not None else ''
        threshold_arg = 'threshold:%s,' % threshold if threshold is not None else ''
        index_arg = 'index:%s,' % index if index is not None else ''
        res = self.client.mutation('mutation{createFloatSeriesValue(%s%s%s%s%s%s%s%s%s%s%s){id}}' % (
            deviceId_arg, private_arg, hidden_arg, unitOfMeasurement_arg, precision_arg, min_arg, max_arg, name_arg, cardSize_arg, threshold_arg, index_arg))["createFloatSeriesValue"]

        def wrapper(id):
            return FloatSeriesValue(self.client, id)

        return wrapById(res, wrapper)

    def createFloatSeriesNode(self, seriesId, value, timestamp=None):
        seriesId_arg = 'seriesId:"%s",' % seriesId
        value_arg = 'value:%s,' % value
        timestamp_arg = 'timestamp:"%s",' % timestamp if timestamp is not None else ''
        res = self.client.mutation('mutation{createFloatSeriesNode(%s%s%s){id}}' % (
            seriesId_arg, timestamp_arg, value_arg))["createFloatSeriesNode"]

        def wrapper(id):
            return FloatSeriesNode(self.client, id)

        return wrapById(res, wrapper)

    def createCategorySeriesValue(self, deviceId, name, private=None, hidden=None, cardSize=None, allowedValues=None, index=None):
        deviceId_arg = 'deviceId:"%s",' % deviceId
        name_arg = 'name:"%s",' % name
        private_arg = 'private:%s,' % private if private is not None else ''
        hidden_arg = 'hidden:%s,' % hidden if hidden is not None else ''
        cardSize_arg = 'cardSize:%s,' % cardSize if cardSize is not None else ''
        allowedValues_arg = 'allowedValues:%s,' % allowedValues if allowedValues is not None else ''
        index_arg = 'index:%s,' % index if index is not None else ''
        res = self.client.mutation('mutation{createCategorySeriesValue(%s%s%s%s%s%s%s){id}}' % (
            deviceId_arg, private_arg, hidden_arg, name_arg, cardSize_arg, allowedValues_arg, index_arg))["createCategorySeriesValue"]

        def wrapper(id):
            return CategorySeriesValue(self.client, id)

        return wrapById(res, wrapper)

    def createCategorySeriesNode(self, seriesId, value, timestamp=None):
        seriesId_arg = 'seriesId:"%s",' % seriesId
        value_arg = 'value:"%s",' % value
        timestamp_arg = 'timestamp:"%s",' % timestamp if timestamp is not None else ''
        res = self.client.mutation('mutation{createCategorySeriesNode(%s%s%s){id}}' % (
            seriesId_arg, timestamp_arg, value_arg))["createCategorySeriesNode"]

        def wrapper(id):
            return CategorySeriesNode(self.client, id)

        return wrapById(res, wrapper)

    def user(self, quietMode=None, devMode=None, paymentPlan=None, name=None, profileIcon=None):

        quietMode_arg = 'quietMode:%s,' % quietMode if quietMode is not None else ''
        devMode_arg = 'devMode:%s,' % devMode if devMode is not None else ''
        paymentPlan_arg = 'paymentPlan:%s,' % paymentPlan if paymentPlan is not None else ''
        name_arg = 'name:"%s",' % name if name is not None else ''
        profileIcon_arg = 'profileIcon:"%s",' % profileIcon if profileIcon is not None else ''
        res = self.client.mutation('mutation{user(%s%s%s%s%s){id}}' % (
            quietMode_arg, devMode_arg, paymentPlan_arg, name_arg, profileIcon_arg))["user"]

        def wrapper(id):
            return User(self.client)

        return wrapById(res, wrapper)

    def changeEmail(self, newEmail):
        newEmail_arg = 'newEmail:"%s",' % newEmail

        return self.client.mutation('mutation{changeEmail(%s)}' % (newEmail_arg))["changeEmail"]

    def settings(self, language=None, lengthAndMass=None, temperature=None, dateFormat=None, timeFormat=None, passwordChangeEmail=None, pendingOwnerChangeReceivedEmail=None, pendingEnvironmentShareReceivedEmail=None, pendingOwnerChangeAcceptedEmail=None, pendingEnvironmentShareAcceptedEmail=None, permanentTokenCreatedEmail=None):

        language_arg = 'language:"%s",' % language if language is not None else ''
        lengthAndMass_arg = 'lengthAndMass:%s,' % lengthAndMass if lengthAndMass is not None else ''
        temperature_arg = 'temperature:%s,' % temperature if temperature is not None else ''
        dateFormat_arg = 'dateFormat:%s,' % dateFormat if dateFormat is not None else ''
        timeFormat_arg = 'timeFormat:%s,' % timeFormat if timeFormat is not None else ''
        passwordChangeEmail_arg = 'passwordChangeEmail:%s,' % passwordChangeEmail if passwordChangeEmail is not None else ''
        pendingOwnerChangeReceivedEmail_arg = 'pendingOwnerChangeReceivedEmail:%s,' % pendingOwnerChangeReceivedEmail if pendingOwnerChangeReceivedEmail is not None else ''
        pendingEnvironmentShareReceivedEmail_arg = 'pendingEnvironmentShareReceivedEmail:%s,' % pendingEnvironmentShareReceivedEmail if pendingEnvironmentShareReceivedEmail is not None else ''
        pendingOwnerChangeAcceptedEmail_arg = 'pendingOwnerChangeAcceptedEmail:%s,' % pendingOwnerChangeAcceptedEmail if pendingOwnerChangeAcceptedEmail is not None else ''
        pendingEnvironmentShareAcceptedEmail_arg = 'pendingEnvironmentShareAcceptedEmail:%s,' % pendingEnvironmentShareAcceptedEmail if pendingEnvironmentShareAcceptedEmail is not None else ''
        permanentTokenCreatedEmail_arg = 'permanentTokenCreatedEmail:%s,' % permanentTokenCreatedEmail if permanentTokenCreatedEmail is not None else ''

        return self.client.mutation('mutation{settings(%s%s%s%s%s%s%s%s%s%s%s){id lengthAndMass temperature timeFormat dateFormat language passwordChangeEmail pendingOwnerChangeReceivedEmail pendingEnvironmentShareReceivedEmail pendingOwnerChangeAcceptedEmail pendingEnvironmentShareAcceptedEmail permanentTokenCreatedEmail}}' % (language_arg, lengthAndMass_arg, temperature_arg, dateFormat_arg, timeFormat_arg, passwordChangeEmail_arg, pendingOwnerChangeReceivedEmail_arg, pendingEnvironmentShareReceivedEmail_arg, pendingOwnerChangeAcceptedEmail_arg, pendingEnvironmentShareAcceptedEmail_arg, permanentTokenCreatedEmail_arg))["settings"]

    def updatePaymentInfo(self, stripeToken):
        stripeToken_arg = 'stripeToken:"%s",' % stripeToken

        return self.client.mutation('mutation{updatePaymentInfo(%s)}' % (stripeToken_arg))["updatePaymentInfo"]

    def environment(self, id, name=None, picture=None, index=None, muted=None):
        id_arg = 'id:"%s",' % id
        name_arg = 'name:"%s",' % name if name is not None else ''
        picture_arg = 'picture:%s,' % picture if picture is not None else ''
        index_arg = 'index:%s,' % index if index is not None else ''
        muted_arg = 'muted:%s,' % muted if muted is not None else ''
        res = self.client.mutation('mutation{environment(%s%s%s%s%s){id}}' % (
            id_arg, name_arg, picture_arg, index_arg, muted_arg))["environment"]

        def wrapper(id):
            return Environment(self.client, id)

        return wrapById(res, wrapper)

    def device(self, id, deviceType=None, name=None, index=None, signalStatus=None, batteryStatus=None, batteryCharging=None, firmware=None, muted=None, starred=None):
        id_arg = 'id:"%s",' % id
        deviceType_arg = 'deviceType:"%s",' % deviceType if deviceType is not None else ''
        name_arg = 'name:"%s",' % name if name is not None else ''
        index_arg = 'index:%s,' % index if index is not None else ''
        signalStatus_arg = 'signalStatus:%s,' % signalStatus if signalStatus is not None else ''
        batteryStatus_arg = 'batteryStatus:%s,' % batteryStatus if batteryStatus is not None else ''
        batteryCharging_arg = 'batteryCharging:%s,' % batteryCharging if batteryCharging is not None else ''
        firmware_arg = 'firmware:"%s",' % firmware if firmware is not None else ''
        muted_arg = 'muted:%s,' % muted if muted is not None else ''
        starred_arg = 'starred:%s,' % starred if starred is not None else ''
        res = self.client.mutation('mutation{device(%s%s%s%s%s%s%s%s%s%s){id}}' % (
            id_arg, deviceType_arg, name_arg, index_arg, signalStatus_arg, batteryStatus_arg, batteryCharging_arg, firmware_arg, muted_arg, starred_arg))["device"]

        def wrapper(id):
            return Device(self.client, id)

        return wrapById(res, wrapper)

    def value(self, id, private=None, hidden=None, cardSize=None, name=None, index=None):
        id_arg = 'id:"%s",' % id
        private_arg = 'private:%s,' % private if private is not None else ''
        hidden_arg = 'hidden:%s,' % hidden if hidden is not None else ''
        cardSize_arg = 'cardSize:%s,' % cardSize if cardSize is not None else ''
        name_arg = 'name:"%s",' % name if name is not None else ''
        index_arg = 'index:%s,' % index if index is not None else ''
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
        deviceId_arg = 'deviceId:"%s",' % deviceId
        newEnvironmentId_arg = 'newEnvironmentId:"%s",' % newEnvironmentId

        res = self.client.mutation('mutation{moveDevice(%s%s){id}}' % (
            deviceId_arg, newEnvironmentId_arg))["moveDevice"]

        def wrapper(id):
            return Device(self.client, id)

        return wrapById(res, wrapper)

    def resetOnlineState(self, deviceId):
        deviceId_arg = 'deviceId:"%s",' % deviceId

        res = self.client.mutation('mutation{resetOnlineState(%s){id}}' % (deviceId_arg))[
            "resetOnlineState"]

        def wrapper(id):
            return Device(self.client, id)

        return wrapById(res, wrapper)

    def floatValue(self, id, permission=None, private=None, hidden=None, unitOfMeasurement=None, value=None, precision=None, min=None, max=None, name=None, cardSize=None, index=None):
        id_arg = 'id:"%s",' % id
        permission_arg = 'permission:%s,' % permission if permission is not None else ''
        private_arg = 'private:%s,' % private if private is not None else ''
        hidden_arg = 'hidden:%s,' % hidden if hidden is not None else ''
        unitOfMeasurement_arg = 'unitOfMeasurement:"%s",' % unitOfMeasurement if unitOfMeasurement is not None else ''
        value_arg = 'value:%s,' % value if value is not None else ''
        precision_arg = 'precision:%s,' % precision if precision is not None else ''
        min_arg = 'min:%s,' % min if min is not None else ''
        max_arg = 'max:%s,' % max if max is not None else ''
        name_arg = 'name:"%s",' % name if name is not None else ''
        cardSize_arg = 'cardSize:%s,' % cardSize if cardSize is not None else ''
        index_arg = 'index:%s,' % index if index is not None else ''
        res = self.client.mutation('mutation{floatValue(%s%s%s%s%s%s%s%s%s%s%s%s){id}}' % (
            id_arg, permission_arg, private_arg, hidden_arg, unitOfMeasurement_arg, value_arg, precision_arg, min_arg, max_arg, name_arg, cardSize_arg, index_arg))["floatValue"]

        def wrapper(id):
            return FloatValue(self.client, id)

        return wrapById(res, wrapper)

    def atomicUpdateFloat(self, id, incrementBy):
        id_arg = 'id:"%s",' % id
        incrementBy_arg = 'incrementBy:%s,' % incrementBy

        res = self.client.mutation('mutation{atomicUpdateFloat(%s%s){id}}' % (
            id_arg, incrementBy_arg))["atomicUpdateFloat"]

        def wrapper(id):
            return FloatValue(self.client, id)

        return wrapById(res, wrapper)

    def stringValue(self, id, permission=None, private=None, hidden=None, value=None, maxChars=None, name=None, cardSize=None, allowedValues=None, index=None):
        id_arg = 'id:"%s",' % id
        permission_arg = 'permission:%s,' % permission if permission is not None else ''
        private_arg = 'private:%s,' % private if private is not None else ''
        hidden_arg = 'hidden:%s,' % hidden if hidden is not None else ''
        value_arg = 'value:"%s",' % value if value is not None else ''
        maxChars_arg = 'maxChars:%s,' % maxChars if maxChars is not None else ''
        name_arg = 'name:"%s",' % name if name is not None else ''
        cardSize_arg = 'cardSize:%s,' % cardSize if cardSize is not None else ''
        allowedValues_arg = 'allowedValues:%s,' % allowedValues if allowedValues is not None else ''
        index_arg = 'index:%s,' % index if index is not None else ''
        res = self.client.mutation('mutation{stringValue(%s%s%s%s%s%s%s%s%s%s){id}}' % (
            id_arg, permission_arg, private_arg, hidden_arg, value_arg, maxChars_arg, name_arg, cardSize_arg, allowedValues_arg, index_arg))["stringValue"]

        def wrapper(id):
            return StringValue(self.client, id)

        return wrapById(res, wrapper)

    def booleanValue(self, id, permission=None, private=None, hidden=None, value=None, name=None, cardSize=None, index=None):
        id_arg = 'id:"%s",' % id
        permission_arg = 'permission:%s,' % permission if permission is not None else ''
        private_arg = 'private:%s,' % private if private is not None else ''
        hidden_arg = 'hidden:%s,' % hidden if hidden is not None else ''
        value_arg = 'value:%s,' % value if value is not None else ''
        name_arg = 'name:"%s",' % name if name is not None else ''
        cardSize_arg = 'cardSize:%s,' % cardSize if cardSize is not None else ''
        index_arg = 'index:%s,' % index if index is not None else ''
        res = self.client.mutation('mutation{booleanValue(%s%s%s%s%s%s%s%s){id}}' % (
            id_arg, permission_arg, private_arg, hidden_arg, value_arg, name_arg, cardSize_arg, index_arg))["booleanValue"]

        def wrapper(id):
            return BooleanValue(self.client, id)

        return wrapById(res, wrapper)

    def floatSeriesValue(self, id, private=None, hidden=None, unitOfMeasurement=None, precision=None, min=None, max=None, name=None, cardSize=None, threshold=None, index=None):
        id_arg = 'id:"%s",' % id
        private_arg = 'private:%s,' % private if private is not None else ''
        hidden_arg = 'hidden:%s,' % hidden if hidden is not None else ''
        unitOfMeasurement_arg = 'unitOfMeasurement:"%s",' % unitOfMeasurement if unitOfMeasurement is not None else ''
        precision_arg = 'precision:%s,' % precision if precision is not None else ''
        min_arg = 'min:%s,' % min if min is not None else ''
        max_arg = 'max:%s,' % max if max is not None else ''
        name_arg = 'name:"%s",' % name if name is not None else ''
        cardSize_arg = 'cardSize:%s,' % cardSize if cardSize is not None else ''
        threshold_arg = 'threshold:%s,' % threshold if threshold is not None else ''
        index_arg = 'index:%s,' % index if index is not None else ''
        res = self.client.mutation('mutation{floatSeriesValue(%s%s%s%s%s%s%s%s%s%s%s){id}}' % (
            id_arg, private_arg, hidden_arg, unitOfMeasurement_arg, precision_arg, min_arg, max_arg, name_arg, cardSize_arg, threshold_arg, index_arg))["floatSeriesValue"]

        def wrapper(id):
            return FloatSeriesValue(self.client, id)

        return wrapById(res, wrapper)

    def floatSeriesNode(self, id, value=None, timestamp=None):
        id_arg = 'id:"%s",' % id
        value_arg = 'value:%s,' % value if value is not None else ''
        timestamp_arg = 'timestamp:"%s",' % timestamp if timestamp is not None else ''
        res = self.client.mutation('mutation{floatSeriesNode(%s%s%s){id}}' % (
            id_arg, value_arg, timestamp_arg))["floatSeriesNode"]

        def wrapper(id):
            return FloatSeriesNode(self.client, id)

        return wrapById(res, wrapper)

    def categorySeriesValue(self, id, private=None, hidden=None, name=None, cardSize=None, allowedValues=None, index=None):
        id_arg = 'id:"%s",' % id
        private_arg = 'private:%s,' % private if private is not None else ''
        hidden_arg = 'hidden:%s,' % hidden if hidden is not None else ''
        name_arg = 'name:"%s",' % name if name is not None else ''
        cardSize_arg = 'cardSize:%s,' % cardSize if cardSize is not None else ''
        allowedValues_arg = 'allowedValues:%s,' % allowedValues if allowedValues is not None else ''
        index_arg = 'index:%s,' % index if index is not None else ''
        res = self.client.mutation('mutation{categorySeriesValue(%s%s%s%s%s%s%s){id}}' % (
            id_arg, private_arg, hidden_arg, name_arg, cardSize_arg, allowedValues_arg, index_arg))["categorySeriesValue"]

        def wrapper(id):
            return CategorySeriesValue(self.client, id)

        return wrapById(res, wrapper)

    def categorySeriesNode(self, id, value=None, timestamp=None):
        id_arg = 'id:"%s",' % id
        value_arg = 'value:"%s",' % value if value is not None else ''
        timestamp_arg = 'timestamp:"%s",' % timestamp if timestamp is not None else ''
        res = self.client.mutation('mutation{categorySeriesNode(%s%s%s){id}}' % (
            id_arg, value_arg, timestamp_arg))["categorySeriesNode"]

        def wrapper(id):
            return CategorySeriesNode(self.client, id)

        return wrapById(res, wrapper)

    def notification(self, id, content=None, read=None):
        id_arg = 'id:"%s",' % id
        content_arg = 'content:"%s",' % content if content is not None else ''
        read_arg = 'read:%s,' % read if read is not None else ''
        res = self.client.mutation('mutation{notification(%s%s%s){id}}' % (
            id_arg, content_arg, read_arg))["notification"]

        def wrapper(id):
            return Notification(self.client, id)

        return wrapById(res, wrapper)

    def deleteNotification(self, id):
        id_arg = 'id:"%s",' % id

        return self.client.mutation('mutation{deleteNotification(%s)}' % (id_arg))["deleteNotification"]

    def deleteValue(self, id):
        id_arg = 'id:"%s",' % id

        return self.client.mutation('mutation{deleteValue(%s)}' % (id_arg))["deleteValue"]

    def deleteDevice(self, id):
        id_arg = 'id:"%s",' % id

        return self.client.mutation('mutation{deleteDevice(%s)}' % (id_arg))["deleteDevice"]

    def unclaimDevice(self, id):
        id_arg = 'id:"%s",' % id

        return self.client.mutation('mutation{unclaimDevice(%s){id}}' % (id_arg))["unclaimDevice"]

    def deleteEnvironment(self, id):
        id_arg = 'id:"%s",' % id

        return self.client.mutation('mutation{deleteEnvironment(%s)}' % (id_arg))["deleteEnvironment"]

    def deleteUser(self, ):

        return self.client.mutation('mutation{deleteUser()}' % ())["deleteUser"]

    def deleteFloatSeriesNode(self, id):
        id_arg = 'id:"%s",' % id

        return self.client.mutation('mutation{deleteFloatSeriesNode(%s)}' % (id_arg))["deleteFloatSeriesNode"]

    def deleteCategorySeriesNode(self, id):
        id_arg = 'id:"%s",' % id

        return self.client.mutation('mutation{deleteCategorySeriesNode(%s)}' % (id_arg))["deleteCategorySeriesNode"]
