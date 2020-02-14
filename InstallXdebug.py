import os
import subprocess


class AddAndConfigureDebugger:
    def __init__(self, user_name):
        self.user_name = user_name

    def process(self):
        xdebug = Xdebug(self.user_name)
        xdebug.install_xdebug()


class Xdebug:
    def __init__(self, user_name):
        self.user_name = user_name

    def install_xdebug(self):
        os.system('pecl install xdebug')
        self.find_php_loaded_file()
        obj = AddXdebugSettingToPhpLoadedFile(self.user_name, self.loaded_php_conf)
        obj.modify_php_loaded_file()

    def find_php_loaded_file(self):
        file_name = "/Users/" + self.user_name + "/Sites/phpini.tmp"
        result = subprocess.run(['php', '--ini'], stdout=subprocess.PIPE)

        g = open(file_name, 'wb')
        g.write(result.stdout)
        g.close()

        self.search_load_module()

    def search_load_module(self):
        file_name = "/Users/" + self.user_name + "/Sites/phpini.tmp"
        with open(file_name) as f:
            for c in f.readlines():
                if c.find('Loaded Configuration File:') >= 0:
                    self.loaded_php_conf = c.strip('Loaded Configuration File:')
                    self.loaded_php_conf = self.loaded_php_conf.strip('\n')
                    print('Got php loaded configuration path that is : ' + self.loaded_php_conf)

        return self.loaded_php_conf


class AddXdebugSettingToPhpLoadedFile:
    def __init__(self, user_name, file_name):
        self.user_name = user_name
        self.file_name = file_name

    def modify_php_loaded_file(self):
        template = "[xdebug]\nzend_extension=\"xdebug.so\"\nxdebug.remote_autostart=1\nxdebug.default_enable=1\nxdebug.remote_port=9001\nxdebug.remote_host=127.0.0.1\nxdebug.remote_connect_back=1\nxdebug.remote_enable=1\nxdebug.idekey=PHPSTORM"
        with open(self.file_name, "a") as myfile:
            myfile.write(template)

        print('Added Xdebug to loaded php configuration at : ' + self.file_name)
