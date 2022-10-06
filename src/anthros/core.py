from interfaces import console, clickermann
from tools import assembly, info, manager, represent, simple, stdinout, convert
import os, sys, threading, copy, time

r'''
Цели для выполнения АС:
[Tand]
    - Доделать документацию по АС
    - Перевести доки на английский
    - Разработать систему скриптинга АС
    - Сделать систему тестов
    - Добавить args и dir первой командой или что то с этим придумать
    - Починить tools.info.args
    - Реализовать subs
    - Нужно что то придумать с ошибками
    - Добавить установку сторонних библиотек с подтверждением пользователя или убрать pyglet
    - Реализовать тесты для АС
[Net-Panner]
    - Релазивать парсер блоков (Парсер, создающий единую строку из блока, записывающий множество этих блоков в список)
    - Реализовать парсер Инкриментов (Парсер достающий информацию из строки по начальному и конечному инкременту, должен возвращать список с отделённым эллементом)
    - Сделать extens ini.class
'''

#=> [['[Tand]', '- Доделать документацию по АС', ...], ['[Net-Panner]', '- Сделать extens ini.class', '...'], ...]

class help():
    __doc__ = manager.open_file(simple.slash_os().join([info.ac_path(), 'docs', 'rus', 'help.md']))

    def __init__(self, pos: 'list' = [], test = 123):
        self.pos = pos

    def __call__(self):
        global help
        temp = simple.slash_os().join([info.ac_path(), 'docs', 'rus'] + self.pos) + '.md'
        if self.pos == []: return help.__doc__
        elif simple.file_exist(temp):
            return manager.open_file(temp)
        else:
            global ac
            _ac = ac()
            return sub.goto_attr(_ac, self.pos).__doc__

    def __getattr__(self, attr: 'str'):
        global help
        out = help(self.pos + [attr])
        return out

class tools():
    r'''Компонент tools, даже неандертальцы не могли жить без инструментов
*Документация написана для разработчиков на python, тк поддержка других языков будет добавлена позже
Является модулем с набором функций и собственной структурой. Не может иметь зависимости от других компонентов ac

Дополнения для пользователей, вы можете устанавливать стороние tools, созданные другими людьми, просто положите их
в папку tools у себя в проекте или же измените это расположение в manifst, введите: help manifest
использовать естественно вы можете их выполнив: ac.tools.name.function; введя: tools name function

Дополнения для разработчиков, не импортируйте не чего из ас, кроме других tools! Это очень строгое правило
Так же вы можете использовать сторонние пакеты для ваших инструментов,
 но с их установкой и решения вопросов лецензии вы берёте на свои плечи
Выше, не зря было сказанно модуль, любой tools должен быть модулем, и крайне не желательно
 расширять это в нечто большее, все же инструменты это односложные функции,выполняющие конкретную задачу
 для большего используйте interfaces и apps'''
    def __init__(self):
        import tools

        self.modules = []
        for elm in dir(tools):
            temp = getattr(tools, elm)
            if simple.type(temp) == 'module':
                self.modules.append(temp)

        self.functions = []
        for module in self.modules:
            for elm in dir(module):
                temp = getattr(module, elm)
                if simple.type(temp) == 'function':
                    self.functions.append(temp)

    def __call__(self):
        return self.__dir__()

    def __dir__(self):
        out = []
        for name in self.modules:
            out.append(name.__name__.split('.')[1])
        return out

    def __getattr__(self, attr):
        #Надо добавить проверку типа передаваймых аргументов
        #for function in self.functions:
        #    if attr == function.__name__:
        #        return function

        for module in self.modules:
            if 'tools.' + attr == module.__name__:
                return module

        raise Exception('no module with this name')

    def echo(self, *args):
        r'''Возвращает написанное. Нужен для прсмотр содержания в переменных или для создания переменной вручную'''
        if len(args) == 1: return args[0]
        else: return args

