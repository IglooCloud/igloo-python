async def _asyncWrapWith(res, wrapper_fn):
    result = await res
    return wrapper_fn(result["id"])


def wrapWith(res, wrapper_fn):
    if isinstance(res, dict):
        return wrapper_fn(res)
    else:
        return _asyncWrapWith(res, wrapper_fn)
