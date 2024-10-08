import aiohttp
import asyncio


class Auth:
    def __init__(self, cookie: str) -> None:
        self.cookie = cookie

        self.user_id = None
        self.name = None
        self.username = None

        self.session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(limit=None, ssl=False),
            trust_env=True,
            cookies={".ROBLOSECURITY": self.cookie}
        )

        asyncio.create_task(self.update_csrf_token())

    async def close_session(self):
        await self.session.close()

    async def update_csrf_token(self, csrf_token: str | None = None) -> None:
        if csrf_token is None:
            async with aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(limit=None, ssl=False),
                trust_env=True
            ) as session:
                async with session.post(
                        "https://economy.roblox.com/",
                        cookies={".ROBLOSECURITY": self.cookie},
                        ssl=False
                ) as response:
                    csrf_token = response.headers.get("x-csrf-token")

        self.session.headers.update({"x-csrf-token": csrf_token})

    async def update_auth_info(self) -> None:
        async with self.session.get("https://users.roblox.com/v1/users/authenticated",
                                    ssl=False) as response:
            data = await response.json()

            if response.status != 200 or data.get("errors") and data["errors"][0].get("code") == 0:
                return None

            self.user_id = data.get("id")
            self.name = data.get("displayName")
            self.username = data.get("name")

            return None
