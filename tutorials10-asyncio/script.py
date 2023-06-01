import asyncio
import time

start = time.perf_counter()

my_data = {}

async def fetch_data():
    val = 1
    for i in range(10):
        await asyncio.sleep(2.3)
        my_data.update({'apples': val})
        val += 1
        print(my_data)
        
async def print_data():
    for i in range(2,22,2):
        await asyncio.sleep(2)
        print(f"{i} seconds passed.")

async def main():
    print("start fetching")
    task1 = asyncio.create_task(fetch_data())
    task2 = asyncio.create_task(print_data())
    await task1
    await task2
    print("done fetching")

asyncio.run(main())

end = time.perf_counter()
print(f"Elapsed time: {(end-start):.3f} seconds")