import os
import subprocess


class SudoLogin:
    user_name = ''

    def __init__(self, username):
        self.user_name = username

    def get_sudo_login(self):
        print('Please enter your macbook password')
        os.system('sudo echo Hello ' + self.user_name)
        result = subprocess.run(['sudo', 'whoami'], stdout=subprocess.PIPE)
        file_name = "/Users/" + self.user_name + "/Sites/sudo.tmp"
        g = open(file_name, 'wb')
        g.write(result.stdout)

    def check_if_root_or_not(self):
        file_name = "/Users/" + self.user_name + "/Sites/sudo.tmp"
        with open(file_name) as f:
            for c in f.readlines():
                if c.find('root') >= 0:
                    print('Enjoy u are sudo user')
                    return True

        return False
