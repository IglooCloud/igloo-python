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
    def __init__(self, client, id=None):
        self.client = client

        if id is None:
            self._id = self.client.query(
                '{user{id}}', keys=["user", "id"], asyncio=False)
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
            'mutation{user(id:"%s")(name:"%s"){id}}' % (self._id, newName), asyncio=False)

    @property
    def profileIconColor(self):
        if self.client.asyncio:
            return self.loader.load("profileIconColor")
        else:
            return self.client.query('{user(id:"%s"){profileIconColor}}' % self._id,
                                     keys=["user", "profileIconColor"])

    @property
    def quietMode(self):
        if self.client.asyncio:
            return self.loader.load("quietMode")
        else:
            return self.client.query('{user(id:"%s"){quietMode}}' % self._id, keys=[
                "user", "quietMode"])

    @quietMode.setter
    def quietMode(self, newMode):
        self.client.mutation(
            'mutation{user(id:"%s")(quietMode:%s){id}}' % (self._id, "true" if newMode else "false"), asyncio=False)

    @property
    def emailIsVerified(self):
        if self.client.asyncio:
            return self.loader.load("emailIsVerified")
        else:
            return self.client.query('{user(id:"%s"){emailIsVerified}}' % self._id, keys=[
                "user", "emailIsVerified"])

    @property
    def primaryAuthenticationMethods(self):
        if self.client.asyncio:
            return self.loader.load("primaryAuthenticationMethods")
        else:
            return self.client.query('{user(id:"%s"){primaryAuthenticationMethods}}' % self._id, keys=[
                "user", "primaryAuthenticationMethods"])

    @property
    def secondaryAuthenticationMethods(self):
        if self.client.asyncio:
            return self.loader.load("secondaryAuthenticationMethods")
        else:
            return self.client.query('{user(id:"%s"){secondaryAuthenticationMethods}}' % self._id, keys=[
                "user", "secondaryAuthenticationMethods"])

    @property
    def environments(self):
        from .environment import EnvironmentList
        return EnvironmentList(self.client, self.id)

    @property
    def pendingEnvironmentShares(self):
        from .pending_environment_share import UserPendingEnvironmentShareList
        return UserPendingEnvironmentShareList(self.client, self.id)

    @property
    def pendingOwnerChanges(self):
        from .pending_owner_change import UserPendingOwnerChangeList
        return UserPendingOwnerChangeList(self.client, self.id)

    @property
    def developerThings(self):
        from .thing import DeveloperThingList
        return DeveloperThingList(self.client, self.id)

    @property
    def permanentTokens(self):
        from .permanent_token import PermanentTokenList
        return PermanentTokenList(self.client, self.id)


class EnvironmentAdminList:
    def __init__(self, client, environmentId):
        self.client = client
        self.environmentId = environmentId
        self.current = 0

    def __len__(self):
        res = self.client.query(
            '{environment(id:"%s"){adminCount}}' % self.environmentId)
        return res["environment"]["adminCount"]

    def __getitem__(self, i):
        if isinstance(i, int):
            res = self.client.query(
                '{environment(id:"%s"){admins(limit:1, offset:%d){id}}}' % (self.environmentId, i))
            if len(res["environment"]["admins"]) != 1:
                raise IndexError()
            return User(self.client, res["environment"]["admins"][0]["id"])
        elif isinstance(i, slice):
            start, end, _ = i.indices(len(self))
            res = self.client.query(
                '{environment(id:"%s"){admins(offset:%d, limit:%d){id}}}' % (self.environmentId, start, end-start))
            return [User(self.client, user["id"]) for user in res["environment"]["admins"]]
        else:
            raise TypeError("Unexpected type {} passed as index".format(i))

    def __iter__(self):
        return self

    def __next__(self):
        res = self.client.query(
            '{environment(id:"%s"){admins(limit:1, offset:%d){id}}}' % (self.environmentId, self.current))

        if len(res["environment", "admins"]) != 1:
            raise StopIteration

        self.current += 1
        return User(self.client, res["environment"]["admins"][0]["id"])

    def next(self):
        return self.__next__()


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
