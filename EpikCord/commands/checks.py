from ..exceptions import FailedCheck
from logging import getLogger
from typing import (
    Optional,
    Callable
)

logger = getLogger(__name__)

class Check:
    def __init__(self, callback):
        self.callback = callback
        self.success_callback = self.default_success
        self.failure_callback = self.default_failure

    def success(self, callback: Optional[Callable] = None):
        self.success_callback = callback or self.default_success

    def failure(self, callback: Optional[Callable] = None):
        self.failure_callback = callback or self.default_failure

    async def default_success(self, interaction):
        logger.info(
            f"{interaction.author.username} ({interaction.author.id}) passed "
            f"the check {self.command_callback.__name__}. "
        )

    async def default_failure(self, interaction):
        logger.critical(
            f"{interaction.author.username} ({interaction.author.id}) failed "
            f"the check {self.command_callback.__name__}. "
        )
        raise FailedCheck(
            f"{interaction.author.username} ({interaction.author.id}) failed "
            f"the check {self.command_callback.__name__}. "
        )
