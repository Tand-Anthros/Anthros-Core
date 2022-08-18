from anthros import core as ac

path = ac.extens.path(__file__) - 2

try: ac.tools.manager.remove(str(path + f'src/anthros_core.egg-info'))
except: pass
fold = ac.tools.represent.fold_dict(str(path + 'dist'))
for key in fold.keys():
    if '.whl' in key: ac.tools.manager.remove(fold[key])

if ac.tools.assembly.create_whl(str(path)) != 0: exit()

fold = ac.tools.represent.fold_dict(str(path + 'dist'))
for key in fold.keys():
    if '.whl' in key: ac.tools.assembly.install_package(fold[key])