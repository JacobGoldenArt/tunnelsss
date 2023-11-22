from dataclasses import field
from app.models.base_model import BlockBase
from typing import Dict, Any, Optional
import asyncio


class Block(BlockBase):
    """
    Base class for all blocks.
    """

    data: Optional[Dict[str, Any]] = field(default_factory=dict)

    async def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process method for this block class.
        """
        await asyncio.sleep(5)
        return {self.name: data}

    async def input(self, data: Dict[str, Any]) -> None:
        """
        Inputs data into the block.
        """
        self.data = data
        processed_data = await self.process(self.data)
        self.processed.set(processed_data)
