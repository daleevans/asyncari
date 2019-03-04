#!/usr/bin/python3

"""Example demonstrating ARI channel origination.

"""

#
# Copyright (c) 2013, Digium, Inc.
#
import trio_ari
import trio
import logging

from pprint import pprint

import os
ast_host = os.getenv("AST_HOST", 'localhost')
ast_port = int(os.getenv("AST_ARI_PORT", 8088))
ast_url = os.getenv("AST_URL", 'http://%s:%d/'%(ast_host,ast_port))
ast_username = os.getenv("AST_USER", 'asterisk')
ast_password = os.getenv("AST_PASS", 'asterisk')
ast_app = os.getenv("AST_APP", 'hello')
ast_outgoing = os.getenv("AST_OUTGOING", 'SIP/blink')

async def clean_bridges(client):
    #
    # Find (or create) a holding bridge.
    #
    for b in await client.bridges.list():
        if b.channels:
            continue
        await b.destroy()

async def main():
    async with trio_ari.connect(ast_url, ast_app, ast_username,ast_password) as client:
        await clean_bridges(client)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    trio.run(main)
