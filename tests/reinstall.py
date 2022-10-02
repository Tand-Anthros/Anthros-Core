from anthros import core as ac

info = ac.tools.info
simple = ac.tools.simple
manager = ac.tools.manager

if 'Создание временных __init__.py':
    actual_ac = info.project_path().split(simple.slash_os())
    actual_ac = simple.slash_os().join(actual_ac[:len(actual_ac) - 1] + ['src', 'anthros'])

    fold_dict_ac = manager.fold_dict(actual_ac)
    module_suicide = 'import os\nos.remove(__file__)'

    def dict_sort(value: dict):
        out = dict()
        for key in value.keys():
            if simple.type(value[key]) == 'dict':
                out[key] = dict_sort(value[key])
            elif simple.type(value[key]) == 'str' and simple.file_exist(value[key]) == 'folder' and '__pycache__' not in value[key]:
                temp = value[key] + simple.slash_os() + '__init__.py'
                if simple.file_exist(temp) != 'file':
                    manager.save_file(temp, module_suicide)

    dict_sort(fold_dict_ac)

if 'Переустановка AC':
    path = ac.extens.path(__file__) - 2

    try: manager.remove(str(path + f'src/anthros_core.egg-info'))
    except: pass
    fold = ac.tools.represent.fold_dict(str(path + 'dist'))
    for key in fold.keys():
        if '.whl' in key: manager.remove(fold[key])

    if ac.tools.assembly.create_whl(str(path)) != 0: exit()

    fold = ac.tools.represent.fold_dict(str(path + 'dist'))
    for key in fold.keys():
        if '.whl' in key: ac.tools.assembly.install_package(fold[key])