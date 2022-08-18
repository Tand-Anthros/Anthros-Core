r'''Возвращает объект ядра консольного интерфейса
*Для запуска АС через него используйте run()'''
from tools import stdinout, info
import sys, os
if sys.path[0][len(sys.path[0]) - 1] == 'interfaces': sys.path[0] = sys.path[0][:len(sys.path[0]) - 1]
hello_text = f'anthros-core (1.1a) for {info.system_name()}\n  write "help" for command help\n'

def clear_screen():
    r'''Очищает консоль'''
    if sys.platform == 'win32': os.system('cls')
    else: os.system('clear')

def run():
    r'''Запускает интерактивный режим AC
*Что бы выйти введите: exit'''
    import core
    clear_screen()
    print(hello_text)

    cmd = ''
    while cmd not in ['exit', 'restart']:
        cmd = input('>')

        if cmd == 'clear':
            clear_screen()
            print(hello_text)
            continue

        try:
            if cmd not in ['exit', 'restart']:
                out = core.command(cmd)
                if out != None: print(out, end = '\n\n')
                else: print(end = '\n')
        except:
            err = stdinout.exception(sys.exc_info())
            print(err, end = '\n\n')

    if cmd == 'restart': run()