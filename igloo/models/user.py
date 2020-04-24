from aiodataloader import DataLoader


class UserLoader(DataLoader):
    def __init__(self, client, id):
        super().__init__()
        self.client = client
        self._id = id

    async def batch_load_fn(self, keys):
        fields = " ".join(set(keys))
        res = await self.client.query('{user(id:"%s"){%s}}' % (self._id, fields), keys=["user"])

        resolvedValues = [res[key] for key in keys]

        return resolvedValues


class User:
    def __init__(self, client, id=None, email=None):
        self.client = client

        if id is None and email is None:
            self._id = self.client.query(
                '{user{id}}', keys=["user", "id"], asyncio=False)
        elif id is None:
            self._id = self.client.query(
                '{user(email:"%s"){id}}' % email, keys=["user", "id"], asyncio=False)
        else:
            self._id = id

        self.loader = UserLoader(client, self._id)

    @property
    def id(self):
        return self._id

    @property
    def email(self):
        if self.client.asyncio:
            return self.loader.load("email")
        else:
            return self.client.query('{user(id:"%s"){email}}' % self._id, keys=["user", "email"])

    @property
    def name(self):
        if self.client.asyncio:
            return self.loader.load("name")
        else:
            return self.client.query('{user(id:"%s"){name}}' % self._id, keys=["user", "name"])

    @name.setter
    def name(self, newName):
        self.client.mutation(
            'mutation{user(id:"%s", name:"%s"){id}}' % (self._id, newName), asyncio=False)

    @property
    def company_name(self):
        if self.client.asyncio:
            return self.loader.load("companyName")
        else:
            return self.client.query('{user(id:"%s"){companyName}}' % self._id, keys=["user", "companyName"])

    @company_name.setter
    def company_name(self, newName):
        self.client.mutation(
            'mutation{user(id:"%s", companyName:"%s"){id}}' % (self._id, newName), asyncio=False)

    @property
    def profile_icon_color(self):
        if self.client.asyncio:
            return self.loader.load("profileIconColor")
        else:
            return self.client.query('{user(id:"%s"){profileIconColor}}' % self._id,
                                     keys=["user", "profileIconColor"])

    @property
    def quiet_mode(self):
        if self.client.asyncio:
            return self.loader.load("quietMode")
        else:
            return self.client.query('{user(id:"%s"){quietMode}}' % self._id, keys=[
                "user", "quietMode"])

    @quiet_mode.setter
    def quiet_mode(self, newMode):
        self.client.mutation(
            'mutation{user(id:"%s",quietMode:%s){id}}' % (self._id, "true" if newMode else "false"), asyncio=False)

    @property
    def address_line1(self):
        if self.client.asyncio:
            return self.loader.load("addressLine1")
        else:
            return self.client.query('{user(id:"%s"){addressLine1}}' % self._id, keys=[
                "user", "addressLine1"])

    @address_line1.setter
    def address_line1(self, newValue):
        self.client.mutation(
            'mutation{user(id:"%s", addressLine1:"%s"){id}}' % (self._id, newValue), asyncio=False)

    @property
    def address_line2(self):
        if self.client.asyncio:
            return self.loader.load("addressLine2")
        else:
            return self.client.query('{user(id:"%s"){addressLine2}}' % self._id, keys=[
                "user", "addressLine2"])

    @address_line2.setter
    def address_line2(self, newValue):
        self.client.mutation(
            'mutation{user(id:"%s", addressLine2:"%s"){id}}' % (self._id, newValue), asyncio=False)

    @property
    def address_postal_code(self):
        if self.client.asyncio:
            return self.loader.load("addressPostalCode")
        else:
            return self.client.query('{user(id:"%s"){addressPostalCode}}' % self._id, keys=[
                "user", "addressPostalCode"])

    @address_postal_code.setter
    def address_postal_code(self, newValue):
        self.client.mutation(
            'mutation{user(id:"%s", addressPostalCode:"%s"){id}}' % (self._id, newValue), asyncio=False)

    @property
    def address_city(self):
        if self.client.asyncio:
            return self.loader.load("addressCity")
        else:
            return self.client.query('{user(id:"%s"){addressCity}}' % self._id, keys=[
                "user", "addressCity"])

    @address_city.setter
    def address_city(self, newValue):
        self.client.mutation(
            'mutation{user(id:"%s", addressCity:"%s"){id}}' % (self._id, newValue), asyncio=False)

    @property
    def address_state(self):
        if self.client.asyncio:
            return self.loader.load("addressState")
        else:
            return self.client.query('{user(id:"%s"){addressState}}' % self._id, keys=[
                "user", "addressState"])

    @address_state.setter
    def address_state(self, newValue):
        self.client.mutation(
            'mutation{user(id:"%s", addressState:"%s"){id}}' % (self._id, newValue), asyncio=False)

    @property
    def address_country_or_territory(self):
        if self.client.asyncio:
            return self.loader.load("addressCountryOrTerritory")
        else:
            return self.client.query('{user(id:"%s"){addressCountryOrTerritory}}' % self._id, keys=[
                "user", "addressCountryOrTerritory"])

    @address_country_or_territory.setter
    def address_country_or_territory(self, newValue):
        self.client.mutation(
            'mutation{user(id:"%s", addressCountryOrTerritory:"%s"){id}}' % (self._id, newValue), asyncio=False)

    @property
    def billing_plan(self):
        if self.client.asyncio:
            return self.loader.load("billingPlan")
        else:
            return self.client.query('{user(id:"%s"){billingPlan}}' % self._id, keys=[
                "user", "billingPlan"])

    @property
    def billing_cycle(self):
        if self.client.asyncio:
            return self.loader.load("billingCycle")
        else:
            return self.client.query('{user(id:"%s"){billingCycle}}' % self._id, keys=[
                "user", "billingCycle"])

    @property
    def billing_status(self):
        if self.client.asyncio:
            return self.loader.load("billingStatus")
        else:
            return self.client.query('{user(id:"%s"){billingStatus}}' % self._id, keys=[
                "user", "billingStatus"])

    @property
    def payment_intent_secret(self):
        if self.client.asyncio:
            return self.loader.load("paymentIntentSecret")
        else:
            return self.client.query('{user(id:"%s"){paymentIntentSecret}}' % self._id, keys=[
                "user", "paymentIntentSecret"])

    @property
    def card_last4_digits(self):
        if self.client.asyncio:
            return self.loader.load("cardLast4Digits")
        else:
            return self.client.query('{user(id:"%s"){cardLast4Digits}}' % self._id, keys=[
                "user", "cardLast4Digits"])

    @property
    def card_expiry_month(self):
        if self.client.asyncio:
            return self.loader.load("cardExpiryMonth")
        else:
            return self.client.query('{user(id:"%s"){cardExpiryMonth}}' % self._id, keys=[
                "user", "cardExpiryMonth"])

    @property
    def card_expiry_year(self):
        if self.client.asyncio:
            return self.loader.load("cardExpiryYear")
        else:
            return self.client.query('{user(id:"%s"){cardExpiryYear}}' % self._id, keys=[
                "user", "cardExpiryYear"])

    @property
    def vat_number(self):
        if self.client.asyncio:
            return self.loader.load("vatNumber")
        else:
            return self.client.query('{user(id:"%s"){vatNumber}}' % self._id, keys=[
                "user", "vatNumber"])

    @vat_number.setter
    def vat_number(self, newValue):
        self.client.mutation(
            'mutation{user(id:"%s", vatNumber:"%s"){id}}' % (self._id, newValue), asyncio=False)

    @property
    def next_billing_date(self):
        if self.client.asyncio:
            return self.loader.load("nextBillingDate")
        else:
            return self.client.query('{user(id:"%s"){nextBillingDate}}' % self._id, keys=[
                "user", "nextBillingDate"])

    @property
    def billing_credit(self):
        if self.client.asyncio:
            return self.loader.load("billingCredit")
        else:
            return self.client.query('{user(id:"%s"){billingCredit}}' % self._id, keys=[
                "user", "billingCredit"])

    @property
    def extra_storage(self):
        if self.client.asyncio:
            return self.loader.load("extraStorage")
        else:
            return self.client.query('{user(id:"%s"){extraStorage}}' % self._id, keys=[
                "user", "extraStorage"])

    @property
    def extra_throughput(self):
        if self.client.asyncio:
            return self.loader.load("extraThroughput")
        else:
            return self.client.query('{user(id:"%s"){extraThroughput}}' % self._id, keys=[
                "user", "extraThroughput"])

    @property
    def max_storage(self):
        if self.client.asyncio:
            return self.loader.load("maxStorage")
        else:
            return self.client.query('{user(id:"%s"){maxStorage}}' % self._id, keys=[
                "user", "maxStorage"])

    @property
    def max_throughput(self):
        if self.client.asyncio:
            return self.loader.load("maxThroughput")
        else:
            return self.client.query('{user(id:"%s"){maxThroughput}}' % self._id, keys=[
                "user", "maxThroughput"])

    @property
    def used_storage(self):
        if self.client.asyncio:
            return self.loader.load("usedStorage")
        else:
            return self.client.query('{user(id:"%s"){usedStorage}}' % self._id, keys=[
                "user", "usedStorage"])

    @property
    def used_throughput(self):
        if self.client.asyncio:
            return self.loader.load("usedThroughput")
        else:
            return self.client.query('{user(id:"%s"){usedThroughput}}' % self._id, keys=[
                "user", "usedThroughput"])

    @property
    def custom_apps(self):
        if self.client.asyncio:
            return self.loader.load("customApps")
        else:
            return self.client.query('{user(id:"%s"){customApps}}' % self._id, keys=[
                "user", "customApps"])

    @property
    def email_is_verified(self):
        if self.client.asyncio:
            return self.loader.load("emailIsVerified")
        else:
            return self.client.query('{user(id:"%s"){emailIsVerified}}' % self._id, keys=[
                "user", "emailIsVerified"])

    @property
    def unique_developer_firmwares(self):
        if self.client.asyncio:
            return self.loader.load("uniqueDeveloperFirmwares")
        else:
            return self.client.query('{user(id:"%s"){uniqueDeveloperFirmwares}}' % self._id, keys=[
                "user", "uniqueDeveloperFirmwares"])

    @property
    def environments(self):
        from .environment import EnvironmentList
        return EnvironmentList(self.client, self.id)

    @property
    def pendingShares(self):
        from .pending_share import UserPendingShareList
        return UserPendingShareList(self.client, self.id)

    @property
    def pendingTransfers(self):
        from .pending_transfer import UserPendingTransferList
        return UserPendingTransferList(self.client, self.id)

    @property
    def developerThings(self):
        from .thing import DeveloperThingList
        return DeveloperThingList(self.client, self.id)

    @property
    def accessTokens(self):
        from .access_token import AccessTokenList
        return AccessTokenList(self.client, self.id)

    @property
    def totp_enabled(self):
        if self.client.asyncio:
            return self.loader.load("totpEnabled")
        else:
            return self.client.query('{user(id:"%s"){totpEnabled}}' % self._id, keys=[
                "user", "totpEnabled"])

    @property
    def length_and_mass(self):
        if self.client.asyncio:
            return self.loader.load("lengthAndMass")
        else:
            return self.client.query('{user(id:"%s"){lengthAndMass}}' % self._id, keys=[
                "user", "lengthAndMass"])

    @length_and_mass.setter
    def length_and_mass(self, newValue):
        self.client.mutation(
            'mutation{user(id:"%s", lengthAndMass:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def temperature(self):
        if self.client.asyncio:
            return self.loader.load("temperature")
        else:
            return self.client.query('{user(id:"%s"){temperature}}' % self._id, keys=[
                "user", "temperature"])

    @temperature.setter
    def temperature(self, newValue):
        self.client.mutation(
            'mutation{user(id:"%s", temperature:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def time_format(self):
        if self.client.asyncio:
            return self.loader.load("timeFormat")
        else:
            return self.client.query('{user(id:"%s"){timeFormat}}' % self._id, keys=[
                "user", "timeFormat"])

    @time_format.setter
    def time_format(self, newValue):
        self.client.mutation(
            'mutation{user(id:"%s", timeFormat:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def date_format(self):
        if self.client.asyncio:
            return self.loader.load("dateFormat")
        else:
            return self.client.query('{user(id:"%s"){dateFormat}}' % self._id, keys=[
                "user", "dateFormat"])

    @date_format.setter
    def date_format(self, newValue):
        self.client.mutation(
            'mutation{user(id:"%s", dateFormat:%s){id}}' % (self._id, newValue), asyncio=False)

    @property
    def language(self):
        if self.client.asyncio:
            return self.loader.load("language")
        else:
            return self.client.query('{user(id:"%s"){language}}' % self._id, keys=[
                "user", "language"])

    @language.setter
    def language(self, newValue):
        self.client.mutation(
            'mutation{user(id:"%s", language:"%s"){id}}' % (self._id, newValue), asyncio=False)

    @property
    def password_change_email(self):
        if self.client.asyncio:
            return self.loader.load("passwordChangeEmail")
        else:
            return self.client.query('{user(id:"%s"){passwordChangeEmail}}' % self._id, keys=[
                "user", "passwordChangeEmail"])

    @password_change_email.setter
    def password_change_email(self, newValue):
        self.client.mutation(
            'mutation{user(id:"%s", passwordChangeEmail:%s){id}}' % (self._id, "true" if newValue == True else "false"), asyncio=False)

    @property
    def shares_email(self):
        if self.client.asyncio:
            return self.loader.load("sharesEmail")
        else:
            return self.client.query('{user(id:"%s"){sharesEmail}}' % self._id, keys=[
                "user", "sharesEmail"])

    @shares_email.setter
    def shares_email(self, newValue):
        self.client.mutation(
            'mutation{user(id:"%s", sharesEmail:%s){id}}' % (self._id, "true" if newValue == True else "false"), asyncio=False)

    @property
    def access_token_created_email(self):
        if self.client.asyncio:
            return self.loader.load("accessTokenCreatedEmail")
        else:
            return self.client.query('{user(id:"%s"){accessTokenCreatedEmail}}' % self._id, keys=[
                "user", "accessTokenCreatedEmail"])

    @access_token_created_email.setter
    def access_token_created_email(self, newValue):
        self.client.mutation(
            'mutation{user(id:"%s", accessTokenCreatedEmail:%s){id}}' % (self._id, "true" if newValue == True else "false"), asyncio=False)

    @property
    def business_pricing(self):
        return self.client.query('{user(id:"%s"){businessPricing{id maxStorage maxThroughput price}}}' % self._id, keys=[
            "user", "businessPricing"])


class EnvironmentEditorList:
    def __init__(self, client, environmentId):
        self.client = client
        self.environmentId = environmentId
        self.current = 0

    def __len__(self):
        res = self.client.query(
            '{environment(id:"%s"){editorCount}}' % self.environmentId)
        return res["environment"]["editorCount"]

    def __getitem__(self, i):
        if isinstance(i, int):
            res = self.client.query(
                '{environment(id:"%s"){editors(limit:1, offset:%d){id}}}' % (self.environmentId, i))
            if len(res["environment"]["editors"]) != 1:
                raise IndexError()
            return User(self.client, res["environment"]["editors"][0]["id"])
        elif isinstance(i, slice):
            start, end, _ = i.indices(len(self))
            res = self.client.query(
                '{environment(id:"%s"){editors(offset:%d, limit:%d){id}}}' % (self.environmentId, start, end-start))
            return [User(self.client, user["id"]) for user in res["environment"]["editors"]]
        else:
            raise TypeError("Unexpected type {} passed as index".format(i))

    def __iter__(self):
        return self

    def __next__(self):
        res = self.client.query(
            '{environment(id:"%s"){editors(limit:1, offset:%d){id}}}' % (self.environmentId, self.current))

        if len(res["environment", "editors"]) != 1:
            raise StopIteration

        self.current += 1
        return User(self.client, res["environment"]["editors"][0]["id"])

    def next(self):
        return self.__next__()


class EnvironmentSpectatorList:
    def __init__(self, client, environmentId):
        self.client = client
        self.environmentId = environmentId
        self.current = 0

    def __len__(self):
        res = self.client.query(
            '{environment(id:"%s"){spectatorCount}}' % self.environmentId)
        return res["environment"]["spectatorCount"]

    def __getitem__(self, i):
        if isinstance(i, int):
            res = self.client.query(
                '{environment(id:"%s"){spectators(limit:1, offset:%d){id}}}' % (self.environmentId, i))
            if len(res["environment"]["spectators"]) != 1:
                raise IndexError()
            return User(self.client, res["environment"]["spectators"][0]["id"])
        elif isinstance(i, slice):
            start, end, _ = i.indices(len(self))
            res = self.client.query(
                '{environment(id:"%s"){spectators(offset:%d, limit:%d){id}}}' % (self.environmentId, start, end-start))
            return [User(self.client, user["id"]) for user in res["environment"]["spectators"]]
        else:
            raise TypeError("Unexpected type {} passed as index".format(i))

    def __iter__(self):
        return self

    def __next__(self):
        res = self.client.query(
            '{environment(id:"%s"){spectators(limit:1, offset:%d){id}}}' % (self.environmentId, self.current))

        if len(res["environment", "spectators"]) != 1:
            raise StopIteration

        self.current += 1
        return User(self.client, res["environment"]["spectators"][0]["id"])

    def next(self):
        return self.__next__()
