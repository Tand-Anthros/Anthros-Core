from tools import represent, info, simple, stdinout, manager
import os, sys, copy, inspect, pyglet, time, configparser
sub_types = ['__name__', '__doc__', '__package__', '__loader__', '__spec__', '__file__', '__cached__', '__builtins__', 'represent', 'info', 'simple', 'stdinout', 'manager', 'os', 'sys', 'copy', 'inspect', 'pyglet', 'time', 'configparser']


class data:
	r'''Является временным представлением для данных в интересах оптимизации. Может быть преобразован в конечный, подробнее в функции get(). Не может быть представлен в виде файла'''
	def __init__(self, pos: 'path'):
	    pos = simple.smart_path(str(pos))
	    if pos == None: raise Exception('file does not exist')
	    pos = path(pos)
	
	    global types, sub_types
	    for i in sub_types:
	        try: types.pop(i)
	        except: pass
	
	    self.pos = pos
	    try: self.extens = pos.name().split('.')[1]
	    except: self.extens = ''
	
	    if self.extens in types.keys():
	        self.content = types[self.extens]
	    #elif self.extens in ['py', 'def', 'class']:
	    #    self.content = types['_' + self.extens]
	    else:
	        self.content = None
	
	def __str__(self):
	    return f'data.{type(self.content).__name__}.path("{self.pos}")'
	
	def __repr__(self):
	    return f'data.{type(self.content).__name__}.path("{self.pos}")'
	
	def get(self):
	    r'''Возвращает объект класса, который представляет. Если такого класса нет, вернёт сам себя'''
	    if self.content == None: return self
	    else: return self.content(self.pos)
	
	def name(self):
	    r'''возвращает имя файла'''
	    return self.pos.name()
	
	def type(self):
	    r'''возвращает тип объекта, который представляет'''
	    return self.content


class fold:
	r'''создаёт из папки объект, который можно использовать как словарь или как объект с атрибутами
	*Внимание, не будет корректно работать, если в одной папке будет два файла с одинаковым названием!'''
	def __init__(self, pos: 'path'): #Поправить недоработку с одинаковыми названиями
	    pos = simple.smart_path(str(pos))
	    if pos == None: raise Exception('folder does not exist')
	    pos = path(pos)
	    self.pos = pos
	
	    self.folders = dict()
	    self.files = dict()
	    for elem in os.listdir(str(self.pos)):
	            if os.path.isdir(str(self.pos + elem)):
	                self.folders[elem] = fold(self.pos + elem)
	            else:
	                self.files[elem.split('.')[0]] = data(self.pos + elem).get()
	
	def __path__(self):
	    return str(self.pos)
	
	def __call__(self):
	    return self.__dir__()
	
	def __str__(self):
	    return f'fold({", ".join(self.folders.keys())}, {", ".join(self.files.keys())})'
	
	def __dir__(self):
	    return list(self.folders.keys()) + list(self.files.keys())
	
	def __getattr__(self, attr):
	    if attr in self.folders.keys(): return self.folders[attr]
	    elif attr in self.files.keys(): return self.files[attr]
	    raise Exception('name not in fold')
	
	def __getitem__(self, item):
	    if item in self.folders.keys(): return self.folders[item]
	    elif item in self.files.keys(): return self.files[item]
	    raise Exception('name not in fold')
	
	def list(self):
	    out = []
	    for folder in self.folders.keys(): out.append(folder)
	    for file in self.files.keys(): out.append(file)
	    return out


class hts:
	def __init__(self, filename: 'path'):
		global types
		if type(filename).__name__ == 'path':
			filename = str(filename)
		if type(filename) != str:
			print("ERR: invalid parameter")
			
		file = open(filename, "r")
		dictionary = dict()
		
		dictionary['DEFAULT'] = ''
		category = 'DEFAULT'
		counter = 0
		line = file.readline()
		while(len(line) > 0):
			#commentary
			if line[0] == '#':
				pass
			#category
			elif line[0] == '[':
				category = ''
				for i in range(1, len(line)):
					if line[i] == ']':
						break
					else:
						category += line[i]
				dictionary[category] = ''
			#empty string
			elif line[0] == '\n':
				pass
			#filling dictionary
			elif category != '':
				key = line
				dictionary[category] += key
			#check for '=' symbol
			for i in range(len(line)):
				if line[i] == '=':
					has_symbol = True
			#check for commentaries
			for i in range(len(line)):
				if line[i] == '#' or line[i] == ';':
					has_commentaries = True
			line = file.readline()
		if (dictionary['DEFAULT'] == ''):
			del dictionary['DEFAULT']
		self.dictionary = dictionary
	
	def get_dict(self):
		return self.dictionary


