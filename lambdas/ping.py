import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class HTTPError(Exception):
    """API Gateway can recognise HTTPError and use the status code and data for its error response templates.  N.B this
    is the only point of coupling between the λ and API Gateway.  It allows idomatic python to be written and convert
    properly"""

    def __init__(self, msg, code):
        Exception.__init__(self, json.dumps({"statusCode": code, "data": msg}))


class HTTPResponse(dict):
    def __init__(self, data: object, code: int = 200):
        """Allows `data` to be returned with a custom http code. N.b, this requires matching response mapping API
        Gateway configuration.  E.g:

        >>> HTTPResponse("I'm a teapot", 418)
        >>> HTTPResponse("created", 201)
        """
        self["statusCode"] = code
        self["data"] = data


def main(event, context):
    logger.info(f"Event: {json.dumps(event)}")

    # KeyErrors are prevented by APIG
    if event["details"]["msg"] == "200":
        return "pong"  # default 200
    if event["details"]["msg"] == "404":
        raise HTTPError("Not Found", 404)
    if event["details"]["msg"] == "201":
        return HTTPResponse("created", 201)

    raise Exception(f"unrecognised msg '{event['details']['msg']}'")
