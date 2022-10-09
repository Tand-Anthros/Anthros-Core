import anthros
from anthros.tools import simple

def find_template(line, template, mode: ('str')):
    r''' searches the _template_ in the _line_ with the return _mode_:
            'p' - returns list with positions where template is found
            'q' - returns quanity of positions
            'qir' - returns list of quanity of positions in a rows
    '''
    if simple.type(line) != 'str':
        print('line != str')
        return -1
    if simple.type(template) != 'str':
        print('template != str')
        return -1
    if simple.type(mode) != 'str':
        print('mode != str')
        return -1

    #if mode != 'p':
	    #if mode != 'q':
		    #if mode != 'qir':
		        #return -1

    line_length = len(line)
    template_length = len(template)
    poses = list()

    for i in range(0, line_length - template_length + 1):
        if line[i:(i+template_length)] == template:
        	poses.append(i)

    if mode == 'p':
        return poses #list of int

    if mode == 'q':
        return len(poses) #int

    lst_quanity = list()
    quanity = 1
    prev = 0
    for i in range(0, len(poses) - 1):
        if poses[i] + 1 == poses[i + 1]:
            quanity+=1;
        else:
            lst_quanity.append(quanity)
            quanity = 1
    lst_quanity.append(quanity)
    return lst_quanity # list of int

def get_blocks(fill: ('str'), tabs: ('list', 'tuple', 'str')):
    
    #converts _tabs_ into list with integers
    def __convert_tabs(tabs: ('list', 'tuple', 'str')):
        if simple.type(tabs) == 'tuple':
            lst = list()
            for i in range(0, len(tabs)):
                if simple.type(tabs[i] != 'int'):
                    lst[i].append(int(tabs[i]))
                else:
                   lst[i].append(tabs[i])
        #check the type of tabs('lst') elements 
        if simple.type(tabs) == 'list' and simple.type(tabs[i] == 'str'):
            lst = list()
            for i in range(0, len(tabs)):
                lst.append(int(tabs[i]))
        if simple.type(tabs) == 'str':
            tabs = tabs.replace(' ', '')
            tabs = tabs.split(',')
            lst = list()
            for i in range(0, len(tabs)):
                lst.append(int(tabs[i]))
        #print(list)
        return lst

    def __max_element(lst: ('list')):
        mx = lst[0]
        for i in range(1, len(lst)):
            if lst[i] > mx:
                mx = lst[i]
        return mx

    tabs = __convert_tabs(tabs)
    lines = fill.split('\n') #separate lines with \n
    catname = '' #default category name
    line = ''
    outputl = list() #list with lists
    sublist = list() #list that is sublist
    maxtab = 0 #max tab with find_template
    maxtabs = __max_element(tabs) #max tab with given values
    for i in range(0, len(lines)):
        #category
        if find_template(lines[i], '[', 'q') == 1 or lines[i] == '':
            if (i > 0):
                outputl.append(sublist)
                #print('appending to outputl', sublist)
                sublist = 0
                sublist = list()
            catname = lines[i]
            catname = catname.replace('[', '')
            catname = catname.replace(']', '')
            #print('catname: ', catname)
            sublist.append(catname)
        #elements
        else:
            if maxtab == 0:
                maxtab = find_template(lines[i], ' ', 'qir')
                maxtab = maxtab[0]
                if maxtab > maxtabs:
                    maxtab = maxtabs
            line = lines[i]
            for i in range(0, maxtab):#cutting tab
                line = line[1:]
            #print('line: ', line)
            sublist.append(line)
    outputl.append(sublist)
    return outputl

'''
anthros.interfaces.console.clear_screen()
tab = '   '#3
line = '\n' + tab + 'lolly = hunter\n'
line += '[case]\n' + tab + 'gacha = life\n' + tab + 'simple = code\n'
line += '[lolly]\n' + tab + 'caser = bully\n'
line +=  '\n' + tab + 'spooky != shish'
print('__line__\n', line)
a = get_blocks(line, '1, 2, 3, 4')
print('\n\n__get_blocks__\n\n', a, '\n\n\n')
'''
