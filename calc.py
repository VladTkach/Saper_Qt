
# check if cell in matrix
def is_cell(i, j, w, h):
    if 0 <= i < h and 0 <= j < w:
        return True
    else:
        return False

# calculate mines around cell
def calc_min(List, i, j, w, h, value):
    sum = 0
    if j + 1 < w:
        if List[i][j + 1] == value:
            sum += 1

    if j - 1 >= 0:
        if List[i][j - 1] == value:
            sum += 1

    if i + 1 < h:
        if List[i + 1][j] == value:
            sum += 1

    if i - 1 >= 0:
        if List[i - 1][j] == value:
            sum += 1

    if j + 1 < w and i + 1 < h:
        if List[i + 1][j + 1] == value:
            sum += 1

    if j - 1 >= 0 and i + 1 < h:
        if List[i + 1][j - 1] == value:
            sum += 1

    if j + 1 < w and i - 1 >= 0:
        if List[i - 1][j + 1] == value:
            sum += 1

    if j - 1 >= 0 and i - 1 >= 0:
        if List[i - 1][j - 1] == value:
            sum += 1

    return sum

# get coordinates by way
def get_index(i, j, way):
    match way:
        case 1:
            return i - 1, j
        case 2:
            return i - 1, j + 1
        case 3:
            return i, j + 1
        case 4:
            return i + 1, j + 1
        case 5:
            return i + 1, j
        case 6:
            return i + 1, j - 1
        case 7:
            return i, j - 1
        case 8:
            return i - 1, j - 1
