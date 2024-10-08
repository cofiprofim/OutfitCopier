import sys
import os

VERSION = "1.0.0"

try:
    import asyncio
    import traceback
    
    from core.auth import Auth
    from core.visuals import Display, Tools
    from core.copier import Outfit
    from core.detection import get_user_id, load_user_avatar
    
    os.system("cls" if os.name == "nt" else "clear")
except ModuleNotFoundError:
    install = input("Uninstalled modules found, do you want to install them? Y/n: ").lower() == "y"

    if install:
        print("Installing modules now...")
        os.system("pip install aiohttp rgbprint")
        print("Successfully installed required modules.")
    else:
        print("Aborting installing modules.")

    input("Press \"enter\" to exit...")
    sys.exit(1)
     

async def start(cookie: str):    
    auth = Auth(cookie)
    
    await auth.update_auth_info()
    if auth.user_id is None:
        Display.exception("Invalid cookie provided")
    
    while True:
        Tools.clear_console()
        Display.main()
        
        choice = await Display.user_input("Enter user name or ID you want to copy from\n > ")
        
        Display.info("Checking user name or ID to be valid...")
        user_id = await get_user_id(choice, auth)
        
        if user_id is None:
            Display.error("Invalid user that you provided is invalid or banned")
            await asyncio.sleep(1)
            continue
        Display.success("User name or ID is valid!")
        
        Display.info("Starting coping user outfit...")
        outfit_data = await load_user_avatar(user_id, auth)
        
        await Outfit(outfit_data).copy(auth, log=True)
        input("Press any key to continue...")


async def main():
    Tools.clear_console()
    
    try:
        with open("cookie.txt", "r") as f:
            cookie = f.read()
        
        if not cookie:
            return Display.exception(f"Invalid cookie provided")
        
    except FileNotFoundError:
        return Display.exception(f"File with cookie was not found")

    except Exception as err:
        return Display.exception(f"Failed to load cookie file: {err}")

    try:
        await start(cookie)
    except Exception:
        return Display.exception(f"Unknown error occurred:\n\n{traceback.format_exc()}")


if __name__ == "__main__":
    asyncio.run(main())
