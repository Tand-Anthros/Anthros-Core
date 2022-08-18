r'''Пожалуйста используйте исключительно anthros.core, модуль не расчитан на его использование через anthros или
anthros.tools и тд.
*Для документации пожалуйста обратитесть к: anthros.core.help()'''
import  sys
if sys.platform in ['win32']: sb = '\\'
else: sb = '/'
_path = __file__
_path = _path.split(sb)
_path = _path[:len(_path) - 1]
_path = sb.join(_path)

save_path = sys.path[0]
sys.path[0] = _path
from tools import stdinout, info, simple, manager
if simple.file_exist(_path + simple.path_os('/extens/__init__.py')): manager.remove(_path + simple.path_os('/extens/__init__.py'))
if save_path == '' or save_path == info.ac_path(): stdinout.var('pj_pos', info.ac_path() + simple.slash_os() + 'project', namespace = '__ac__')
else: stdinout.var('pj_pos', save_path, namespace = '__ac__')
import core, interfaces, tools
sys.path[0] = save_path

del sys
del sb
del _path
del save_path
del stdinout
del info
del simple
del manager