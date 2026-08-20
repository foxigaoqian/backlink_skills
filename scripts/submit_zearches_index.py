#!/usr/bin/env python3
"""Use the live Zearches homepage form, where submissions are currently located."""

import submit_zearches as zearches

zearches.SUBMIT_PAGE = "https://zearches.com/index.php"

if __name__ == "__main__":
    raise SystemExit(zearches.main())
