from typing import (
    Tuple,
    Optional,
    Mapping,
    Union,
    Literal,
    overload
)

from ..visuals import Display
from ..auth import Auth

__all__ = ("Item", "Emote", "BodyColors", "BodyScales")


class Item:
    @overload
    def __init__(
        self,
        _id: int,
        name: Optional[str] = None,
        positions: Optional[Tuple[int, int, int]] = None,
        rotations: Optional[Tuple[int, int, int]] = None,
        scale: Optional[int] = None
    ) -> None:
        pass
    
    @overload
    def __init__(
        self,
        _id: int,
        name: Optional[str] = None,
        order: Optional[int] = None
    ) -> None:
        pass
    
    @overload
    def __init__(self, data: Mapping[str, Mapping[str, Union[int, Mapping[str, int]]]]) -> None:
        pass
    
    def __init__(
        self,
        option_1,
        option_2: Optional[str] = None,
        option_3: Optional[Union[int, Tuple[int, int, int]]] = None,
        rotations: Optional[Tuple[int, int, int]] = None,
        scale: Optional[int] = None
    ) -> None:
        
        if isinstance(option_1, int):
            self.id = option_1
            self.name = option_2
            
            if isinstance(option_3, tuple):
                self.position = option_3
                self.rotation = rotations
                self.scale = scale
                
                self.order = None
                
                self.__type = "Asset"
            
            elif isinstance(option_3, int):
                self.order = option_3
                
                self.position = None
                self.rotation = None
                self.scale = None
                
                self.__type = "3DClothing"
        
        elif isinstance(option_1, dict):
            self.id = option_1["id"]
            self.name = option_1["name"]
            
            meta = option_1.get("meta", dict())
            
            self.order = meta.get("order")
            
            if self.order is None:
                self.position = list(meta.get("position").values()) if meta.get("position") is not None else None
                self.rotation = list(meta.get("rotation").values()) if meta.get("rotation") is not None else None
                self.scale = (meta.get("scale", dict()).get("x") or None)
                
                self.__type = "Asset"
                
            else:
                self.position = None
                self.rotation = None
                self.scale = None
                
                self.__type = "3DClothing"
            
        else:
            Display.exception("Invalid item format provided")
    
    @property
    def item_type(self) -> Literal["Asset", "3DClothing"]:
        return self.__type
    
    def to_dict(self) -> Mapping[str, Mapping[str, Union[int, Mapping[str, int]]]]:
        
        def from_coords(coords: Tuple[int, int, int]) -> Mapping[str, int]:
            if len(coords) == 3:
                data = {
                    "X": coords[0],
                    "Y": coords[1],
                    "Z": coords[2]
                }
                return data
            
            elif len(coords) == 1:
                coord = coords[0]
                
                data = {
                    "X": coord,
                    "Y": coord,
                    "Z": coord
                }
                return data
        
        data = {
            "id": self.id
        }
        
        if self.__type == "Asset" and any(val is not None for val in (self.position, self.rotation, self.scale)):
            data.update({"meta": dict()})
            
            if self.position is not None:
                data["meta"]["position"] = from_coords(self.position)
            if self.rotation is not None:
                data["meta"]["rotation"] = from_coords(self.rotation)
            if self.scale is not None:
                data["meta"]["scale"] = from_coords(self.scale)
            
        elif self.__type == "3DClothing":
            data = {
                "id": self.id,
                "meta": {
                    "order": self.order
                }
            }

        return data


