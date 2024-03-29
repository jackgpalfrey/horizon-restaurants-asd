# Author: Jack Palfrey (22032928)
"""Module for individual pages."""
import tkinter as tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .PageManager import PageManager


class Page(tk.Frame):
    """A special type of frame for pages."""

    def __init__(self, page_manager: "PageManager", *args, **kwargs):
        """Provide PageManager."""
        self._manager = page_manager
        tk.Frame.__init__(self, page_manager, *args, **kwargs)

    @property
    def pages(self) -> "PageManager":
        """Get access to parent PageManager class."""
        return self._manager

    def show(self) -> None:
        """Show page, should rarely be used outside of PageManager."""
        self.pack(fill=tk.X)
        self.on_show()

    def hide(self):
        """Hide page, should rarely be used outside of PageManager."""
        self.pack_forget()

    def on_show(self):
        pass


class GridPage(Page):

    @property
    def pages(self) -> "PageManager":
        """Get access to parent PageManager class."""
        return self._manager

    def show(self) -> None:
        """Show page, should rarely be used outside of PageManager."""
        self.grid()

    def hide(self):
        """Hide page, should rarely be used outside of PageManager."""
        self.grid_forget()
