from .float_value import FloatValue
from .file_value import FileValue
from .boolean_value import BooleanValue
from .string_value import StringValue
from .float_series_value import FloatSeriesValue
from .category_series_value import CategorySeriesValue
from igloo.utils import get_representation


def Value(client, id, resolveType):
    if resolveType == "FloatValue":
        return FloatValue(client, id)
    elif resolveType == "FileValue":
        return FileValue(client, id)
    elif resolveType == "BooleanValue":
        return BooleanValue(client, id)
    elif resolveType == "StringValue":
        return StringValue(client, id)
    elif resolveType == "FloatSeriesValue":
        return FloatSeriesValue(client, id)
    elif resolveType == "CategorySeriesValue":
        return CategorySeriesValue(client, id)


class ThingValuesList:
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
