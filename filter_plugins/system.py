# Copyright (c) 2016 crito <crito@fifo.sh>

import pwd

class FilterModule(object):
    def filters(self):
        return {
            'getHome': self.getHome,
        }

    def getHome(self, user):
        return pwd.getpwnam(user).pw_dir
