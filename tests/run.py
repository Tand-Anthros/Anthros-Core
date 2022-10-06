#from anthros import core as ac
#Не работает запуск AC, поправить
import os, sys

if sys.platform in ['win32']: slash = '\\'
else: slash = '/'

if '\\' in str(__file__): pos = str(__file__).split('\\')
else: pos = str(__file__).split('/')
pos = slash.join(pos[:len(pos) - 2] + ['src', 'anthros'])

sys.path[0] = pos
os.chdir(pos)
if sys.platform == 'win32':
    os.system(pos.split(slash)[:1][0])

import core as ac
ac.interfaces.console.run()


r'''
import os, sys

if sys.platform in ['win32']: slash = '\\'
else: slash = '/'

if '\\' in str(__file__): pos = str(__file__).split('\\')
else: pos = str(__file__).split('/')
pos = slash.join(pos[:len(pos) - 2] + ['src', 'anthros'])

sys.path[0] = pos
os.chdir(pos)
if sys.platform == 'win32':
    os.system(pos.split(slash)[:1][0])

import core as ac
ac.interfaces.console.run()
'''