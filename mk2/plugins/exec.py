import os
import re

from mk2.plugins import Plugin
from mk2.events import ServerOutput


# Yes, if not used properly, this kills kittens.
class Exec(Plugin):
    command = Plugin.Property(default="msg {user} {message}")
    path = Plugin.Property(default="triggerExec.txt")
    
    triggers = {}
    
    def setup(self):
        if self.path and os.path.exists(self.path):
            f = open(self.path, 'r')
            for l in f:
                m = re.match('^\!?([^,]+),(.+)$', l)
                if m:
                    a, b = m.groups()
                    c = self.triggers.get(a, [])
                    c.append(b)
                    self.triggers[a] = c
            f.close()
            
            if self.triggers:
                self.register(self.trigger, ServerOutput, pattern='<([A-Za-z0-9_]{1,16})> \!(\w+)')
    
    def trigger(self, event):
        user, trigger = event.match.groups()
        if trigger in self.triggers:
            for line in self.triggers[trigger]:
                os.system(line)
