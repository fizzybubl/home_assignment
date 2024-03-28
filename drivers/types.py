from typing import Literal


ByType = Literal["id", "css selector", "xpath", "class name", "name", "partial link text", "link text"]

LocatorType = tuple[ByType, str]