class ini:
	r'''Представляет *.ini файлы, вы можете передать как строку из ini файла, так и расположение (обязательно *.path)'''
	def __init__(self, obj: ('str', 'path')):
	    self.start_pos = str(obj)
	    if simple.type(obj) == 'path' or simple.file_exist(str(obj)):
	        obj = manager.open_file(str(obj))
	
	    temp_pos = info.project_path() + simple.slash_os() + '__pycache__' + simple.slash_os() + 'temp.ini'
	    file = manager.save_file(temp_pos, obj, rewrite = True)
	
	    save_pos = simple.pos_switch(str(path(temp_pos) - 1))
	    read_conf = configparser.ConfigParser()
	    read_conf.read(temp_pos, encoding = 'utf-8')
	    simple.pos_switch(save_pos)
	
	    self.dict = dict()
	    for section in read_conf.keys():
	        _out = dict()
	        for key in read_conf[section].keys():
	            _out[key] = read_conf[section][key]
	        self.dict[section] = _out
	
	    manager.remove(temp_pos)
	
	def __getitem__(self, item):
	    return copy.deepcopy(self.dict[item])
	
	def __setitem__(self, item, value: 'dict'):
	    self.dict[item] = value
	
	def __file__(self):
	    out = ''
	    for section in self.dict.keys():
	        if section != 'DEFAULT': out += f'[{section}]\n'
	        for key in self.dict[section].keys():
	            out += f'{key} = {self.dict[section][key]}\n'
	    return out[:len(out) - 1]
	
	def __str__(self):
	    return str(self.dict)
	
	def pop(self, item):
	    return self.dict.pop(item)
	
	def base(self):
	    r'''Возвращает этот объект в виде двумерного словаря'''
	    return copy.deepcopy(self.dict)
	
	def save(self, path: ('str', 'path') = None, rewrite = False):
	    if not path: path = self.start_pos
	    manager.save_file(str(path), self.__file__(), rewrite = rewrite)
	
	def keys(self):
	    return self.dict.keys()
	
	def get(self, item):
	    return self.dict.get(item)


class mp3:
	def __init__(self, pos: 'path'):
	    pos = simple.smart_path(str(pos))
	    if pos == None: raise Exception('file does not exist')
	    pos = path(pos)
	    self.pos = pos
	
	    pj_pos = path(info.project_path())
	    ac_pos = path(info.ac_path())
	    try:
	        rel_pos = pos - pj_pos
	        sys_pos = pj_pos
	    except:
	        try:
	            rel_pos = pos - ac_pos
	            sys_pos = ac_pos
	        except: raise Exception('script relative location not found')
	
	    self.player = pyglet.media.Player()
	    self.sys_pos = sys_pos
	
	    save_pos = simple.pos_switch(str(sys_pos))
	    self.sound = pyglet.media.load(str(rel_pos))
	    self.player.queue(self.sound.get_queue_source())
	    simple.pos_switch(save_pos)
	
	def play(self):
	    self.player.play()
	
	def pause(self):
	    self.player.pause()
	
	def stop(self):
	    self.player.pause()


class path:
	r'''Является ссылкой на какой либо объект. Нужен для гибкой работы с пакетами и удобного редактирования ссылок, может быть представлен в виде файла, хотя для того и не расчитан'''
	import sys
	
	
	def __init__(self, var:('str', 'list')):
	    r'''Отвечает за создание класса'''
	    if type(var).__name__ == 'str':
	        _var = ['']
	        i = 0
	        for sb in var:
	            if sb not in ['\\', '/']:
	                _var[i] += sb
	            else:
	                _var.append('')
	                i += 1
	        var = _var
	
	    self.list = var
	
	
	def __str__(self):
	    r'''Отвечает за представление класса как строки'''
	    return simple.slash_os().join(self.list)
	
	
	def __repr__(self):
	    r'''Отвечает за строчное представление класса внутри массива'''
	    return '"' + simple.slash_os().join(self.list) + '"'
	
	
	def __len__(self):
	    r'''Возвращает длинну ссылки в виде числа (за единицу считается сам файл и каждый пакет в который он вложен)'''
	    return len(self.list)
	
	
	def __getitem__(self, var: 'int'):
	    r'''Возвращает название эллемента в цепочке ссылки'''
	    return self.list[var]
	
	
	def __add__(self, var: ('str', 'list', 'path')):
	    r'''Позволяет добавить эллемент в конец ссылки'''
	    if type(var).__name__ in ['str', 'list']: var = path(var)
	    return path(self.list + var.list)
	
	
	def __sub__(self, var:('int', 'str', 'list', 'path')):
	    '''Вычитает часть ссылки с конца, если не удасться, попытаеться вечесть с начала, иначе ошибка'''
	    if type(var).__name__ == 'int':
	        if var < len(self.list): return path(self.list[:len(self.list) - var])
	        else: raise Exception('path length is less than number passed')
	    if type(var).__name__ in ['str', 'list']: var = path(var)
	    var = copy.deepcopy(var).list
	    out = copy.copy(self.list)
	
	    if len(var) == 0 or len(var) == 1 and var[0] in ['']: return path(out)
	    if len(var) == 1:
	        try: out.pop(out.index(var[0]))
	        except:
	            raise Exception('the path does not contain the passed value')
	
	    out.reverse()
	    var.reverse()
	
	    i_out = 0
	    i_var = 0
	    while i_out < len(out):
	        if i_var == len(var) - 1: break
	        if out[i_out] == var[i_var]: i_var += 1
	        i_out += 1
	
	    if i_var + 1 != len(var):
	        raise Exception('the path does not contain the passed value')
	    i_var += 1
	
	    out = out[:i_out + 1 - len(var)] + out[i_out + 1:]
	    out.reverse()
	    return path(out)
	
	
	def name(self):
	    r'''возврщает имя файла'''
	    return self.list[len(self.list) - 1]


class txt:
	def __init__(self, pos: 'path'):
	    pos = simple.smart_path(str(pos))
	    if pos == None: raise Exception('folder does not exist')
	    pos = path(pos)
	
	    file = open(str(pos), 'r')
	    self.pos = pos
	    self.content = file.read()
	    file.close()
	
	def __call__(self, var):
	    return self.content
	
	def __str__(self):
	    return self.content
	
	def read(self):
	    return self.content


types = copy.copy(locals())

