from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError


def custom_exception_handler(exc, context):
    resp = exception_handler(exc, context)

    if isinstance(exc, ValidationError) and resp is not None:

        codes = exc.get_codes()

        def contains_unique(v):
            if isinstance(v, list):
                return any(c == "unique" for c in v)
            if isinstance(v, dict):
                return any(contains_unique(x) for x in v.values())
            return v == "unique"

        if contains_unique(codes):
            return Response(resp.data, status=status.HTTP_409_CONFLICT)

    return resp
