import json
import requests

with open("introspection.gql") as f:
    query = f.read()

url = "https://api.igloo.ooo/graphql"
payload = {"query": query}
headers = {
    'content-type': "application/json"
}
response = requests.request(
    "POST", url, data=json.dumps(payload), headers=headers)

parsedRes = json.loads(response.text)
if "errors" in parsedRes.keys():
    raise Exception(parsedRes["errors"][0]["message"])

introspection = parsedRes["data"]["__schema"]


def getTypename(type):
    if type["kind"] != "NON_NULL":
        return type["name"]
    else:
        return getTypename(type["ofType"])


unit = "    "


def indent(string, n):
    return "\n".join([unit*n + str for str in string.split("\n")])


def create_query(subscription):
    arg_names = [arg["name"] for arg in subscription["args"]]
    query_args = ",".join([arg+"_arg" for arg in arg_names])

    if subscription["type"]["kind"] == "OBJECT":
        if subscription["type"]["name"][0] != subscription["type"]["name"].upper()[0]:
            returnValue = "{%s}" % " ".join([field["name"]
                                             for field in subscription["type"]["fields"]])
        else:
            returnValue = "{id}"
    elif subscription["type"]["kind"] == "INTERFACE":
        returnValue = "{id __typename}"
    else:
        returnValue = ""

    query = """subscription{%s(%s)%s}""" % (
        subscription["name"],
        "%s"*len(subscription["args"]),
        returnValue
    )

    return "('{query}' % ({query_args})).replace('()','')".format(query=query, query_args=query_args)


def create_handler(subscription):
    required_args = [arg["name"] for arg in subscription["args"]
                     if arg["type"]["kind"] == "NON_NULL"]
    optional_args = [arg["name"] for arg in subscription["args"]
                     if arg["type"]["kind"] != "NON_NULL"]
    all_args = [*required_args, *[arg+"=None" for arg in optional_args]]

    args_type = {arg["name"]: getTypename(
        arg["type"]) for arg in subscription["args"]}

    def arg_to_string(arg_name):
        arg_type = args_type[arg_name]
        if arg_type == "String" or arg_type == "ID":
            return '{}:"%s",'.format(arg_name)
        else:
            return '{}:%s,'.format(arg_name)

    func_args_list = ", ".join(all_args)
    parsed_required_args = "\n".join(["{name}_arg = '{arg_string}' % {name}".format(
        name=arg, arg_string=arg_to_string(arg)) for arg in required_args])
    parsed_optional_args = "\n".join(["{name}_arg = '{arg_string}' % {name} if {name} is not None else ''".format(
        name=arg, arg_string=arg_to_string(arg)) for arg in optional_args])

    return """
    async def {name}(self, {func_args_list}):
{parsed_required_args}
{parsed_optional_args}

        async for data in self.client.subscribe({query}):
            {yieldVal}            
    """.format(name=subscription["name"],
               parsed_required_args=indent(parsed_required_args, 2),
               parsed_optional_args=indent(parsed_optional_args, 2),
               query=create_query(subscription),
               func_args_list=func_args_list,
               query_args="",
               yieldVal='yield data["{name}"]'.format(name=subscription["name"]) if subscription["type"][
                   "kind"] == "SCALAR" or subscription["type"]["name"][0] != subscription["type"]["name"].upper()[0] else 'yield %s(self.client, data["{name}"]["id"])'.format(name=subscription["name"]) % subscription["type"]["name"]
               )


with open("subscriptions.py", "w") as f:
    f.write("""# programmatically generated file
from .models.user import User
from .models.permanent_token import PermanentToken
from .models.pending_environment_share import PendingEnvironmentShare
from .models.environment import Environment
from .models.thing import Thing
from .models.float_value import FloatVariable
from .models.pending_owner_change import PendingOwnerChange
from .models.notification import Notification
from .models.boolean_value import BooleanVariable
from .models.string_value import StringVariable
from .models.float_series_value import FloatSeriesVariable
from .models.category_series_value import CategorySeriesVariable
from .models.category_series_node import CategorySeriesNode
from .models.file_value import FileVariable
from .models.float_series_node import FloatSeriesNode

class SubscriptionRoot:
    def __init__(self, client):
        self.client = client
""")

    for subscription in introspection["subscriptionType"]["fields"]:
        f.write(create_handler(subscription))
