#!/usr/bin/env python

"""Brief example of using the channel API.

This app will answer any channel sent to Stasis(hello), and play "Hello,
world" to the channel. For any DTMF events received, the number is played back
to the channel. Press # to hang up, and * for a special message.
"""

#
# Copyright (c) 2013, Digium, Inc.
#

import trio_ari
import trio_asyncio
import trio
import logging

import os
ast_url = os.getenv("AST_URL", 'http://localhost:8088/')
ast_username = os.getenv("AST_USER", 'asterisk')
ast_password = os.getenv("AST_PASS", 'asterisk')
ast_app = os.getenv("AST_APP", 'hello')

async def on_dtmf(channel, event):
    """Callback for DTMF events.

    When DTMF is received, play the digit back to the channel. # hangs up,
    * plays a special message.

    :param channel: Channel DTMF was received from.
    :param event: Event.
    """
    digit = event['digit']
    print(digit)
    await trio.sleep(0.01)
    if digit == '#':
        await channel.play(media='sound:goodbye')
        await trio.sleep(2)
        await channel.continueInDialplan()
    elif digit == '*':
        await channel.play(media='sound:asterisk-friend')
    else:
        await channel.play(media='sound:digits/%s' % digit)


async def on_start(objs, event):
    """Callback for StasisStart events.

    On new channels, register the on_dtmf callback, answer the channel and
    play "Hello, world"

    :param channel: Channel DTMF was received from.
    :param event: Event.
    """
    channel = objs['channel']
    await trio.sleep(0.01)
    #r = await channel.getChannelVar(variable="CALLERID(num)")
    #t = await channel.getChannelVar(variable="CALLERID(ton)")
    #print("** START **", channel, t,r,event)
    channel.on_event('ChannelDtmfReceived', on_dtmf)
    await channel.answer()
    await channel.play(media='sound:hello-world')

async def on_end(channel, event):
    """Callback for StasisEnd events.

    :param channel: Channel DTMF was received from.
    :param event: Event.
    """
    #print("** END **", channel, event)

logging.basicConfig(level=logging.DEBUG)
async def main():
    async with trio_ari.connect(ast_url, ast_app, ast_username,ast_password) as client:
        client.on_channel_event('StasisStart', on_start)
        client.on_channel_event('StasisEnd', on_end)
        # Run the WebSocket
        async for m in client:
            print("** EVENT **", m)

if __name__ == "__main__":
    trio_asyncio.run(main)