class Emote:
    @overload
    def __init__(
        self,
        _id: int,
        slot: int,
        name: Optional[str] = None
    ) -> None:
        pass
    
    @overload
    def __init__(self, data: Mapping[str, Union[str, int]]) -> None:
        pass
    
    def __init__(
        self,
        option_1,
        slot: Optional[int] = None,
        name: Optional[str] = None
    ) -> None:
        
        if isinstance(option_1, int):
            self.id = option_1
            self.name = name
            self.__slot = slot
            
        elif isinstance(option_1, dict):
            self.id = option_1.get("assetId")
            self.name = option_1.get("assetName")
            self.__slot = option_1.get("position")
            
        else:
            Display.exception("Invalid item format provided")
        
        if self.__slot > 8 or self.__slot < 1:
            Display.exception("Slot value can only be from 1 to 8")
    
    @property
    def slot(self) -> int:
        return self.__slot
    
    @slot.setter
    def slot(self, new: int) -> None:
        if new > 8 or new < 1:
            return Display.exception("Slot value can only be from 1 to 8")
        
        self.__slot = new
    
    async def set_emote(self, from_user: Auth, *, slot: Optional[int] = None) -> int:
        if slot is not None and (slot > 8 or slot < 1):
            return Display.exception("Slot value can only be from 1 to 8")
        
        async with from_user.session.post(
            f"https://avatar.roblox.com/v1/emotes/{self.id}/{self.slot}",
            ssl=False
        ) as response:
            return response.status


class BodyColors:
    @overload
    def __init__(
        self,
        head: str,
        torso: str,
        right_arm: str,
        left_arm: str,
        right_leg: str,
        left_leg: str
    ) -> None:
        pass
    
    @overload
    def __init__(self, data: Mapping[str, str]) -> None:
        pass
    
    def __init__(
        self,
        option,
        torso: Optional[str] = None,
        right_arm: Optional[str] = None,
        left_arm: Optional[str] = None,
        right_leg: Optional[str] = None,
        left_leg: Optional[str] = None
    ) -> None:
        
        if isinstance(option, str):
            self.head = option
            self.torso = torso
            self.right_arm = right_arm
            self.left_arm = left_arm
            self.right_leg = right_leg
            self.left_leg = left_leg
        
        elif isinstance(option, dict):
            self.head = option.get("headColor3")
            self.torso = option.get("torsoColor3")
            self.right_arm = option.get("rightArmColor3")
            self.left_arm = option.get("leftArmColor3")
            self.right_leg = option.get("rightLegColor3")
            self.left_leg = option.get("leftLegColor3")
        
        else:
            Display.exception("Invalid body color format provided")
    
    async def set_colors(self, from_user: Auth) -> int:
        data = {
            "headColor3": self.head,
            "torsoColor3": self.torso,
            "rightArmColor3": self.right_arm,
            "leftArmColor3": self.right_arm,
            "rightLegColor3": self.right_leg,
            "leftLegColor3": self.left_leg
        }
        
        async with from_user.session.post(
            "https://avatar.roblox.com/v2/avatar/set-body-colors",
            json=data,
            ssl=False
        ) as response:
            return response.status


class BodyScales:
    @overload
    def __init__(
        self,
        height: float,
        width: float,
        head: int,
        depth: int,
        proportion: int,
        body_type: float
    ) -> None:
        pass
    
    @overload
    def __init__(self, data: Mapping[str, Union[int, float]]) -> None:
        pass
    
    def __init__(
        self,
        option,
        width: Optional[float] = None,
        head: Optional[int] = None,
        depth: Optional[int] = None,
        proportion: Optional[int] = None,
        body_type: Optional[float] = None
    ) -> None:
        
        if isinstance(option, str):
            self.height = option
            self.width = width
            self.head = head
            self.depth = depth
            self.proportion = proportion
            self.body_type = body_type
        
        elif isinstance(option, dict):
            self.height = option.get("height")
            self.width = option.get("width")
            self.head = option.get("head")
            self.depth = option.get("depth")
            self.proportion = option.get("proportion")
            self.body_type = option.get("bodyType")
        
        else:
            Display.exception("Invalid body color format provided")
    
    async def set_scales(self, from_user: Auth) -> int:
        data = {
            "height": self.height,
            "width": self.width,
            "head": self.head,
            "depth": self.depth,
            "proportion": self.proportion,
            "bodyType": self.body_type
        }
        
        async with from_user.session.post(
            "https://avatar.roblox.com/v1/avatar/set-scales",
            json=data,
            ssl=False
        ) as response:
            return response.status
