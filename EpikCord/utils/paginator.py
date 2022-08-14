from typing import List
from ..message import Embed

class Paginator:
    def __init__(self, *, pages: List[Embed]):
        self.current_index: int = 0
        self.__pages = pages

    def __iter__(self):
        return self

    def __len__(self):
        return len(self.__pages)

    def __next__(self):
        return self.forward()

    @property
    def page(self):
        return self.__pages[self.current_index]

    def forward(self):
        self.current_index = min(len(self.__pages), self.current_index + 1)
        return self.__pages[self.current_index]

    def back(self):
        self.current_index = max(0, self.current_index - 1)
        return self.__pages[self.current_index]

    def first(self):
        self.current_index = 0

    def last(self):
        self.current_index = len(self.__pages)

    def add_page(self, page: Embed):
        self.__pages.append(page)

    def insert_page(self, page: Embed, index: int):
        if index >= len(self.__pages):
            self.add_page(page)
            return

        self.__pages.index(page, index)

    def remove_page(self, page: Embed):
        self.__pages = list(filter(lambda embed: embed != page, self.__pages))