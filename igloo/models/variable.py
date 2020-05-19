from .float_variable import FloatVariable
from .file_variable import FileVariable
from .boolean_variable import BooleanVariable
from .string_variable import StringVariable
from .float_series_variable import FloatSeriesVariable
from .category_series_variable import CategorySeriesVariable
from igloo.utils import get_representation


def Variable(client, id, resolveType):
    if resolveType == "FloatVariable":
        return FloatVariable(client, id)
    elif resolveType == "FileVariable":
        return FileVariable(client, id)
    elif resolveType == "BooleanVariable":
        return BooleanVariable(client, id)
    elif resolveType == "StringVariable":
        return StringVariable(client, id)
    elif resolveType == "FloatSeriesVariable":
        return FloatSeriesVariable(client, id)
    elif resolveType == "CategorySeriesVariable":
        return CategorySeriesVariable(client, id)


class ThingVariablesList:
    def __init__(self, client, thingId):
        self.client = client
        self.thingId = thingId
        self.current = 0
        self._filter = "{}"

    def filter(self, _filter):
        self._filter = get_representation(_filter)
        return self

    def __len__(self):
        res = self.client.query(
            '{thing(id:"%s"){valueCount(filter:%s)}}' % (self.thingId, self._filter))
        return res["thing"]["valueCount"]

    def __getitem__(self, i):
        if isinstance(i, int):
            res = self.client.query(
                '{thing(id:"%s"){values(limit:1, offset:%d, filter:%s){id __typename}}}' % (self.thingId, i, self._filter))
            if len(res["thing"]["values"]) != 1:
                raise IndexError()
            return Value(self.client, res["thing"]["values"][0]["id"], res["thing"]["values"][0]["__typename"])
        elif isinstance(i, slice):
            start, end, _ = i.indices(len(self))
            res = self.client.query(
                '{thing(id:"%s"){values(offset:%d, limit:%d, filter:%s){id __typename}}}' % (self.thingId, start, end-start, self._filter))
            return [Value(self.client, value["id"], value["__typename"]) for value in res["thing"]["values"]]
        else:
            raise TypeError("Unexpected type {} passed as index".format(i))

    def __iter__(self):
        return self

    def __next__(self):
        res = self.client.query(
            '{thing(id:"%s"){values(limit:1, offset:%d, filter:%s){id __typename}}}' % (self.thingId, self.current, self._filter))

        if len(res["thing", "values"]) != 1:
            raise StopIteration

        self.current += 1
        return Value(self.client, res["thing"]["values"][0]["id"], res["thing"]["values"][0]["__typename"])

    def next(self):
        return self.__next__()
