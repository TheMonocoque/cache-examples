#!/usr/bin/env python

from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.requests import Request
import hashlib

# run with python -m uvicorn etagfastapi:app
app = FastAPI()


def get_resource_content():
    return "example-content"


def generate_etag(content):
    hashed = hashlib.sha1(content.encode()).hexdigest()
    return f'"{hashed}"'


@app.get("/resource")
async def resource(request: Request):
    content = get_resource_content()
    etag = generate_etag(content)

    if_none_match = request.headers.get("If-None-Match")

    if if_none_match == etag:
        return Response(status_code=304)
    else:
        headers = {"ETag": etag}
        return Response(content=f"Current content: {content}\n", status_code=200, headers=headers)
