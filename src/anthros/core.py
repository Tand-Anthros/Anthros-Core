from interfaces import console, clickermann
from tools import assembly, info, manager, represent, simple, stdinout, convert
import os, sys, threading, copy, time

class help():
    r'''Добро пожаловать в AC (anthros - core)!
 Что бы нам было удобнее, импортируйте пакет AC вот так: from anthros import core as ac
 *Обратите внимание, что использование модуля Anthros или его дочерних объектов кроме core, неприемлимо
 *Советую выставить ширену консоли не менее 120 символов, для комфортного отоборажения

Давайте для начала определимся с двумя понятиями. Запуск AC через консоль и через проект
 Если вы скачивали AC не через пакет, то у вас должно быть что то вроде run.bat или run.sh
  В противном же случае может быть вызван вручную через python скрипт
  выполните: ac.interfaces.console.run()
 Запуск через проект, собственно происходит при самом импорте, в атрибутах ac уже есть всё что вам нужно
  *Заметка для тех, кто смотрит документацию через скрипт,
   используйте: ac.help.object(), ac.help.object.attribute()

Запуск AC в интерактивном режиме позволит поэксперементировать с модулем или кодом python на живую
Запуск AC через проект позволит расширить ваш проект инструментами, интерфейсами, а так же использовать
 ваши локальные файлы проекта так, буд-то это атрибуты ac.projeсt, например: ac.project.manifest

Если вы системный админестратор или человек интресующийся конкретно AC, советую использовать интерактивный режим
 введите: help interact
Разработчики же, могут использовать AC для расширения своего проекта, а интерактивный режим для тестов
 выполните: print(ac.help.devolop()); введите: help devolop

Если вышесказанное для вас показалось сложным, вы можете воспользоваться справкой для новичков, введите: help basic
Для дополнительной информации по ac можете обратится к документации ядра, введите: help ac'''

    def __init__(self, pos: 'list' = [], test = 123):
        self.pos = pos

    def __call__(self):
        global help
        if self.pos == []: return help.__doc__
        else:
            global ac
            _ac = ac()
            return sub.goto_attr(_ac, self.pos).__doc__

    def __getattr__(self, attr: 'str'):
        global help
        out = help(self.pos + [attr])
        return out

    def interact(self):
        r'''Думаю все знакомы с игрой minecraft? Если нет, то не страшно, однако проведу аналогию с этой игрой
 Использование интерактивного режима AC не сложнее чем использовать команды в minercaft, но со своими особенностями...

Синтаксис, он очень прост, вся команда состоит из имён написанных через пробел
 А какие имена есть и что они делают? для этого нужно копнуть немного глубже, но поверьте это проще чем кажется
 Cтандартные имена AC: tools, project, interfaces, extens, help
 Получить их список можно просто нажав enter, или введя: dir
Так же стоит добавить по поводу dir и help. прочтите о этих командах подробнее, что бы вам проще было ориентироватся,
 введите: help help; введите: help dir

Теперь тонкости. Имена это объекты а подимена это атрибуты и аргументы, но не торопитесь пугаться, я объясню
 Объекты, по сути это виртуальное представление данных, которые позволяют совершать над собой какие то действия
 Атрибуты, это всё то, что пишется через точку после объекта: ac.help.interact
 Аргументы, передаваемые вами данные для выполнения функции, например 123: ac.tools.simple.type(123)
  *Функция, это любой атрибут который может быть вызван и не является классом
 Теперь переведём код в команду: ac.tools.simple.type(123); получится: tools simple type 123
  где tools объект, simple и type аттрибуты, а 123 передаваемый аргумент
  *имя ac используется только в проекте, в консоли вы вызываете его атрибуты по умолчанию

Спросите, зачем вам эта информация? Для понимания процесса. Теперь когда вы разобрались в этом, продолжим
Иногда вам нужно явно указать где атрибуты, а где аргументы, сделать это можно с помощью допольнительного
 Пробела: tools simple type  123
 Где два пробела подряд обозначают конец перечесления атрибутов и начало передачи аргументов
Так же, вы можете "аккуратно" получить последний атрибут, указав пробел в конце, помимо доступных атрибутов
 вы получите объект из этого атрибута который сохранится в переменную _
Что ещё за переменная _? В этой переменной хранится результат последней выполненой вами команды, если это не None и
 не ошибка. Но это не всё, вы так же можете получить и предыдущие результаты с помощью __, ___, ____ и тд.
Зачем вам "аккуратно" получать объект? Для того, что бы не вызвать его, некоторые атрибуты не вызываемы
 Например: interfaces console ; после вы можете: _ run

Теперь вы знакомы с основами интерактивной консоли, но для более полного понимания, все же советую посетить
 документацию и по объекту ac, того самого, атрибутами которого вы пользуетесь: help ac
*Так же стоит упомянуть, что передаваемые аргументы автоматический конвертируются в требуемый тип, про тонкости
 этого процесса, вы можете узнать в: help subs; помимо этого там рассказанно про модификацию комманд в AC'''
        return self.interact.__doc__

    def devolop(self):
        r'''Творцы, чудесные люди, но без должной среды их жизнь была бы тяжкой
Раз вы попали сюда, то наверное уже разбираетесь в основах, но все же,
 настоятельно рекомендую посетить основы interact и ac, введите: help interact; help ac

Что касается использования самого ac, то про его стандартные атрибуты вы уже знаете
Всё что нужно вам для создания приложения, это загрузить или создать нужные вам файлы
Далее определитесь с интерфейсом, в ac пока что есть коносльный и символьный интерфейсы
 Если же вам они не подходят выберете какую нибудь библиотеку из вашего языка программирования
 *На данный момент ac поддерживает только python, посему могу предложить tkinter, kivy, pygame, qt
  А так же могу предложить и веб интерфейсы Flask, Django, и интерфейс для ботов, к примеру discord.py
  Обязательно не забудте про интерфейс ввода, к примеру keyboard, pyautogui, хотя они могут быть и встроены

Когда с интерфейсами и с файлами все решено, если нет, обратитесь к документации, введите: help interfaces; help extens
 Всё недостоющее вы можете найти в сообществе Anthros или создать самостоятельно
Теперь далее, мы пришли к самому интересному и сложному. Структура вашего проекта
 Для начала займитесь настройкой своего файла manifest, что бы в проекте все работало так, как нужно вам
  Подробнее вы естствено можете узнать, введя: help manifest
 После аргонизуйте ваше приложение или игру. Создайте отдельные папки для различных окон, создайте папку инструментов
  Введите: help tools
 Создайте отдельную папку для временных файлов, создайте папку контента, от куда будете подгружать звуки и визуал
 Не забудъте и про папку с зависимостями, которые нужны для запуска приложения, к примеру chromedriver

Архитектура сугубо творческий процесс, проявите фантазию. А теперь приступим к написанию кода
Импортируйте все нужное, благодоря ac.project, подгрузите все нужны данные
Благодоря собственным наработкам и ac.tools, сделайте над данными нужные манипуляции
Удалите все лишнее и создайте заготовки интерфейсов, запустите глобальный цикл
Запустите интерфейс, выведете нужную информацию на экран, ожидайте ввоба пользователя,
 после изменяйте интерфейс, делайте нужные изменения с файлами в проекте

По большому счёту это всё. В первый раз будет очень сложно, но не бойтесь трудностей, у вас обязательно получится
Если вам показалось все вышесказанное трудноватым, то попробуйте для начала использовать ac как пользователь
Введите help interact; help basic'''
        return self.devolop.__doc__

    def basic(self):
        r'''Данное руководство будет созданно позже (ac требует много внимания, поэтому лучше сфокусироваться пока на нём)
Но вы всё ещё можете воспользоваться ссылками на руководства оставленными ниже:
https://www.youtube.com/playlist?list=PLMB6wLyKp7lWSa816Oicnp6X66oZhBrP4
https://www.youtube.com/playlist?list=PLvoBekrlHDgROfUUHMbrrdsy_b2y2V_rj
https://pythonworld.ru/samouchitel-python (Русская документация)
https://docs.python.org/3/ (Официальная англоязычная)
*Это всё руководства для python, так как ac пока что базируется только на нём

Чудесные люди, которые на пальцах расскажут вам о основах
Не бойтесь ошибаться и не чего не понимать, вам предстоит чудесная пора открытий

Что касается использования исключительно AC, для начала вам будет достаточно и внутреннего руководства,
Напишите: help interact; help ac'''
        return self.basic.__doc__

    def help(self):
        r'''Знаю, забавно видеть такую команду
Что касается использования, то help это не обычная функция, это способ вызова как и dir
*Такие способы вызова вы можете задать самостоятельно благодоря subs, введите: help subs

Как работает? Если вы знакомы с основами "interact" то знакомы с объектом, аттрибутами и аргументами
Так вот help выступает в роли стандартного объекта ac, а все аттрибуты переданные help воспринимаются как аттрибуты ac
С тем лишь отличием, что help не работает с аргументами, он "аккуратно" получает объект и возвращает его доки
*Эту информацию можно получить и без help, просто в конце вместо аргументов написать __doc__
 Однако это будет иногда работать некорректно с самим объектом ac и его компонентами
 Ну а так же в будущем планируются и переводы, которые так же без использования help не сработают'''
        return self.help.__doc__

    def dir(self):
        r'''Работает так же как и help, но возвращает доступные атрибуты для объекта
*К сожалению пока не реализован, ждите следуещего обновления
*Так же как и с help, эту информацию можно получить вместо аргументов написав __dir__'''
        return self.dir.__doc__

    def ac(self):
        r'''Знали бы вы, сколько времени и нервов я на это всё потратил...
Базовый, стандартный объект anthros-core, собственно и одноимённый ac, что их себя представляет? Разберёмся ниже

Сам объект ac сам по себе... ничто, лишь набор логики, вся магия кроется в его гибкости и компонентах
Перечислю все компоненты, а после разберём их по отдельности: tools, extens, interfaces, envs, apps

Компонент tools, является набором модулей по сути с набором функций, однако вы можете допускать вольности.
 Но не забывайте, что tools выполняет функцию ящика с инструментами. Чем инструмент проще и независимее тем лучше
 Использование других компонентов из tools строго запрещенно, tools обязан быть независимым в избежании ошибок
*На самом деле любой компонент не должен быть в единственном числе, они состоят из множества частей, но так удобнее

Компонент extens, является набором классов, которые представляют собой виртуальные виды файлов или создают новый
 объекты из переданной при иницилизации информации
*Если вы знаете python, то благодоря анотациям, можно явно указать, какой тип передавать в функцию, так вот ac
 Подхватывает это значение и находит одноимённый экстенс, куда и передаёт не преобразованный аргумент, а после
 возвращает готовый объект на базе extens и это работает как в интерактивном режиме, так и в режиме разработчика

Компонент interfaces, является набором пакетов. При чем, не обязательно пакетов созданными сообществом anthros.
 Это может быть пакет qt или интерфейс для бота в discord. Сам interfaces по сути представляет собой переходник,
 к примеру переходник между пользователем и программой, между программой и лампочкой в умном доме

Компонент envs, является вашей песочницей, тут может находится что угодно и как вам угодно. Думаю, многим
 программистам должны быть знакомы виртуальные окружения. Вы можете пользоваться определённым окружением как
 мини - операционной системой, а другим уже как средой для создания собственного приложения

Компонент apps, является настроенной песочницей других умельцев сообщества. По сути готовые приложения,
 ну или что то похожее на них, на что хватит фантазии, хоть дистрибутив на основе ac
*Функционал одного и другого пока выполняет project, расположение которого вы можете менять

Про каждый компонент подробнее вы можете прочесть в help, к примеру введите: help tools
*Однако envs и apps, пока что являются project
А так же, manifest, это не компонент, это файл который задаёт настройки вашего проекта, введите: help manifest'''
        return self.ac.__doc__

    def subs(self):
        r'''Компонент subs, переосмысли данное по новому
Компонент subs пока что находится внутри ядра и моддификации не подвержен, мы сделаем это в скором времени,
 про изменения вы можете прочесть в отдельном листе, введите: help versions'''
        return self.subs.__doc__

    def manifest(self):
        r'''manifest, или то как скинуть часть проблем на пользователя
И он не работает, пока что. Смотрите изменения, написав: help versions'''
        return self.manifest.__doc__

    def project(self):
        r'''В ваших руках так много свободы! Но на неё вы не чего не способны себе позволить
Компонент project, это папка в которой вы решили начать работать. Задаётся она автоматический при импорте ac
Через компонент project вы можете обратится к любому файлу в вашем проекте, и делать что то с ним
Для этого в ваших extens должен быть одноимённый расширению файла класс, введите: help extens

Используйте ваши файлы, делайте с ними требуемое вам, а после можете написать для этого всего интерфейс
Введите: help interfaces
Ну и если будете готовы писать полноценное приложение, то введите: help devolop'''
        return self.project.__doc__

    def envs(self):
        r'''Компонент envs все ещё находится в разработке, его заменяет компонент project'''
        return self.envs.__doc__ + '\n\n' + self.project.__doc__

    def apps(self):
        r'''Компонент apps все ещё находится в разработке, его заменяет компонент project'''
        return self.apps.__doc__ + '\n\n' + self.project.__doc__

    def versions(self):
        r'''Пришли заглянуть что новенького?
Проследить за выходом обнавлений вы можете по ссылке: https://pypi.org/project/anthros-core/

v1.0 Самая первая версия, которая даже толком не справлялась со своими функциями:
 - Добавлен core и его работа по атрибутам
 - Добавлен интерфейс console
 - Добавлены реализации для extens и tools, а так же небольшое необходимое количество
 - Реализован отладчик ошибок

v1.1 То же что и первая, но качественее
 - Реализована документация и возможность просмотра атрибутов
 - Добавлен этот раздел, а так же созданна ирархия всех ac
    Их было куда больше чем две версии, намнооого больше
 - Новые tools и extens
 - Оптимизации в пакете для более стабильной работы
 - Доработан отладчик ошибок, однако он не похож на стандартный, из за сложности получения данных из шапки
 - Правка множества багов, причесывание в целом
 - Упрознены extens _def, _class, _py. Сделаем в будущем, пока работаем над доработкой другого

v1.2 Кажется я начал входить во вкус
 - Переработан ini
 - Добавлен ради эксперемента интерфейс clickermann
    Разработчик, не кусай, мы уважаем твою работу, вот ссылка на неё: http://crapware.aidf.org/page/clickermann
    Да мы не собираемся её оставлять вот так, пока думаем над этим
 - Доработана работа в интерактивном режиме, некоторые вещи теперь выполняются как задумано

 Заметки:
 - Вы можете заметить что некоторые части ac на английском, мы работаем над этим и в будущем хотим сделать переводы
 - args и dir планируется добавить в следующем обнавлении
 - Не всегда корректно отрабатывает tools.info.args, будет поправлено в будущем
 - Требуется расширять sub, так как нельзя экранировать расположения файлов кавычками
 - Нужнол починить ошибки происходящие в режиме пректа (иногда просто возвращается ошибка)
 - Добавить установку сторонних библиотек с подтверждением пользователя

 Вопросы (Напишите Tand(у), если есть мысли):
 - Стоит ли упрознять *.class и *.def? Есть некоторые проблемы с ними
 - Стоит ли реализовывать manifest? По сути все можно решить и без конфигов'''
        return self.versions.__doc__

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
    def command_pars(line: 'str', auto_var: ('list', 'tuple')):
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

    def command(self, command: ('str', 'list'), kwargs: 'dict' = None):
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