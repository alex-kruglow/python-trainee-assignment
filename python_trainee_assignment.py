import aiohttp
import logging

logger = logging.getLogger(__name__)


async def get_matrix(url: str) -> list[int]:
    pass


async def _get_data_by_url(url: str) -> str | None:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                text: str = await resp.text()
    return text


def _convert_str_matrix_to_list_matrix(str_matrix: str) -> list[list[int]]:
    pass


def _travers_matrix(matrix: list[list[int]]) -> list[int]:
    pass