class extens():
    r'''Компонент extens, почему бы нам не использовать тот мяч, как ключ шифрования?
Является классом, представляющий переданную строку или файл в виртуальном виде
*Да да мы поддерживаем пока что только python, документация расчитана под него

Наверное, всеравно может звучать непонятно, по крайней мере для разработчика. Как это я должен представить
Строку или файл в виртуальном виде? Чтож, extens не зря являются классами
При инициализации, метод __init__, вы должны как то распорядится с сылкой на файл или с переданной строкой
Причем переданая строка может быть как в юникоде, так и в байткоде
После чего создаётся объект класса, которым уже пользуется тот, кто использует ваш extens
Этот объект будет работать так, как вы сами зададите в своём классе

В дополнение можно сказать, что вы так же можете использовать компонент tools, а так же сторонние пакеты
но как и в случае с tools, все проблемы с установкой и лицензиями вы берёте на себя

Что же касается пользователей extens, как правило, вам не нужно о них задумаваться, так как вы можете: ac.project.file
Если же файл находится вне вашего проекта или вы получили сырую строку для обработки, то вы можете
выполнить: ac.extens.name(link)'''
    def __init__(self):
        r'''Возвращает все объекты расширений из папки extens, в виде словаря
        *Внимание! Компонент будет работать правильно только после запуска core.run()'''
        represent.class_def_comp(info.ac_path() + simple.path_os('/extens'), encoding='cp1251')
        save_pos = simple.pos_switch(info.ac_path())

        import extens
        folder = represent.fold_dict(info.ac_path() + simple.path_os('/extens'))
        separ = {'str': str, 'int': int}
        for elem in folder:
            if simple.type(elem) == 'str':
                name = simple.path_name(elem)
                if '.class' in name:
                    name = name.split('.')[0]
                    separ[name] = getattr(extens, name)

        simple.pos_switch(**save_pos)
        self.separ = separ

    def __call__(self):
        return self.__dir__()

    def __getitem__(self, key):
        return self.separ[key]

    def __getattr__(self, attr):
        return self.separ[attr]

    def __dir__(self):
        return list(self.separ.keys())

    def keys(self):
        return self.separ.keys()

class interfaces():
    r'''Компонент interfaces, не смогли соединить hdmi с водой? Тогда вы просто не нашли достаточно хороший переходник
Является пакетом, с модулем __init__.py, который задаёт будущее поведение

Начнём с пользователей. С вами все просто. Установите нужный пакет в папку interfaces или другую, укажите в manifest
После берём ac и выполняем: ac.interfaces.name.module.function
Это всё. Большее узнавайте у разработчика интерфейса, структура тут сугубо индивидулаьная
Попробуйте: help interfaces name; или выполните: help.interfaces.name()

Чтож, а теперь разработчики. Относитесь к интерфейсам как к apps, только их цель предоставить возможность
объединить два взаимодействия. Ну к примеру, выполнение кода и нажатие на кнопку пользователем
Как вы будете это реализовывать, лишь ваша фантазия, но постарайтесь максимально доступно объяснить
вашим пользователям, как это работает. Сделайте документацию или сайт при надобности
Вы можете использовать сторонние пакеты, лицензия и установка на вашей совести'''
    def __init__(self):
        pass

    def __call__(self):
        return self.__dir__()

    def __getattr__(self, attr):
        if attr == 'console': return console
        elif attr == 'clickermann': return clickermann

    def __dir__(self):
        return ['console', 'clickermann']

