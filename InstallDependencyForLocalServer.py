import os
import subprocess


class InstallDependencyForLocalServer:
    user_name = ''

    def __init__(self, user_name):
        self.user_name = user_name

    def process(self):
        sites = CreateSitesDirectory(self.user_name)
        sites.create_sites_directory()

        php = InstallPhp(self.user_name)
        php.install_php()

        composer = InstallComposer(self.user_name)
        composer.install_composer()

        mysql = InstallMysql(self.user_name)
        mysql.install_mysql()


class InstallPhp:
    def __init__(self, username):
        self.user_name = username

    def install_php(self):
        print("🐘🐘🐘🐘 Installing Php@7.3 🐘🐘🐘🐘")
        result = subprocess.run(['brew', 'install', 'php@7.3'], stdout=subprocess.PIPE)
        file_name = "/Users/" + self.user_name + "/sites/php.tmp"
        g = open(file_name, 'wb')
        g.write(result.stdout)


class InstallComposer:
    def __init__(self, username):
        self.user_name = username

    def install_composer(self):
        print(" 🎵🎵🎵🎵 Installing composer@1.9 🎵🎵🎵🎵🎵🎵🎵")
        result = subprocess.run(['brew', 'install', 'composer'], stdout=subprocess.PIPE)
        file_name = "/Users/" + self.user_name + "/sites/composer.tmp"
        g = open(file_name, 'wb')
        g.write(result.stdout)


class InstallMysql:
    def __init__(self, username):
        self.username = username

    def install_mysql(self):
        print(" 💿💿💿💿 Installing Mysql@5.7 💿💿💿💿")
        result = subprocess.run(['brew', 'install', 'mysql@5.7'], stdout=subprocess.PIPE)
        file_name = "/Users/" + self.username + "/sites/mysql.tmp"
        g = open(file_name, 'wb')
        g.write(result.stdout)
        os.system('brew tap homebrew/services')
        os.system('brew services start mysql@5.7')
        os.system('brew link mysql@5.7 --force')


class CreateSitesDirectory:
    def __init__(self, user_name):
        self.user_name = user_name

    def create_sites_directory(self):
        print('Creation site directory:')
        os.system('sudo mkdir /Users/' + self.user_name + '/Sites')
