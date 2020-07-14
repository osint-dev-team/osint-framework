#!/usr/bin/env python3
import requests
import aiohttp
import asyncio
from src.core.utils.log import Logger
from src.core.utils.response import ScriptResponse
from src.core.base.osint import BaseRunner
from time import sleep

class networks:
    def __init__(self):
        with open("./src/scripts/osint/check_nickname/social_networks.txt") as f:
            self.net = [str(i).strip() for i in f.readlines()]

#for the black times i wrote sync

def check_nickname_sync(nickname) -> str:
    """
    checks nicknames from social networks(sync)
    :param nickname: just nickname :)
    :return: list with links to user from social
     networks which have this nickname
    """
    ans = []
    social = networks().net
    for i in social:
        try:
            url = "https://"+i+nickname
            s = requests.Session()
            r = s.get(url)
            if(r.status_code == 200):
                ans.append(url)
        except:
            print("ERROR!!!!!")
    return ans

async def check_nickname_async(nickname,social) -> str:
    """
    checks nicknames from social networks(async)
    :param nickname: just nickname :)
    :return: list with links to user from social
    networks which have this nickname
    """
    ans = []
    async with aiohttp.ClientSession() as s:
        while not social.empty():
            url = await social.get()
            try:
                async with s.get(url) as r:
                    if(r.status == 200):
                        ans.append(url)
            except:
                print("ERROR!!!!")
    return ans

class Runner(BaseRunner):
    def __init__(self, logger: str = __name__):
        super().__init__()
    async def __run(self,*args,**kwargs):
        try:
            username = kwargs.get("username")
            social = asyncio.Queue()
            for i in networks().net:
                await social.put("https://" + i + username)
            temp_result = await asyncio.gather(
                *[asyncio.create_task(check_nickname_async(username, social)) for i in range(10)])
            temp_temp_result = []
            for i in temp_result:
                for j in i:
                    temp_temp_result.append(j)
            result = {username : temp_temp_result}
            return ScriptResponse.success(
                result=result,
                message="yeah"
            )
        except Exception as err:
            return ScriptResponse.error(message=str(err))
    def run(self, *args, **kwargs):
        return asyncio.run(self.__run(username="admin"))


"""if __name__ =="__main__":
    srcipt_module = Runner()
    srcipt_result = asyncio.run(srcipt_module.run(username="admin"))
    print(srcipt_result)
"""