class sub(): #Переработать в сестему методов с возможностью модификации
    r'''Вспомогательный класс для работы core и tools. Он не расчитан для личного использования, но вы все ещё можете им воспользоватся'''
    comand_pars_args = ('tuple', 'list')
    def command_pars(line: 'str', auto_var: comand_pars_args):
        r'''Принимает сырую строку от пользователя и делит её на список, после чего вставляет переменные
        *auto_var это список, содержащий в себе переменные, вставляются по правилу, самое последние значние в списке auto_var первое'''
        command = line.split(' ')
        global return_value

        i_cmd = 0
        while i_cmd < len(command):
            i = 0
            lenght = 0
            while i < len(command[i_cmd]):
                if command[i_cmd][i] == '_': lenght += 1
                else:
                    lenght = 0
                    break
                i += 1

            if lenght > 0:
                if auto_var and lenght <= len(auto_var): command[i_cmd] = auto_var[len(auto_var) - lenght]
                else:
                    try: raise Exception('no saved variables')
                    except:
                        return stdinout.exception(sys.exc_info())
            i_cmd += 1

        return command

    def indent_offset(command):
        r'''Считает смещение для команды и возвращает число'''
        out = 0
        while out < len(command):
            if command[out] == '': out += 1
            else: break
        return out

    def attr_offset(obj, command):
        r'''Автоматический определяет момент перехода от атрибутов к аргументов в команде. возращает массив с атрибутами
        *Можно явно указать переход, поставив дополнительный пробел
        *Принимает любой атрибут для объектов с методом __getattr__'''
        global return_value
        index = None
        if '' in command:
            index = command.index('')
            if '' in command[:index]:
                try: raise Exception('odd space')
                except:
                    return stdinout.exception(sys.exc_info())
            command = command[:index]

        i = 0
        out = []
        while i < len(command):
            if simple.type(obj) == 'exception': return obj
            try:
                obj = getattr(obj, command[i])
            except:
                exc = stdinout.exception(sys.exc_info())
                if index:
                    return exc #Нет пояснения ошибки
                elif exc.exception() == 'Exception':
                    return exc #Вероятно может задействовать и другие ошибки, кроме отлаживаемых
                break
            out.append(command[i])
            i += 1
        return out

    def filter(command):
        r'''Удаляет вообще все пустые строки("") из комманды'''
        out = []
        for elm in command:
            if elm not in ['']: out.append(elm)
        return out

    def types_obj(obj):
        r'''Создаёт словарь со списком названий типов переменных, требуемых для вызова переданного объекта
        *Если в анотации переменной больше одной переменной запишет список на её месте
        *Если объект принимает *args и/или **kwargs, укажет "*args", "**kwargs" в конце списка'''
        args = info.args(obj)
        out = {'args': [], 'kwargs': {}, '*args': None, '**kwargs': None}

        for arg in args['args']:
            if simple.type(arg['ann']) in ['str', 'list', 'tuple']:
                if arg['def'] == None: out['args'].append(arg['ann'])
                else: out['kwargs'][arg['name']] = arg['ann']
            else:
                if arg['def'] == None: out['args'].append('str')
                else: out['kwargs'][arg['name']] = 'str'

        if args['*args'] and args['*args']['ann'] in ['str', 'list', 'tuple']: out['*args'] = args['*args']['ann']
        elif args['*args'] and args['*args']['ann'] == None: out['*args'] = 'str'

        if args['**kwargs'] and args['**kwargs']['ann'] in ['str', 'list', 'tuple']: out['**kwargs'] = args['**kwargs']['ann']
        elif args['**kwargs'] and args['**kwargs']['ann'] == None: out['**kwargs'] = 'str'

        return out

    def types_vars(args, kwargs, types):
        r'''Подготавливает args и kwargs для конвертации в типы указанные в словаре types
        *Непостоянные аргументы, переданные не в словаре, будут вставлены подряд в незанятыми словарём переменные'''
        if len(types['args']) > len(args):
            try: raise Exception('not enough arguments passed')
            except: return stdinout.exception(sys.exc_info())
        if kwargs == None: kwargs = dict()

        _args = []
        temp_kwargs = []
        _types = copy.deepcopy(types['args'])
        if types['*args'] == None:
            temp_kwargs = args[len(types['args']):]
            args = args[:len(types['args'])]
        else:
            _types += [types['*args'] for i in range(len(types['args']), len(args))]
        for i in range(0, len(_types)):
            _args.append(dict(value = args[i], type = _types[i]))

        if types['kwargs'] == None: types['kwargs'] == dict()
        if types['**kwargs'] == None and len(kwargs) + len(temp_kwargs) > len(types['kwargs']):
            try: raise Exception('extra positional arguments')
            except: return stdinout.exception(sys.exc_info())
        _kwargs = []
        for kwarg in types['kwargs'].keys():
            if kwargs.get(kwarg) != None:
                _kwargs.append(dict(value = kwargs.pop(kwarg), type = types['kwargs'][kwarg]))
            elif len(temp_kwargs) > 0:
                _kwargs.append(dict(value = temp_kwargs.pop(0), type = types['kwargs'][kwarg]))
        if types['**kwargs']:
            for key in kwargs.keys():
                _kwargs.append(dict(name = key, value = kwargs.pop(key), type = types['**kwargs']))
            for i in range(0, len(temp_kwargs)):
                _kwargs.append(dict(name = str(i), value = temp_kwargs[i], type = types['**kwargs']))
        elif len(kwargs) > 0 or len(temp_kwargs) > 0:
            try: raise Exception('too many arguments')
            except: stdinout.exception(sys.exc_info())

        return dict(args = _args, kwargs = _kwargs)

    def convert_var(value, type):
        r'''Конвертирует переменную в указанный тип. Для конветрации использует extens'''
        global _ac_extens
        _extens = _ac_extens()
        if simple.type(type) == 'str': type = [type]
        elif simple.type(type) in ['tuple', 'list']: pass
        else:
            try: raise Exception('invalid annotation type, must be: str, tuple or list')
            except: return stdinout.exception(sys.exc_info())

        _excepts = []
        for _type in type:
            if simple.type(value) == _type:
                return value
            elif _type in ['_class', 'class']:
                return value
            else:
                try: return getattr(_extens, _type)(value)
                except: _excepts.append(stdinout.exception(sys.exc_info()))

        if _excepts == []:
            try: raise Exception('failed to convert')
            except: return stdinout.exception(sys.exc_info())
        else:
            return _excepts[0]  # Доработать эту ошибку, что бы могло передавать сразу все или выбирала наиболее подходящую

    def convert_vars(args, kwargs):
        r'''Принимает два списка с переменными и возвращает готовый сконвертированный *args и **kwargs'''
        _args = []
        _kwargs = {}
        temp = None

        for arg in args:
            temp = sub.convert_var(arg['value'], arg['type'])
            if simple.type(temp) == 'exception': return temp
            else: _args.append(temp)
        for kwarg in kwargs:
            temp = sub.convert_var(kwarg['value'], kwarg['type'])
            if simple.type(temp) == 'exception': return temp
            else:
                if 'name' in kwarg.keys():
                    _kwargs[kwarg['name']] = temp

        return dict(args = _args, kwargs = _kwargs)

    def goto_attr(obj, attrs):
        r'''Принимает объект и список атрибутов, возвращает объект являющийся смещением по аттрибутам от основного объекта'''
        for attr in attrs: obj = getattr(obj, attr)
        return obj

