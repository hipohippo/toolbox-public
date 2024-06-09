from typing import Union

multiplier = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
end_map = {}
end_map.update({0: "1", 1: "0", 2: "X"})
end_map.update({v: str(12 - v) for v in range(3, 11)})


def validate_id(id: str):
    return fill_last_digit(int(id[:-1])) == id[-1]


def fill_last_digit(idfirst17: Union[str, int]):
    idfirst17 = int(idfirst17)
    ecc_code = 0
    for i in range(len(multiplier)):
        ecc_code += (idfirst17 % 10) * multiplier[-(i + 1)] % 11
        idfirst17 //= 10
    return end_map[ecc_code % 11]


if __name__ == "__main__":
    validate_id("110101199001010103")
    fill_last_digit("11010119900101010")
