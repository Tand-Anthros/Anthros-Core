Думаю все знакомы с игрой minecraft? Если нет, то не страшно, однако проведу аналогию с этой игрой
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
 этого процесса, вы можете узнать в: help subs; помимо этого там рассказанно про модификацию комманд в AC