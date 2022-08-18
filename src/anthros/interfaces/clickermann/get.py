import os, time
from tools import info, manager, convert

def clicker_pos():
	return info.ac_path() + '\\interfaces\\clickermann\\exe\\Clickermann.exe'

def screen_width():
	out_pos = info.ac_path() + '\\interfaces\\clickermann\\exe\\projects\\get\\out.txt'
	manager.remove(out_pos)
	cms_pos = info.ac_path() + '\\interfaces\\clickermann\\exe\\projects\\get\\screen_width.cms'
	os.system(clicker_pos() + ' ' + cms_pos)
	time.sleep(0.1)
	out = manager.open_file(out_pos)	
	return convert.to_int(out) + 1

def screen_height():
	out_pos = info.ac_path() + '\\interfaces\\clickermann\\exe\\projects\\get\\out.txt'
	manager.remove(out_pos)
	cms_pos = info.ac_path() + '\\interfaces\\clickermann\\exe\\projects\\get\\screen_height.cms'
	os.system(clicker_pos() + ' ' + cms_pos)
	time.sleep(0.1)
	out = manager.open_file(out_pos)	
	return convert.to_int(out) + 1

def screen_size():
	return (screen_width(), screen_height())

def screenshot(from_x: 'int' = 0, from_y: 'int' = 0, to_x: 'int' = None, to_y: 'int' = None):
	pass
