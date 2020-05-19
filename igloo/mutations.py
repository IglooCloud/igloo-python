from igloo.models.user import User
from igloo.models.access_token import AccessToken
from igloo.models.pending_share import PendingShare
from igloo.models.environment import Environment
from igloo.models.thing import Thing
from igloo.models.variable import Variable
from igloo.models.float_variable import FloatVariable
from igloo.models.pending_transfer import PendingTransfer
from igloo.models.notification import Notification
from igloo.models.boolean_variable import BooleanVariable
from igloo.models.string_variable import StringVariable
from igloo.models.float_series_variable import FloatSeriesVariable
from igloo.models.category_series_variable import CategorySeriesVariable
from igloo.models.category_series_node import CategorySeriesNode
from igloo.models.file_variable import FileVariable
from igloo.models.float_series_node import FloatSeriesNode
from igloo.utils import parse_arg, undefined


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

    def log_in(self, email, password, totp=undefined, private_cloud=undefined):
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

    def sign_up(self, email, name, password, accept_privacy_policy_and_EULA, company_name=undefined, private_cloud=undefined):
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

    def share_environment(self, environment_id, role, email=undefined, user_id=undefined):
        environmentId_arg = parse_arg("environmentId", environment_id)
        role_arg = parse_arg("role", role, is_enum=True)
        email_arg = parse_arg("email", email)
        userId_arg = parse_arg("userId", user_id)
        res = self.client.mutation('mutation{shareEnvironment(%s%s%s%s){id}}' % (
            environmentId_arg, email_arg, userId_arg, role_arg))["shareEnvironment"]

        def wrapper(id):
            return PendingShare(self.client, id)

        return wrapById(res, wrapper)

    def pending_share(self, id, role):
        id_arg = parse_arg("id", id)
        role_arg = parse_arg("role", role, is_enum=True)

        res = self.client.mutation('mutation{pendingShare(%s%s){id}}' % (
            id_arg, role_arg))["pendingShare"]

        def wrapper(id):
            return PendingShare(self.client, id)

        return wrapById(res, wrapper)

    def revoke_pending_share(self, pending_share_id):
        pendingShareId_arg = parse_arg(
            "pendingShareId", pending_share_id)

        return self.client.mutation('mutation{revokePendingShare(%s)}' % (pendingShareId_arg))["revokePendingShare"]

    def accept_pending_share(self, pending_share_id):
        pendingShareId_arg = parse_arg(
            "pendingShareId", pending_share_id)

        res = self.client.mutation('mutation{acceptPendingShare(%s){sender{id} receiver{id} role environment{id}}}' % (
            pendingShareId_arg))["acceptPendingShare"]

        def wrapper(res):
            res["sender"] = User(self.client, res["sender"]["id"])
            res["receiver"] = User(self.client, res["receiver"]["id"])
            res["environment"] = Environment(
                self.client, res["environment"]["id"])

            return res

        return wrapWith(res, wrapper)

    def decline_pending_share(self, pending_share_id):
        pendingShareId_arg = parse_arg(
            "pendingShareId", pending_share_id)

        return self.client.mutation('mutation{declinePendingShare(%s)}' % (pendingShareId_arg))["declinePendingShare"]

    def stop_sharing_environment(self, environment_id, email=undefined, user_id=undefined):
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

    def transfer_environment(self, environment_id, email=undefined, user_id=undefined):
        environmentId_arg = parse_arg("environmentId", environment_id)
        email_arg = parse_arg("email", email)
        userId_arg = parse_arg("userId", user_id)
        res = self.client.mutation('mutation{transferEnvironment(%s%s%s){id}}' % (
            environmentId_arg, email_arg, userId_arg))["transferEnvironment"]

        def wrapper(id):
            return PendingTransfer(self.client, id)

        return wrapById(res, wrapper)

    def revoke_pending_transfer(self, pending_transfer_id):
        pending_transfer_id_arg = parse_arg(
            "pendingTransferId", pending_transfer_id)

        return self.client.mutation('mutation{revokePendingTransfer(%s)}' % (pending_transfer_id_arg))["revokePendingTransfer"]

    def accept_pending_transfer(self, pending_transfer_id):
        pending_transfer_id_arg = parse_arg(
            "pendingTransferId", pending_transfer_id)

        res = self.client.mutation('mutation{acceptPendingTransfer(%s){id sender{id} receiver{id} environment{id}}}' % (
            pending_transfer_id_arg))["acceptPendingTransfer"]

        def wrapper(res):
            res["sender"] = User(self.client, res["sender"]["id"])
            res["receiver"] = User(self.client, res["receiver"]["id"])
            res["environment"] = Environment(
                self.client, res["environment"]["id"])

            return res

        return wrapWith(res, wrapper)

    def decline_pending_transfer(self, pending_transfer_id):
        pending_transfer_id_arg = parse_arg(
            "pendingTransferId", pending_transfer_id)

        return self.client.mutation('mutation{declinePendingTransfer(%s)}' % (pending_transfer_id_arg))["declinePendingTransfer"]

    def change_role(self, environment_id, email, new_role):
        environmentId_arg = parse_arg("environmentId", environment_id)
        email_arg = parse_arg("email", email)
        newRole_arg = parse_arg("newRole", new_role)

        res = self.client.mutation('mutation{changeRole(%s%s%s){id}}' % (
            environmentId_arg, email_arg, newRole_arg))["changeRole"]

        def wrapper(id):
            return Environment(self.client, id)

        return wrapById(res, wrapper)

    def create_environment(self, name, picture=undefined, index=undefined, muted=undefined):
        name_arg = parse_arg("name", name)
        picture_arg = parse_arg("picture", picture, is_enum=True)
        index_arg = parse_arg("index", index)
        muted_arg = parse_arg("muted", muted)
        res = self.client.mutation('mutation{createEnvironment(%s%s%s%s){id}}' % (
            name_arg, picture_arg, index_arg, muted_arg))["createEnvironment"]

        def wrapper(id):
            return Environment(self.client, id)

        return wrapById(res, wrapper)

    def create_thing(self, type, firmware=undefined, battery_threshold=undefined, stored_notifications=undefined):
        type_arg = parse_arg("type", type)
        firmware_arg = parse_arg("firmware", firmware)
        battery_threshold_arg = parse_arg(
            "batteryThreshold", battery_threshold)
        stored_notifications_arg = parse_arg(
            "storedNotifications", stored_notifications)
        res = self.client.mutation('mutation{createThing(%s%s%s%s){id}}' % (
            type_arg, firmware_arg, battery_threshold_arg, stored_notifications_arg))["createThing"]

        # FIXME: if we choose to keep the createThingPayload implement it here
        def wrapper(id):
            return Thing(self.client, id)

        return wrapById(res, wrapper)

    def claim_thing(self, claim_code, name, environment_id, index=undefined, muted=undefined):
        claimCode_arg = parse_arg("claimCode", claim_code)
        name_arg = parse_arg("name", name)
        environmentId_arg = parse_arg("environmentId", environment_id)
        index_arg = parse_arg("index", index)
        muted_arg = parse_arg("muted", muted)
        res = self.client.mutation('mutation{claimThing(%s%s%s%s%s){id}}' % (
            claimCode_arg, name_arg, index_arg, environmentId_arg, muted_arg))["claimThing"]

        def wrapper(id):
            return Thing(self.client, id)

        return wrapById(res, wrapper)

    def create_notification(self, thing_id, content, date=undefined):
        thingId_arg = parse_arg("thingId", thing_id)
        content_arg = parse_arg("content", content)
        date_arg = parse_arg("date", date)
        res = self.client.mutation('mutation{createNotification(%s%s%s){id}}' % (
            thingId_arg, content_arg, date_arg))["createNotification"]

        def wrapper(id):
            return Notification(self.client, id)

        return wrapById(res, wrapper)

    def create_float_variable(self, permission, name, thing_id=undefined, developer_only=undefined, allowed_values=undefined, unit_of_measurement=undefined, value=undefined, precision=undefined, min=undefined, max=undefined, index=undefined):
        thingId_arg = parse_arg("thingId", thing_id)
        permission_arg = parse_arg("permission", permission, is_enum=True)
        name_arg = parse_arg("name", name)
        developer_only_arg = parse_arg("developerOnly", developer_only)
        allowed_values_arg = parse_arg("hidden", allowed_values)
        unitOfMeasurement_arg = parse_arg(
            "unitOfMeasurement", unit_of_measurement)
        value_arg = parse_arg("value", value)
        precision_arg = parse_arg("precision", precision)
        min_arg = parse_arg("min", min)
        max_arg = parse_arg("max", max)

        index_arg = parse_arg("index", index)
        res = self.client.mutation('mutation{createFloatVariable(%s%s%s%s%s%s%s%s%s%s%s){id}}' % (thingId_arg, permission_arg, allowed_values_arg, developer_only_arg,
                                                                                                  unitOfMeasurement_arg, value_arg, precision_arg, min_arg, max_arg, name_arg, index_arg))["createFloatVariable"]

        def wrapper(id):
            return FloatVariable(self.client, id)

        return wrapById(res, wrapper)

    def create_string_variable(self, permission, name, thing_id=undefined, developer_only=undefined, value=undefined, max_characters=undefined, allowed_values=undefined, index=undefined):
        thingId_arg = parse_arg("thingId", thing_id)
        permission_arg = parse_arg("permission", permission, is_enum=True)
        name_arg = parse_arg("name", name)
        developer_only_arg = parse_arg("developerOnly", developer_only)
        value_arg = parse_arg("value", value)
        maxChars_arg = parse_arg("maxChars", max_characters)

        allowedValues_arg = parse_arg("allowedValues", allowed_values)
        index_arg = parse_arg("index", index)
        res = self.client.mutation('mutation{createStringVariable(%s%s%s%s%s%s%s%s){id}}' % (
            thingId_arg, permission_arg, developer_only_arg, value_arg, maxChars_arg, name_arg, allowedValues_arg, index_arg))["createStringVariable"]

        def wrapper(id):
            return StringVariable(self.client, id)

        return wrapById(res, wrapper)

    def create_boolean_variable(self, permission, name, thingId=undefined, developer_only=undefined,  value=undefined, index=undefined):
        thingId_arg = parse_arg("thingId", thingId)
        permission_arg = parse_arg("permission", permission, is_enum=True)
        name_arg = parse_arg("name", name)
        developer_only_arg = parse_arg("developerOnly", developer_only)
        value_arg = parse_arg("value", value)

        index_arg = parse_arg("index", index)
        res = self.client.mutation('mutation{createBooleanVariable(%s%s%s%s%s%s){id}}' % (
            thingId_arg, permission_arg, developer_only_arg, value_arg, name_arg, index_arg))["createBooleanVariable"]

        def wrapper(id):
            return BooleanVariable(self.client, id)

        return wrapById(res, wrapper)

    def create_float_series_variable(self, name, shown_nodes, thing_id=undefined, developer_only=undefined, unit_of_measurement=undefined, precision=undefined, min=undefined, max=undefined, index=undefined, stored_nodes=undefined):
        thingId_arg = parse_arg("thingId", thing_id)
        name_arg = parse_arg("name", name)
        developer_only_arg = parse_arg("private", developer_only)
        unitOfMeasurement_arg = parse_arg(
            "unitOfMeasurement", unit_of_measurement)
        precision_arg = parse_arg("precision", precision)
        min_arg = parse_arg("min", min)
        max_arg = parse_arg("max", max)
        shown_nodes_arg = parse_arg("max", shown_nodes)
        stored_nodes_arg = parse_arg("max", stored_nodes)

        index_arg = parse_arg("index", index)
        res = self.client.mutation('mutation{createFloatSeriesVariable(%s%s%s%s%s%s%s%s%s%s){id}}' % (
            shown_nodes_arg, stored_nodes_arg, thingId_arg, developer_only_arg, unitOfMeasurement_arg, precision_arg, min_arg, max_arg, name_arg, index_arg))["createFloatSeriesVariable"]

        def wrapper(id):
            return FloatSeriesVariable(self.client, id)

        return wrapById(res, wrapper)

    def create_float_series_node(self, series_id, value=undefined, timestamp=undefined):
        seriesId_arg = parse_arg("seriesId", series_id)
        value_arg = parse_arg("value", value)
        timestamp_arg = parse_arg("timestamp", timestamp)
        res = self.client.mutation('mutation{createFloatSeriesNode(%s%s%s){id}}' % (
            seriesId_arg, timestamp_arg, value_arg))["createFloatSeriesNode"]

        def wrapper(id):
            return FloatSeriesNode(self.client, id)

        return wrapById(res, wrapper)

    def user(self,
             company_name=undefined,
             quiet_mode=undefined,
             name=undefined,
             language=undefined,
             vat_number=undefined,
             lenght_and_mass=undefined,
             temperature=undefined,
             date_format=undefined,
             time_format=undefined,
             password_change_email=undefined,
             shares_email=undefined,
             access_token_created_email=undefined,
             address_line1=undefined,
             address_line2=undefined,
             address_postal_code=undefined,
             address_city=undefined,
             address_state=undefined,
             address_country_or_territory=undefined
             ):

        company_name_arg = parse_arg("company_name", company_name)
        quiet_mode_arg = parse_arg("quiet_mode", quiet_mode)
        name_arg = parse_arg("name", name)
        language_arg = parse_arg("language", language)
        vat_number_arg = parse_arg("vat_number", vat_number)
        lenght_and_mass_arg = parse_arg(
            "lenght_and_mass", lenght_and_mass)
        temperature_arg = parse_arg("temperature", temperature)
        date_format_arg = parse_arg("date_format", date_format)
        time_format_arg = parse_arg("time_format", time_format)
        password_change_email_arg = parse_arg(
            "password_change_email", password_change_email)
        shares_email_arg = parse_arg("shares_email", shares_email)
        access_token_created_email_arg = parse_arg(
            "access_token_created_email", access_token_created_email)
        address_line1_arg = parse_arg("address_line1", address_line1)
        address_line2_arg = parse_arg("address_line2", address_line2)
        address_postal_code_arg = parse_arg(
            "address_postal_code", address_postal_code)
        address_city_arg = parse_arg("address_city", address_city)
        address_state_arg = parse_arg("address_state", address_state)
        address_country_or_territory_arg = parse_arg(
            "address_country_or_territory", address_country_or_territory)

        res = self.client.mutation('mutation{user(%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s){id}}' % (
            company_name_arg, quiet_mode_arg, name_arg, language_arg, vat_number_arg, lenght_and_mass_arg, temperature_arg, date_format_arg, time_format_arg, password_change_email_arg, shares_email_arg, access_token_created_email_arg, address_line1_arg, address_line2_arg, address_postal_code_arg, address_city_arg, address_state_arg, address_country_or_territory_arg
        ))["user"]

        def wrapper(id):
            return User(self.client)

        return wrapById(res, wrapper)

    def change_email(self, newEmail, password, redirect_to):
        newEmail_arg = parse_arg("newEmail", newEmail)
        password_arg = parse_arg("password", password)
        redirect_to_arg = parse_arg("redirectTo", redirect_to)

        return self.client.mutation('mutation{changeEmail(%s%s%s)}' % (newEmail_arg, password_arg, redirect_to_arg))["changeEmail"]

    def environment(self, id, name=undefined, picture=undefined, index=undefined, muted=undefined):
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

    def thing(self, id, type=undefined, name=undefined, index=undefined, signal_status=undefined, battery_status=undefined, battery_charging=undefined, battery_threshold=undefined, firmware=undefined, muted=undefined, starred=undefined, stored_notifications=undefined):
        id_arg = parse_arg("id", id)
        thingType_arg = parse_arg("type", type)
        name_arg = parse_arg("name", name)
        index_arg = parse_arg("index", index)
        signalStatus_arg = parse_arg("signalStatus", signal_status)
        batteryStatus_arg = parse_arg("batteryStatus", battery_status)
        batteryCharging_arg = parse_arg("batteryCharging", battery_charging)
        firmware_arg = parse_arg("firmware", firmware)
        muted_arg = parse_arg("muted", muted)
        starred_arg = parse_arg("starred", starred)
        battery_threshold_arg = parse_arg(
            "batteryThreshold", battery_threshold)
        stored_notifications_arg = parse_arg(
            "storedNotifications", stored_notifications)
        res = self.client.mutation('mutation{thing(%s%s%s%s%s%s%s%s%s%s%s%s){id}}' % (
            battery_threshold_arg, stored_notifications_arg, id_arg, thingType_arg, name_arg, index_arg, signalStatus_arg, batteryStatus_arg, batteryCharging_arg, firmware_arg, muted_arg, starred_arg))["thing"]

        def wrapper(id):
            return Thing(self.client, id)

        return wrapById(res, wrapper)

    def move_thing(self, thing_id, new_environment_id):
        thing_id_arg = parse_arg("thingId", thing_id)
        new_environment_id_arg = parse_arg(
            "newEnvironmentId", new_environment_id)

        res = self.client.mutation('mutation{moveThing(%s%s){id}}' % (
            thing_id_arg, new_environment_id_arg))["moveThing"]

        def wrapper(id):
            return Thing(self.client, id)

        return wrapById(res, wrapper)

    def value(self, id, developer_only=undefined, hidden=undefined, name=undefined, index=undefined):
        id_arg = parse_arg("id", id)
        developer_only_arg = parse_arg("developerOnly", developer_only)
        hidden_arg = parse_arg("hidden", hidden)

        name_arg = parse_arg("name", name)
        index_arg = parse_arg("index", index)
        res = self.client.mutation('mutation{value(%s%s%s%s%s){id __typename}}' % (
            id_arg, developer_only_arg, hidden_arg, name_arg, index_arg))["value"]

        def wrapper(res):
            return Value(self.client, res["id"], res["__typename"])

        return wrapWith(res, wrapper)

    def reset_online_state(self, thing_id):
        thingId_arg = parse_arg("thingId", thing_id)

        res = self.client.mutation('mutation{resetOnlineState(%s){id}}' % (thingId_arg))[
            "resetOnlineState"]

        def wrapper(id):
            return Thing(self.client, id)

        return wrapById(res, wrapper)

    def float_variable(self, id, permission=undefined, developer_only=undefined, hidden=undefined, unit_of_measurement=undefined, value=undefined, precision=undefined, min=undefined, max=undefined, name=undefined, index=undefined, allowed_values=undefined):
        id_arg = parse_arg("id", id)
        permission_arg = parse_arg("permission", permission, is_enum=True)
        developer_only_arg = parse_arg("developerOnly", developer_only)
        hidden_arg = parse_arg("hidden", hidden)
        unit_of_measurement_arg = parse_arg(
            "unitOfMeasurement", unit_of_measurement)
        value_arg = parse_arg("value", value)
        precision_arg = parse_arg("precision", precision)
        min_arg = parse_arg("min", min)
        max_arg = parse_arg("max", max)
        name_arg = parse_arg("name", name)
        allowed_values_arg = parse_arg("allowedValues", allowed_values)

        index_arg = parse_arg("index", index)
        res = self.client.mutation('mutation{floatVariable(%s%s%s%s%s%s%s%s%s%s%s%s){id}}' % (
            id_arg, permission_arg, developer_only_arg, allowed_values_arg, hidden_arg, unit_of_measurement_arg, value_arg, precision_arg, min_arg, max_arg, name_arg, index_arg))["floatVariable"]

        def wrapper(id):
            return FloatVariable(self.client, id)

        return wrapById(res, wrapper)

    def increment_float_variable(self, id, increment_by):
        id_arg = parse_arg("id", id)
        incrementBy_arg = parse_arg("incrementBy", increment_by)

        res = self.client.mutation('mutation{incrementFloatVariable(%s%s){id}}' % (
            id_arg, incrementBy_arg))["incrementFloatVariable"]

        def wrapper(id):
            return FloatVariable(self.client, id)

        return wrapById(res, wrapper)

    def string_variable(self, id, permission=undefined, developer_only=undefined, hidden=undefined, value=undefined, max_characters=undefined, name=undefined, allowed_values=undefined, index=undefined):
        id_arg = parse_arg("id", id)
        permission_arg = parse_arg("permission", permission, is_enum=True)
        private_arg = parse_arg("developerOnly", developer_only)
        hidden_arg = parse_arg("hidden", hidden)
        value_arg = parse_arg("value", value)
        maxChars_arg = parse_arg("maxCharacters", max_characters)
        name_arg = parse_arg("name", name)

        allowedValues_arg = parse_arg("allowedValues", allowed_values)
        index_arg = parse_arg("index", index)
        res = self.client.mutation('mutation{stringVariable(%s%s%s%s%s%s%s%s%s){id}}' % (
            id_arg, permission_arg, private_arg, hidden_arg, value_arg, maxChars_arg, name_arg, allowedValues_arg, index_arg))["stringVariable"]

        def wrapper(id):
            return StringVariable(self.client, id)

        return wrapById(res, wrapper)

    def boolean_variable(self, id, permission=undefined, developer_only=undefined, hidden=undefined, value=undefined, name=undefined, index=undefined):
        id_arg = parse_arg("id", id)
        permission_arg = parse_arg("permission", permission, is_enum=True)
        private_arg = parse_arg("developerOnly", developer_only)
        hidden_arg = parse_arg("hidden", hidden)
        value_arg = parse_arg("value", value)
        name_arg = parse_arg("name", name)

        index_arg = parse_arg("index", index)
        res = self.client.mutation('mutation{booleanVariable(%s%s%s%s%s%s%s){id}}' % (
            id_arg, permission_arg, private_arg, hidden_arg, value_arg, name_arg, index_arg))["booleanVariable"]

        def wrapper(id):
            return BooleanVariable(self.client, id)

        return wrapById(res, wrapper)

    def float_series_variable(self, id, developer_only=undefined, hidden=undefined, unit_of_measurement=undefined, precision=undefined, min=undefined, max=undefined, name=undefined, index=undefined, shown_nodes=undefined, stored_nodes=undefined):
        id_arg = parse_arg("id", id)
        private_arg = parse_arg("developerOnly", developer_only)
        hidden_arg = parse_arg("hidden", hidden)
        unitOfMeasurement_arg = parse_arg(
            "unitOfMeasurement", unit_of_measurement)
        precision_arg = parse_arg("precision", precision)
        min_arg = parse_arg("min", min)
        max_arg = parse_arg("max", max)
        name_arg = parse_arg("name", name)
        shown_nodes_arg = parse_arg("shownNodes", shown_nodes)
        stored_nodes_arg = parse_arg("storedNodes", stored_nodes)

        index_arg = parse_arg("index", index)
        res = self.client.mutation('mutation{floatSeriesVariable(%s%s%s%s%s%s%s%s%s%s%s){id}}' % (
            id_arg, private_arg, shown_nodes_arg, stored_nodes_arg, hidden_arg, unitOfMeasurement_arg, precision_arg, min_arg, max_arg, name_arg, index_arg))["floatSeriesVariable"]

        def wrapper(id):
            return FloatSeriesVariable(self.client, id)

        return wrapById(res, wrapper)

    def float_series_node(self, id, value=undefined, timestamp=undefined):
        id_arg = parse_arg("id", id)
        value_arg = parse_arg("value", value)
        timestamp_arg = parse_arg("timestamp", timestamp)
        res = self.client.mutation('mutation{floatSeriesNode(%s%s%s){id}}' % (
            id_arg, value_arg, timestamp_arg))["floatSeriesNode"]

        def wrapper(id):
            return FloatSeriesNode(self.client, id)

        return wrapById(res, wrapper)

    def category_series_variable(self, id, developer_only=undefined, hidden=undefined, name=undefined, allowed_values=undefined, index=undefined, shown_nodes=undefined, stored_nodes=undefined):
        id_arg = parse_arg("id", id)
        developer_only_arg = parse_arg("developerOnly", developer_only)
        hidden_arg = parse_arg("hidden", hidden)
        name_arg = parse_arg("name", name)
        shown_nodes_arg = parse_arg("shownNodes", shown_nodes)
        stored_nodes_arg = parse_arg("storedNodes", stored_nodes)

        allowedValues_arg = parse_arg("allowedValues", allowed_values)
        index_arg = parse_arg("index", index)
        res = self.client.mutation('mutation{categorySeriesVariable(%s%s%s%s%s%s%s%s){id}}' % (
            id_arg, developer_only_arg, shown_nodes_arg, stored_nodes_arg, hidden_arg, name_arg, allowedValues_arg, index_arg))["categorySeriesVariable"]

        def wrapper(id):
            return CategorySeriesVariable(self.client, id)

        return wrapById(res, wrapper)

    def category_series_node(self, id, value=undefined, timestamp=undefined):
        id_arg = parse_arg("id", id)
        value_arg = parse_arg("value", value)
        timestamp_arg = parse_arg("timestamp", timestamp)
        res = self.client.mutation('mutation{categorySeriesNode(%s%s%s){id}}' % (
            id_arg, value_arg, timestamp_arg))["categorySeriesNode"]

        def wrapper(id):
            return CategorySeriesNode(self.client, id)

        return wrapById(res, wrapper)

    def notification(self, id, content=undefined, read=undefined):
        id_arg = parse_arg("id", id)
        content_arg = parse_arg("content", content)
        read_arg = parse_arg("read", read)
        res = self.client.mutation('mutation{notification(%s%s%s){id}}' % (
            id_arg, content_arg, read_arg))["notification"]

        def wrapper(id):
            return Notification(self.client, id)

        return wrapById(res, wrapper)

    def delete_notification(self, id):
        id_arg = parse_arg("id", id)

        return self.client.mutation('mutation{deleteNotification(%s)}' % (id_arg))["deleteNotification"]

    def delete_variable(self, id):
        id_arg = parse_arg("id", id)

        return self.client.mutation('mutation{deleteVariable(%s)}' % (id_arg))["deleteVariable"]

    def delete_thing(self, id):
        id_arg = parse_arg("id", id)

        return self.client.mutation('mutation{deleteThing(%s)}' % (id_arg))["deleteThing"]

    def unclaimThing(self, id, reset):
        id_arg = parse_arg("id", id)
        reset_arg = parse_arg("reset", reset)

        return self.client.mutation('mutation{unclaimThing(%s%s){id}}' % (id_arg, reset_arg))["unclaimThing"]

    def delete_environment(self, id):
        id_arg = parse_arg("id", id)

        return self.client.mutation('mutation{deleteEnvironment(%s)}' % (id_arg))["deleteEnvironment"]

    def delete_user(self, ):

        return self.client.mutation('mutation{deleteUser()}' % ())["deleteUser"]

    def delete_float_series_node(self, id):
        id_arg = parse_arg("id", id)

        return self.client.mutation('mutation{deleteFloatSeriesNode(%s)}' % (id_arg))["deleteFloatSeriesNode"]

    def delete_category_series_node(self, id):
        id_arg = parse_arg("id", id)

        return self.client.mutation('mutation{deleteCategorySeriesNode(%s)}' % (id_arg))["deleteCategorySeriesNode"]
