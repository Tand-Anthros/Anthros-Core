from tools import simple

def to_int(obj: 'str'):
    '''Конвертирует базовые типы в int если это возможно, иначе ошибка
*В случае с str берёт все возможные числа и возвращает так, буд-то это одно число'''
    if simple.type(obj) == 'str':
        out = ''
        for sb in obj:
            if sb.isdigit(): out += sb
        return int(out)

