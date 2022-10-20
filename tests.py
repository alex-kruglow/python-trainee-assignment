import asyncio
import pytest

import python_trainee_assignment as pta


pytest_plugins = ('pytest_asyncio',)

EXAMPLE_MATRIX_FROM_URL = (
    '+-----+-----+-----+-----+'
    '|  10 |  20 |  30 |  40 |'
    '+-----+-----+-----+-----+'
    '|  50 |  60 |  70 |  80 |'
    '+-----+-----+-----+-----+'
    '|  90 | 100 | 110 | 120 |'
    '+-----+-----+-----+-----+'
    '| 130 | 140 | 150 | 160 |'
    '+-----+-----+-----+-----+'
)
EXAMPLE_MATRIX_AS_LIST = [
    [10, 20, 30, 40],
    [50, 60, 70, 80],
    [90, 100, 110, 120],
    [130, 140, 150, 160]
]
SUCCESS_RESULT = [
    10, 50, 90, 130, 140, 150, 160, 120, 80, 40, 30, 20, 60, 100, 110, 70
]
URL_FOR_CHECKING = (
    'https://raw.githubusercontent.com/'
    'avito-tech/python-trainee-assignment/main/matrix.txt'
)


@pytest.mark.asyncio
async def test_get_data_by_url(mocker):
    mocker.patch(
        'aiohttp.ClientSession.get', return_value=EXAMPLE_MATRIX_FROM_URL
    )

    response: str = asyncio.run(pta._get_data_by_url(URL_FOR_CHECKING))
    assert response == EXAMPLE_MATRIX_FROM_URL


@pytest.mark.parametrize(
    'test_param, result',
    (
        (EXAMPLE_MATRIX_FROM_URL, EXAMPLE_MATRIX_AS_LIST),
        ('+---+\n| 1 |\n+---+', [1]),
        ('+---+---+\n| 1 | 2 |\n+---+---+', [1, 2])
    )
)
def test_convert_str_matrix_to_list_matrix(test_param, result):
    assert pta._convert_str_matrix_to_list_matrix(test_param) == result


@pytest.mark.parametrize(
    'test_param, result',
    (
        (EXAMPLE_MATRIX_AS_LIST, SUCCESS_RESULT),
        ([1, 2], []),
        ([[1, 2], [3, 4]], [1, 3, 4, 2]),
        ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [1, 4, 7, 8, 9, 6, 3, 2, 5])
    )
)
def test_travers_matrix(test_param, result):
    assert pta._travers_matrix(test_param) == result
