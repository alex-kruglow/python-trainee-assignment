import aiohttp
import asyncio
import logging

logger = logging.getLogger(__name__)


async def get_matrix(url: str) -> list[int]:
    '''Return traversed matrix which was gotten by the url.

    Params:
        url: str - URL address to get text with matrix.
    Returns:
        list[int] - traversed matrix.
    '''
    data: str | None = await _get_data_by_url(url)
    if data is None:
        raise Exception('Cannot get data by network')
    matrix: list[list[int]] = _convert_str_matrix_to_list_matrix(data)
    if _is_matrix_squared(matrix):
        return _travers_matrix(matrix)
    else:
        return []


async def _get_data_by_url(url: str) -> str | None:
    '''Return data from URL.

    Params:
        url: str - URL address to get data.
    Returns:
        str or None - text from the URL.
    '''
    logger.info(f'Request to {url}.')
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    return await resp.text()
                elif 400 <= resp.status < 500:
                    logger.error(
                        f'Request to {url} returned {resp.status} code'
                    )
                elif 500 <= resp.status:
                    logger.error(
                        f'Request to {url} returned {resp.status} code'
                    )
        except aiohttp.ClientConnectionError as e:
            logger.error(f'Request to {url}. Connection error. {e}')
        except asyncio.TimeoutError as e:
            logger.error(f'Request to {url}. Timeout error. {e}')
    return None


def _convert_str_matrix_to_list_matrix(str_matrix: str) -> list[list[int]]:
    '''Return matrix as list[list[int]].
    This is converted matrix from string.

    Params:
        str_matrix: str - matrix as string.
    Returns:
        list[list[int]] - matrix as array.
    '''
    logger.info(f'Converting matrix began. Matrix: {str_matrix}')
    result: list = []
    for line in str_matrix.split('\n'):
        if line and line[0] != '+':
            result.append(
                [int(item.strip()) for item in line[1:-2].split('|')]
            )
    logger.info(f'Converting matrix completed. Result: {result}')
    return result


def _is_matrix_squared(matrix: list[list[int]]) -> bool:
    '''Return True if matrix is squared.
    It means that length of lines are equal items in lines.

    Params:
        matrix: list[list[int]] - matrix to check.
    Returns:
        bool - result of checking.
    '''
    if not all([len(item) == len(matrix) for item in matrix]):
        logger.warning('Matrix is not squared!')
        return False
    else:
        logger.info('Matrix is squared.')
        return True


def _travers_matrix(matrix: list[list[int]]) -> list[int]:
    '''Return list of matrix items which are passed
    of matrix by counterclockwise.

    Params:
        matrix: list[list[int]] - matrix to process.
    Returns:
        list[int] - items by counterclockwise.
    '''
    result: list = []
    for i in range(int(len(matrix) / 2) + 1):
        submatrix: list = [
            item[i:len(item)-i] for item in matrix[i:len(matrix)-i]
        ]
        if submatrix:
            if len(submatrix) == 1 and len(submatrix[0]) == 1:
                # Break the for if there is only one item in submatrix.
                # It processes the item in the end of function.
                break
            result.extend([ln[0] for ln in submatrix if ln])  # left side
            result.extend(submatrix[-1][1:-1])  # bottom side
            result.extend([ln[-1] for ln in submatrix if ln][::-1])  # right
            result.extend(submatrix[0][1:-1][::-1])  # top side
    if len(matrix) % 2:
        # If len(matrix) is odd then it adds the center item in the end.
        result.append(matrix[int(len(matrix)/2)][int(len(matrix)/2)])
    return result
