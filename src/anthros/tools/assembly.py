from tools import simple
import os

def install_package(name: 'str', sys_out: 'bool' = True): #Вместо --force-reinstall сделать полноценное удаление и установку
    r'''Устанавливает переданный пакет, может работать как с *.whl так и устанавливать пакет по имени с интернета
    *Если вернёт 0 значит что всё прошло успешно
    *При sys_out False, не подавляет вывод полностью. Ошибки и предупреждения всеравно видны'''
    #exec('import wafdwafd') #сделать проверку импортами, перед загрузкой
    if sys_out: out = os.system(f'pip install {name} --force-reinstall')
    else: out = os.system(f'pip install {name} -q --force-reinstall')
    return out

def uninstall_package(name: 'str', sys_out: 'bool' = True):
    r'''Удаляет указанные пакет из системы
    *Если вернёт 0 значит все прошло успешно
    *При sys_out False подавляет системыный вывод'''
    if sys_out: out = os.system(f'pip uninstall {name}')
    else: out = os.system(f'pip uninstall {name} -q')
    return out

def create_whl(pj_path: 'str'):
    r'''Создаёт *.whl пакет из вашего проекта(папка с src и setup.cfg), который после можно установить с помощью pip
    *Если вернёт 0 значит что всё прошло успешно
    *Данная функция использует SetupTools, для дополнительной информации обратитесть к: https://setuptools.pypa.io/en/latest/userguide/quickstart.html'''
    save_pos = simple.pos_switch(pj_path)
    out = os.system('py -m build')
    simple.pos_switch(save_pos)
    return out