import asyncio
import pytest

import python_trainee_assignment as pta


pytest_plugins = ('pytest_asyncio',)

EXAMPLE_MATRIX_FROM_URL = (
    '+-----+-----+-----+-----+\n'
    '|  10 |  20 |  30 |  40 |\n'
    '+-----+-----+-----+-----+\n'
    '|  50 |  60 |  70 |  80 |\n'
    '+-----+-----+-----+-----+\n'
    '|  90 | 100 | 110 | 120 |\n'
    '+-----+-----+-----+-----+\n'
    '| 130 | 140 | 150 | 160 |\n'
    '+-----+-----+-----+-----+\n'
)
EXAMPLE_MATRIX_AS_LIST = [
    [10, 20, 30, 40],
    [50, 60, 70, 80],
    [90, 100, 110, 120],
    [130, 140, 150, 160]
]
TRAVERSAL = [
    10, 50, 90, 130, 140, 150, 160, 120, 80, 40, 30, 20, 60, 100, 110, 70
]
SOURCE_URL = (
    'https://raw.githubusercontent.com/'
    'avito-tech/python-trainee-assignment/main/matrix.txt'
)


def test_get_data_by_url(mocker):
    mocker.patch(
        'aiohttp.ClientSession.post', return_value=EXAMPLE_MATRIX_FROM_URL
    )
    with open('test_matrix.txt') as matrix_file:
        matrix: str = matrix_file.read()
    assert asyncio.run(pta._get_data_by_url(SOURCE_URL)) == matrix


@pytest.mark.parametrize(
    'test_param, result',
    (
        (EXAMPLE_MATRIX_FROM_URL, EXAMPLE_MATRIX_AS_LIST),
        ('+---+\n| 1 |\n+---+', [[1]]),
        ('+---+---+\n| 1 | 2 |\n+---+---+', [[1, 2]]),
        (
            '+---+---+\n| 1 | 2 |\n+---+---+\n| 3 | 4 |\n+---+---+',
            [[1, 2], [3, 4]]
        )
    )
)
def test_convert_str_matrix_to_list_matrix(test_param, result):
    assert pta._convert_str_matrix_to_list_matrix(test_param) == result


@pytest.mark.parametrize(
    'test_param, result',
    (
        (EXAMPLE_MATRIX_AS_LIST, TRAVERSAL),
        ([[1, 2], [3, 4]], [1, 3, 4, 2]),
        ([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [1, 4, 7, 8, 9, 6, 3, 2, 5]),
        ([[1]], [1]),
        (
            [
                [1, 2, 4, 5, 6],
                [7, 8, 9, 10, 11],
                [12, 13, 14, 15, 16],
                [17, 18, 19, 20, 21],
                [22, 23, 24, 25, 26]
            ],
            [
                1, 7, 12, 17, 22,
                23, 24, 25, 26, 21,
                16, 11, 6, 5, 4,
                2, 8, 13, 18, 19,
                20, 15, 10, 9, 14
            ]
        )
    )
)
def test_travers_matrix(test_param, result):
    assert pta._travers_matrix(test_param) == result


@pytest.mark.parametrize(
    'test_param, wait_result',
    (
        ([[1, 2]], False),
        (EXAMPLE_MATRIX_AS_LIST, True),
        ([[1, 2], [2, 3]], True),
        ([[1]], True)
    )
)
def test_is_matrix_is_squared(test_param, wait_result):
    assert pta._is_matrix_squared(test_param) == wait_result


def test_get_matrix():
    assert asyncio.run(pta.get_matrix(SOURCE_URL)) == TRAVERSAL
