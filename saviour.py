import os
import subprocess
from UserName import UserName
from SudoLogin import SudoLogin
from EtcDirectoryManagement import EtcDirectoryManagement
from InstallDependencyForLocalServer import InstallDependencyForLocalServer
from InstallXdebug import AddAndConfigureDebugger
from RestartApache import RestartApache
from InstallSoftware import InstallSoftware


def run():
    user_name_object = UserName()
    user_name = user_name_object.get_user_name()

    root = SudoLogin(user_name)
    root.get_sudo_login()

    if (not root.check_if_root_or_not()):
        print('Sorry you have to login with root to run this script')
        return

    install_dependency = InstallDependencyForLocalServer(user_name)
    install_dependency.process()

    local_setup = EtcDirectoryManagement(user_name)
    local_setup.process()

    apache = RestartApache()
    apache.process()

    debugger = AddAndConfigureDebugger(user_name)
    debugger.process()

    apache = RestartApache()
    apache.process()

    softwares = InstallSoftware(user_name)
    softwares.process()









if __name__ == '__main__':
    run()