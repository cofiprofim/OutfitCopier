from typing import Optional

from .external import *
from ..visuals import Display
from ..auth import Auth


class Outfit:
    def __init__(self, data) -> None:
        self.scales = BodyScales(data.get("scales"))
        self.avatar_type = data.get("playerAvatarType")
        self.body_colors = BodyColors(data.get("bodyColor3s"))
        
        self.assets = [Item(asset) for asset in data.get("assets", ())]
        self.emotes = [Emote(emote) for emote in data.get("emotes", ())]
    
    async def set_avatar_type(self, from_user: Auth) -> int:
        data = {
            "playerAvatarType": self.avatar_type
        }
        
        async with from_user.session.post(
            "https://avatar.roblox.com/v1/avatar/set-player-avatar-type",
            json=data,
            ssl=False
        ) as response:
            return response.status
    
    async def set_assets(self, from_user: Auth) -> int:
        data = {
            "assets": [asset.to_dict() for asset in self.assets]
        }
        
        async with from_user.session.post(
            "https://avatar.roblox.com/v2/avatar/set-wearing-assets",
            json=data,
            ssl=False
        ) as response:
            return await response.json()
    
    async def copy(self, from_user: Auth, *, log: Optional[bool] = None) -> None:
        if log: Display.info("Setting the same scales to avatar")
        await self.scales.set_scales(from_user)
        
        if log: Display.info("Setting the avatar type")
        await self.set_avatar_type(from_user)
        
        if log: Display.info("Setting the same body colors")
        await self.body_colors.set_colors(from_user)
        
        if log: Display.info("Wearing user assets")
        await self.set_assets(from_user)
        
        Display.success("Copied user outfit")