class ac():
    r'''Выступает в роли окружения, из этого объекта вы можете вызвать свои файлы или tools, extens, interfaces
    *Сейчас AC воспринимает только "абсолютные пути атрибутов", но в будущем вы сможете использовать сокращения'''
    def __init__(self):
        save_pos = simple.pos_switch(stdinout.var('pj_pos', namespace='__ac__'))
        global _ac_extens, _ac_tools, _ac_interfaces, help
        #if type(help()).__name__ != 'list': help = help()
        _extens, _tools, _interfaces, _help = _ac_extens(), _ac_tools(), _ac_interfaces(), help()

        self._ac_project = _extens.fold(stdinout.var('pj_pos', namespace = '__ac__'))
        self._ac_tools = _tools
        self._ac_extens = _extens
        self._ac_interfaces = _interfaces
        self.help = _help
        simple.pos_switch(**save_pos)

    def __getattr__(self, attr):
        if attr == 'tools': return self._ac_tools
        if attr == 'extens': return self._ac_extens
        if attr == 'interfaces': return self._ac_interfaces
        if attr == 'project': return self._ac_project
        if attr == 'help': return self.help

        raise Exception('project environment does not have this attribute')

    def __dir__(self):
        out = []
        r'''for elm in dir(self._ac_project):
            if len(elm) == 1:
                out.append(elm)
            elif len(elm) >= 2 and elm[:2] != '__':
                out.append(elm)'''
        return ['tools', 'extens', 'interfaces', 'help', 'project'] + out

class core():
    r'''Возвращает экземпляр core. Не желательно создавать этот экземпляр самостоятельно, воспользуйтесь anthros.core.run()'''
    def __init__(self):
        self.env = ac()
        self.auto_var = []

    def __getattr__(self, attr):
        return getattr(self.env, attr)
    
    command_args = ('str', 'list')
    def command(self, command: command_args, kwargs: 'dict' = None):
        r'''Выполняет команду по правилам AC
        *Если будет аннотация, не содержащаяся в папке extens, тогда переменная будет переданна как строка'''
        obj = self.env

        if command in ['', []]: #перенести в mods
            return dir(obj)

        command = sub.command_pars(command, self.auto_var)
        if simple.type(command) == 'exception': return command

        indent = sub.indent_offset(command)
        command = command[indent:]

        if simple.type(command[0]) == 'str': obj = self.env
        else:
            obj = command[0]
            command = command[1:]

        attrs = sub.attr_offset(obj, command)
        if simple.type(attrs) == 'exception': return attrs
        for attr in attrs: obj = getattr(obj, attr)

        if len(command) > 0 and command[len(command) - 1] == '':
            self.auto_var.append(obj)
            return obj

        args = sub.filter(command[len(attrs):])
        if simple.type(obj) == 'exception': return obj

        types = sub.types_obj(obj)
        if simple.type(types) == 'exception': return types

        vars = sub.types_vars(args, kwargs, types)
        if simple.type(vars) == 'exception':
            if str(vars.description()) == 'not enough arguments passed': return vars
            return vars

        args = sub.convert_vars(vars['args'], vars['kwargs'])
        if simple.type(args) == 'exception': return args

        try: return_value = obj(*args['args'], **args['kwargs'])
        except:
            err = stdinout.exception(sys.exc_info())
            if 'object is not callable' in str(err.description()) and '\'NoneType\'' not in str(err.description()): return info.attrs(obj)
            return err

        if return_value != None: self.auto_var.append(return_value)
        return return_value

    def exit(self):
        r'''Завершает работу АС и удаляет все временные файлы'''
        represent.temp_py_clear()

def __getattr__(attr):
    global core
    return getattr(core, attr)

_ac_interfaces = interfaces
_ac_extens = extens
_ac_tools = tools

del interfaces, extens, tools
core = core()