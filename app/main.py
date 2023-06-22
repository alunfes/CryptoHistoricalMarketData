import asyncio
import os
from DataDownLoader import DataDownLoader


class main:
    def __init__(self) -> None:
        print(os.getcwd())

    async def start(self):
        ddl = DataDownLoader()
        try:
            async with asyncio.TaskGroup() as tg:
                task = tg.create_task(ddl.start())
        except* Exception as err:
            print(f"{err.exceptions=}")


if __name__ == '__main__':
    m  = main()
    asyncio.run(m.start())