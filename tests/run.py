from anthros import core as ac

slash = ac.tools.simple.slash_os()
pos = str(__file__).split(slash)
pos = slash.join(pos[:len(pos) - 2] + ['src', 'anthros'])

ac.tools.simple.pos_switch(pos)

import core as ac
ac.interfaces.console.run()