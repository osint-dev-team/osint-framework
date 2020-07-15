#!/usr/bin/env python3

import requests
import aiohttp
import asyncio
from src.core.utils.response import ScriptResponse
from src.core.base.osint import OsintRunner


class Networks:
    def __init__(self):
        with open("./src/scripts/osint/check_nickname/social_networks.txt") as f:
            self.net = [str(i).strip() for i in f.readlines()]


def check_nickname_sync(nickname: str) -> str:
    """
    checks nicknames from social networks(sync)
    :param nickname: just nickname :)
    :return: list with links to user from social
     networks which have this nickname
    """
    ans = []
    social = Networks().net
    for site in social:
        try:
            url = "https://{site}{nickname}".format(site=site, nickname=nickname)
            response = requests.get(url)
            if response.status_code == 200:
                ans.append(url)
        except:
            pass
    return ans


async def check_nickname_async(nickname, social) -> str:
    """
    checks nicknames from social networks(async)
    :param nickname: just nickname :)
    :return: list with links to user from social
    networks which have this nickname
    """
    ans = []
    async with aiohttp.ClientSession() as session:
        while not social.empty():
            url = await social.get()
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        ans.append(url)
            except:
                pass
    return ans


class Runner(OsintRunner):
    def __init__(self, logger: str = __name__):
        super().__init__()

    async def __run(self, *args, **kwargs):
        try:
            username = kwargs.get("username")
            social = asyncio.Queue()
            for site in Networks().net:
                await social.put(
                    "https://{site}{username}".format(site=site, username=username)
                )
            temp_result = await asyncio.gather(
                *[
                    asyncio.create_task(check_nickname_async(username, social))
                    for flow in range(10)
                ]
            )
            result = {username: []}
            for sub_massive in temp_result:
                for site in sub_massive:
                    result[username].append(site)
            return ScriptResponse.success(
                result=result,
                message="Found {count} user accounts".format(
                    count=len(result[username])
                ),
            )
        except Exception as err:
            return ScriptResponse.error(message=str(err))

    def run(self, *args, **kwargs):
        username = kwargs.get("username")
        return asyncio.run(self.__run(username=username))