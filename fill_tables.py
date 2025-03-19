from fill_database import *
import asyncio


async def populate_all():
    await add_users()
    await add_roadmaps()
    await add_cards()
    await add_roadmap_cards()
    await add_card_links()
    await add_user_roadmaps()
    await add_user_cards()
    
   

if __name__ == "__main__":
    asyncio.run(populate_all())
