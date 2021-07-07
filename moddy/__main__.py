from moddy.utils import log
from moddy.bot import main
import asyncio
from moddy.utils import session


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        log("Exiting....")
        asyncio.run(session.close())
