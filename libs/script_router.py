import b_msg
from libs import util, error_handel
from scriptes import scriptes
import pkgutil
import os
import imp
import sys

ABSOLUTE_BASE_PATH = scriptes.__path__[0]


def get_function_parse(file_name, funName):
    try:
        pkgPath = "{}{}".format(ABSOLUTE_BASE_PATH, file_name)
        newPkg = imp.load_source(pkgPath, pkgPath)
        del sys.modules[pkgPath]
        if 'Instance' in newPkg:
            new_package_instance = newPkg.Instance()
            basePath = file_name.replace(".py", '')
            if funName in dir(new_package_instance) and funName[0] != '_':
                return [{
                    "uri": "{}/{}".format(basePath, funName),
                    "data": util.format_script_info_data(getattr(new_package_instance, funName))
                }]
            else:
                return []
        else:
            return []
    except Exception as e:
        raise e


def get_package_parse(file_name):
    # 初始化对象
    absolute_file_path = "{}{}".format(ABSOLUTE_BASE_PATH, file_name)
    new_package_instance = None
    attr_list = []
    base_path = file_name.replace(".py", '')
    # 动态加载package
    try:
        new_pkg = imp.load_source(file_name, absolute_file_path)
        new_package_instance = new_pkg.Instance()
        # 删除掉临时模块
        del sys.modules[file_name]
    except Exception as e:
        error_log = error_handel.log_traceback(e)
        attr_list.append({
            "is_error": True,
            "file_name": file_name,
            "error_msg": error_log
        })
    # 加载完成后返回
    for name in dir(new_package_instance):
        if name[0] != '_':
            # 获取所有方法
            attr_list.append({
                "uri": "{}/{}".format(base_path, name),
                "data": util.format_script_info_data(getattr(new_package_instance, name))
            })
    return attr_list


def get_py_file_list(current_path):
    dirs = []
    path = current_path
    # split这个路径，然后一层一层检查
    full_path = "{}{}".format(ABSOLUTE_BASE_PATH, current_path)
    if os.path.isdir(full_path):
        # 是文件夹
        dirs = os.listdir(full_path)
    elif not os.path.isfile(full_path):
        # 是文件，但不是py文件
        if os.path.isfile("{}.py".format(full_path)):
            # 是文件
            path_splite_list = current_path.split('/')
            if len(path_splite_list) > 1:
                path_file_name = path_splite_list[-1]
                path = '/'.join(path_splite_list[0:-1])
                dirs = ["{}.py".format(path_file_name)]
        else:
            # 是对象。
            path_splite_list = current_path.split('/')
            if len(path_splite_list) > 2:
                path_function_name = path_splite_list[-1]
                path_splite_list[-2] = "{}.py".format(path_splite_list[-2])
                path_file_name = '/'.join(path_splite_list[0:-1])
                return get_function_parse(path_file_name, path_function_name)
    data = []
    for file_name in dirs:
        if file_name != '__pycache__' and file_name != '__init__.py':
            file_path = "{}/{}".format(path, file_name)
            if ".py" in file_name:
                # 具体的package包
                for fun_attr in get_package_parse(file_path):
                    data.append(fun_attr)
            else:
                items = get_py_file_list(file_path)
                for item in items:
                    data.append(item)
    return data


def get_file_label_and_path(file_name):
    absolute_file_path = "{}{}".format(ABSOLUTE_BASE_PATH, file_name)
    new_package_instance = None
    attr_list = []
    base_path = file_name.replace(".py", '')
    try:
        new_pkg = imp.load_source(file_name, absolute_file_path)
        new_package_instance = new_pkg.Instance()
        # 删除掉临时模块
        del sys.modules[file_name]
    except Exception as e:
        error_log = error_handel.log_traceback(e)
        attr_list.append({
            "label": "解析失败",
            "path": file_name,
            "is_error": True,
            "file_name": file_name,
            "error_msg": error_log
        })
    for name in dir(new_package_instance):
        if name[0] != '_':
            # 获取所有方法
            attr_list.append({
                "label": name,
                "path": "{}/{}".format(base_path, name)
            })
    return attr_list


def get_folder_deep_map(current_path):
    # 判断path是folder还是file还是fun
    path = current_path
    if path[-1] == '/':
        path = path[0:-1]
    dirs = []
    current_path_splite_list = path.split('/')
    mapItem = []
    if os.path.isdir("{}{}".format(ABSOLUTE_BASE_PATH, path)):
        # 是文件夹
        dirs = os.listdir("{}/{}".format(ABSOLUTE_BASE_PATH, path))
    elif os.path.isfile("{}/{}.py".format(ABSOLUTE_BASE_PATH, path)):
        # 是文件,就到这一层结束，不再继续下探
        dirName = current_path_splite_list[-1]
        return [{
            'label': dirName,
            'path': path,
            'children': get_file_label_and_path("{}.py".format(path))
        }]
    else:
        # 是对象。这个比较难办。
        return []
    for dirName in dirs:
        if dirName != '__pycache__' and dirName != '__init__.py':
            label = dirName.replace('.py', '')
            newItem = {
                'label': label,
                'path': "{}/{}".format(path, label),
                'children': []
            }
            if ".py" in dirName:
                newItem['children'] = get_file_label_and_path(
                    "{}/{}".format(path, dirName))
            elif not ("." in dirName):
                # 这是folder, 需要下探
                newItem['children'] = get_folder_deep_map(
                    "{}/{}".format(path, dirName))
            else:
                continue
            mapItem.append(newItem)
    return mapItem


def get_package_by_path(methodList, deep=1):
    if deep > len(methodList):
        return False
    path = "{}/{}".format(ABSOLUTE_BASE_PATH, "/".join(methodList[0:deep]))
    if os.path.isdir(path):
        return get_package_by_path(methodList, deep + 1)
    elif os.path.isfile("{}.py".format(path)):
        pkgPath = "{}.py".format(path)
        try:
            mod = imp.load_source(pkgPath, pkgPath)
            del sys.modules[pkgPath]
            return mod
        except Exception as e:
            raise Exception(e)
    else:
        return False


def get_method_list_split(method_str: str):
    method_list = method_str.split('/')
    if method_list[0] == '':
        del method_list[0]
    return method_list


class Route():
    def apply(self, _request_data):
        method_list = get_method_list_split(_request_data['method'])
        module_obj = get_package_by_path(method_list)
        if module_obj != False:
            instance = module_obj.Instance()
            if hasattr(instance, method_list[-1]):
                fun_instance = getattr(instance, method_list[-1])
                return fun_instance(**_request_data["methodParams"])
        return b_msg.error(msg='无此方法: {}'.format(_request_data['method']), print_logger=True)

    def get_scripts_list(self, param):
        root_path = param['rootPath'] or ''
        if root_path == '' or root_path == '/':
            root_path = ''
        uri_list = get_py_file_list(root_path)
        return uri_list

    def get_scripts_tree(self, param):
        root_path = param['rootPath'] or ''
        if root_path == '' or root_path == '/':
            root_path = '/'
        uri_tree = get_folder_deep_map(root_path)
        return uri_tree
