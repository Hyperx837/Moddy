from moddy.bot import main
from moddy.utils import log

if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        log("Exiting....")
