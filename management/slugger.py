# coding=utf-8

import re


def slug(string):
    string = re.sub(r'æ', 'ae', string, flags=re.I)
    string = re.sub(r'ø', 'o', string, flags=re.I)
    string = re.sub(r'å', 'a', string, flags=re.I)

    return re.sub(r'[-\s]+', '-',
                  (re.sub(r'[^\w\s-]', '', string).strip().lower()))
