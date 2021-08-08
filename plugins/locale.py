"""
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>
"""

from os import path
from enum import Enum

import rapidjson as json


# Maps Telegram-specific locales to
# internal locale representation
class Locale(str, Enum):
    """
    Path to Locale String Resources.

    The locale directory should be in the same
    directory as locale.py.
    """
    PT_BR = "locale/pt_BR.json"
    EN_US = "locale/en_US.json"

    DEFAULT = EN_US

    @classmethod
    def load(cls, string):
        language_codes = {
            "en"   : cls.EN_US,
            "pt-br": cls.PT_BR,
        }

        locale = cls.DEFAULT
        try:
            locale = language_codes[string]
        except KeyError:
            pass

        return locale
    


class StringResources:
    """
    Load String Resources from a file.

    Loads string resources dynamically, to access all
    available string resouces, check the instance class
    member.
    """
    instance = {}
    _dirname = path.dirname(__file__)

    def __init__(self, resource_file=None) -> None:
        if resource_file == None:
            raise TypeError("resource_file must be a string pointing to a locale file")

        if resource_file in StringResources.instance:
            self.res = StringResources.instance[resource_file]
            return

        f = None
        fpath = path.join(StringResources._dirname, resource_file)

        try:
            f = open(fpath, "r")
        except FileNotFoundError as e:
            raise e

        self.res = json.loads(f.read())
        f.close()

        StringResources.instance[resource_file] = self.res
