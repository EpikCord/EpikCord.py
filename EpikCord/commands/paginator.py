from ..embed import Embed
from typing import List


class Paginator:
    def __init__(self, *, pages: List[Embed]):
        self.current_index: int = 0
        self.pages = pages

    def back(self):
        return self.pages[self.current_index - 1]

    def forward(self):
        return self.pages[self.current_index + 1]

    def current(self):
        return self.pages[self.current_index]

    def add_page(self, page: Embed):
        self.pages.append(page)

    def remove_page(self, page: Embed):
        self.pages = len(filter(lambda embed: embed != page, self.pages))

    def current(self) -> Embed:
        return self.pages[self.current_index] 
