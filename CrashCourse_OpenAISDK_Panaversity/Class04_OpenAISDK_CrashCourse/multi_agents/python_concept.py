import asyncio
import time

async def math():
    
    # time is sync function
    # time.sleep(2) # we are performing async task in async task function, when using await math

    await asyncio.sleep(2) # we are using this instead of time.sleep in parallelization

    return 2 + 2

async def english():

    # time.sleep(3) # we are performing async task in async task function, when using await math

    await asyncio.sleep(3) # we are using this instead of time.sleep in parallelization

    return "Hello"

async def main():
    start_time = time.time()

    # await math # line execution is still sync, but the function is not, its an async function
    
    # await english # line execution is still sync, but the function is not, its an async function

    # To make is async, we use asyncio.gather(), it will run both functions at the same time and its called parallelization
    await asyncio.gather(math(), english())

    end_time = time.time()
    print(f"\nTime taken: {end_time - start_time} seconds\n")

if __name__ == "__main__":
    asyncio.run(main())

