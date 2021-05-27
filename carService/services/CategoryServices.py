from carService.models import Category


def get_category_path(category: Category, path: str):
    category_parent = category.parent
    if category_parent:
        path = path + '>' + category_parent.name
        if category_parent.parent:
            return get_category_path(category_parent, path)

    return path


def get_category_arr(category: Category, path: []):
    if category.name not in path:
        path.append(category.name)
    category_parent = category.parent
    if category_parent:
        path.append(category_parent.name)
        if category_parent.parent:
            return get_category_arr(category_parent, path)


    return path


def get_path_from_arr(path: []):
    path_string = ''

    for i in reversed(path):
        if path_string == '':
            path_string = i
        else:
            path_string = path_string + '-->' + i

    return path_string
