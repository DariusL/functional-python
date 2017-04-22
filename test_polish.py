import pytest

from polish import tokenize, tokenize_single, Operand, Operator, evaluate, do_operation, _evaluate


def test_empty():
    assert tokenize("") == []


def test_tokenize_whitespace_separated_list():
    string = "* / 15 - 7  + 1  1   3"
    expected = [
        Operator.multiply,
        Operator.divide,
        Operand(15),
        Operator.subtract,
        Operand(7),
        Operator.add,
        Operand(1),
        Operand(1),
        Operand(3)
    ]

    assert tokenize(string) == expected


@pytest.mark.parametrize(
    "str, token", [
        ("5", Operand(5)),
        ("0", Operand(0)),
        ("+", Operator.add),
        ("-", Operator.subtract)
    ])
def test_tokenize_single(str, token):
    assert tokenize_single(str) == token


def test_invalid_token():
    with pytest.raises(Exception):
        tokenize_single("f")


def test_string_evaluate_single():
    assert evaluate("5") == 5


def test_string_single_operation():
    assert evaluate("+ 5 5") == 10


@pytest.mark.parametrize(
    "operator, left, right, expected", [
        (Operator.add.value, 2, 2, 4),
        (Operator.subtract.value, 6, 2, 4),
        (Operator.divide.value, 16, 8, 2),
        (Operator.multiply.value, 9, 8, 72)
    ])
def test_operation(operator, left, right, expected):
    assert do_operation(operator, left, right) == expected


def test_sum_tuple():
    assert (5,) + (6,) == (5, 6)
    assert (5,) + tuple() == (5,)
    assert tuple() + tuple() == tuple()


def test_partition_list():
    assert [5, 6][1:] == [6]
    assert [5][1:] == []


def test_evaluate_single():
    assert _evaluate([Operand(5)]) == (Operand(5),)


def test_evaluate_pair():
    assert _evaluate([Operand(5), Operand(6)]) == (Operand(5), Operand(6))


def test_evaluate_operation():
    assert _evaluate([
        Operator.add, Operand(5), Operand(6)
    ]) == (Operand(11),)


@pytest.mark.parametrize(
    "expression, result", [
        ("+ 5 5", 10),
        ("5", 5),
        ("* / 15 - 7 + 1 1 + 2 + 1 1", 12),
        ("- 5 * 6 7", -37),
        ("* - 5 6 7", -7),
        ("* + 1 3 - 2 3", -4),
        ("* + 1 3 2", 8)
    ])
def test_acceptance(expression, result):
    assert evaluate(expression) == result
