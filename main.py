# Back-compat shim: the game now lives in the qicqacqoe package.
# Prefer `qicqacqoe` (after pip install) or `python -m qicqacqoe`.
from qicqacqoe.game import main

if __name__ == "__main__":
    main()
