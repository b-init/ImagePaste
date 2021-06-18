# Pasteboard - Python interface for reading from NSPasteboard (macOS clipboard)
# Copyright (C) 2017-2021  Toby Fleming
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at https://mozilla.org/MPL/2.0/.
import sys as _sys

assert _sys.platform == "darwin", "pasteboard only works on macOS"

from ._native import *


class PasteboardType:
    """Make type hints not fail on import - don't use this class"""

    pass
