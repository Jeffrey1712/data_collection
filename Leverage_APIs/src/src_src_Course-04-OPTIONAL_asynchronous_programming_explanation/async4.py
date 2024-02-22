import asyncio

async def main():
    await bye()
    print("Hello!")

async def bye():
    print("OK")
    await asyncio.sleep(4) # forces the program to wait for one second
    print("Goodbye!")

asyncio.run(main())
