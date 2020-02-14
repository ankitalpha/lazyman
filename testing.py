import os
import subprocess
from UserName import UserName
from SudoLogin import SudoLogin
from EtcDirectoryManagement import EtcDirectoryManagement
from InstallDependencyForLocalServer import InstallDependencyForLocalServer
from InstallXdebug import AddAndConfigureDebugger
from RestartApache import RestartApache
from InstallSoftware import InstallSoftware
from Utility import Utility


class HttpConfModification:
    def __init__(self):
        self.user_name = 'ankittiwari'

    def process(self):
        self.get_file_pointer()
        self.find_pattern_and_uncomment()
        self.close_pointer()

    def check(self, search, w_pointer, r_pointer):
        if r_pointer.find(search) >= 0:
            w_pointer.write(r_pointer.replace(search, search.strip('#')))
            return True

    def find_pattern_and_uncomment(self):
        print('Doing changes in httpd.conf.bk as required to setup local server')
        for line in self.fin:
            self.check('#LoadModule rewrite_module libexec/apache2/mod_rewrite.so', self.fout, line)
            # self.check('#LoadModule userdir_module libexec/apache2/mod_userdir.so', self.fout, line)
            self.check('#LoadModule vhost_alias_module libexec/apache2/mod_vhost_alias.so', self.fout, line)
            # self.fout.write(line.replace('#LoadModule rewrite_module libexec/apache2/mod_rewrite.so',
            #                              'LoadModule rewrite_module libexec/apache2/mod_rewrite.so\n'))
            # self.fout.write(line.replace('#LoadModule userdir_module libexec/apache2/mod_userdir.so',
            #                              'LoadModule userdir_module libexec/apache2/mod_userdir.so\n'))
            # self.fout.write(line.replace('#LoadModule vhost_alias_module libexec/apache2/mod_vhost_alias.so',
            #                              'LoadModule vhost_alias_module libexec/apache2/mod_vhost_alias.so\n'))
        print('Done with changes that was required in httpd.conf.bk')

    def get_file_pointer(self):
        print('Creating backup file for httpd.conf as httpd.conf.bk in same directory')
        # os.system('sudo cp /Users/ankittiwari/sites/lazyman/testing.tmp  /Users/ankittiwari/sites/lazyman/testing.tmp.bk')
        # os.system('sudo chmod 777 /Users/ankittiwari/sites/lazyman/testing.tmp.bk')

        self.fin = open("/Users/ankittiwari/sites/lazyman/testing.tmp", "rt")
        self.fout = open("/Users/ankittiwari/sites/lazyman/testing.tmp.bk", "r+")

    def close_pointer(self):
        self.fin.close()
        self.fout.close()


def run():
    print(Utility.return_true(False))

    # obj = HttpConfModification()
    # obj.process()


if __name__ == '__main__':
    run()