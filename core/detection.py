from typing import Union
from aiohttp import ClientResponse

from .auth import Auth


async def check_user_id(user_id: int, auth: Auth) -> Union[int, None]:
    async with auth.session.get(
            f"https://users.roblox.com/v1/users/{user_id}",
            ssl=False,
    ) as response:
        
        data = await response.json()
        return user_id if data.get("errors") is None and not data.get("isBanned", True) else None


async def get_user_by_name(user_name: str, auth: Auth) -> Union[int, None]:
    data = {
        "usernames": (user_name,),
        "excludeBannedUsers": True
    }
    
    async with auth.session.post(
            f"https://users.roblox.com/v1/usernames/users",
            json=data,
            ssl=False,
    ) as response:

        data = (await response.json()).get("data")
        return data[0]["id"] if response.status == 200 and data else None


async def get_user_id(user_id_name: Union[int, str], auth: Auth) -> Union[int, None]:
    return (await check_user_id(int(user_id_name, auth)) if isinstance(user_id_name, int) or user_id_name.isdigit()
           else await get_user_by_name(user_id_name, auth))


async def load_user_avatar(user_id: int, auth: Auth) -> ClientResponse:
    async with auth.session.get(
        f"https://avatar.roblox.com/v2/avatar/users/{user_id}/avatar",
        ssl=False
    ) as response:
        return await response.json()


async def load_avatar(from_user: Auth) -> ClientResponse:
    async with from_user.session.get(
        f"https://avatar.roblox.com/v2/avatar/avatar",
        ssl=False
    ) as response:
        return await response.json()
