import os
import subprocess
from Utility import Utility


class EtcDirectoryManagement:
    user_name = ''
    php_module = ''

    def __init__(self, user_name):
        self.user_name = user_name

    def process(self):
        # put a check if php modeule is not found to stop process there itself.
        php_info = GetPhpInfo(self.user_name)
        php_info.get_php_info()

        httpd_conf = HttpConfModification(self.user_name, php_info.php_module)
        httpd_conf.process()

        httpd_userdir = HttpdUserDirModification(self.user_name)
        httpd_userdir.process()

        httpd_vhost = HttpdVhostConf(self.user_name)
        httpd_vhost.process()

        httpd_user_name = CreateUserConfFile(self.user_name)
        httpd_user_name.process()

        hosts = HostsModification(self.user_name)
        hosts.process()

        # files = MoveBackupFileToOriginal(self.user_name)
        # files.process()


class GetPhpInfo:
    def __init__(self, user_name):
        self.user_name = user_name

    def get_php_info(self):
        print('Finding your system loaded php module')
        file_name = "/Users/" + self.user_name + "/sites/phpinfo.tmp"
        result = subprocess.run(['brew', 'info', 'php'], stdout=subprocess.PIPE)

        g = open(file_name, 'wb')
        g.write(result.stdout)
        g.close()

        return self.search_load_module()

    def search_load_module(self):
        file_name = "/Users/" + self.user_name + "/sites/phpinfo.tmp"
        with open(file_name) as f:
            for c in f.readlines():
                if c.find('LoadModule php7_module') >= 0:
                    self.php_module = c.strip('\n')
                    print('Found your loaded php module that is : ' + self.php_module)

        return self.php_module


class HttpConfModification:
    def __init__(self, user_name, new_php_module):
        self.user_name = user_name
        self.new_php_module = new_php_module

    def process(self):
        self.get_file_pointer()
        self.comment_and_replace_new_php_module()
        self.find_pattern_and_uncomment()
        self.close_pointer()

    def comment_and_replace_new_php_module(self):
        print('Commenting old loaded module of php7 with new php module that is loaded into system.')
        for line in self.fin:
            self.fout.write(line.replace('LoadModule php7_module libexec/apache2/libphp7.so',
                                         '#LoadModule php7_module libexec/apache2/libphp7.so\n' + self.new_php_module))

    def find_pattern_and_uncomment(self):
        print('Doing changes in httpd.conf.bk as required to setup local server')
        for line in self.fin:
            if Utility.check_string_replace_it('#LoadModule rewrite_module libexec/apache2/mod_rewrite.so', self.fout, line):
                continue
            elif Utility.check_string_replace_it('#LoadModule userdir_module libexec/apache2/mod_userdir.so', self.fout, line): continue

            elif Utility.check_string_replace_it('#LoadModule userdir_module libexec/apache2/mod_userdir.so', self.fout, line): continue
            elif Utility.check_string_replace_it('#LoadModule userdir_module libexec/apache2/mod_userdir.so', self.fout, line): continue
            else:
                self.fout.write(line)
                self.fout.write(line.replace('#LoadModule vhost_alias_module libexec/apache2/mod_vhost_alias.so',
                'LoadModule vhost_alias_module libexec/apache2/mod_vhost_alias.so'))
                self.fout.write(line.replace('#LoadModule authn_core_module libexec/apache2/mod_authn_core.so',
                'LoadModule authn_core_module libexec/apache2/mod_authn_core.so'))
                self.fout.write(line.replace('#LoadModule authz_host_module libexec/apache2/mod_authz_host.so',
                'LoadModule authz_host_module libexec/apache2/mod_authz_host.so'))
                self.fout.write(line.replace('#LoadModule include_module libexec/apache2/mod_include.so',
                'LoadModule include_module libexec/apache2/mod_include.so'))
                self.fout.write(line.replace('#Include /private/etc/apache2/extra/httpd-vhosts.conf',
                'Include /private/etc/apache2/extra/httpd-vhosts.conf'))
                self.fout.write(line.replace('#Include /private/etc/apache2/extra/httpd-userdir.conf',
                'Include /private/etc/apache2/extra/httpd-userdir.conf'))
                self.fout.write(line.replace('DocumentRoot \"/Library/WebServer/Documents\"',
                'DocumentRoot \"/User/' + self.user_name + '/Documents\"'))
                self.fout.write(line.replace('<Directory \"/Library/WebServer/Documents\">',
                '<Directory \"/User/' + self.user_name + '/Documents\">'))
                self.fout.write(line.replace('AllowOverride none', 'AllowOverride All'))
                # self.fout.write(line.replace('#LoadModule rewrite_module libexec/apache2/mod_rewrite.so',
                #                              'LoadModule rewrite_module libexec/apache2/mod_rewrite.so'))
                # self.fout.write(line.replace('#LoadModule userdir_module libexec/apache2/mod_userdir.so',
                #                              'LoadModule userdir_module libexec/apache2/mod_userdir.so'))
                # self.fout.write(line.replace('#LoadModule vhost_alias_module libexec/apache2/mod_vhost_alias.so',
                #                              'LoadModule vhost_alias_module libexec/apache2/mod_vhost_alias.so'))
                # self.fout.write(line.replace('#LoadModule authn_core_module libexec/apache2/mod_authn_core.so',
                #                              'LoadModule authn_core_module libexec/apache2/mod_authn_core.so'))
                # self.fout.write(line.replace('#LoadModule authz_host_module libexec/apache2/mod_authz_host.so',
                #                              'LoadModule authz_host_module libexec/apache2/mod_authz_host.so'))
                # self.fout.write(line.replace('#LoadModule include_module libexec/apache2/mod_include.so',
                #                              'LoadModule include_module libexec/apache2/mod_include.so'))
                # self.fout.write(line.replace('#Include /private/etc/apache2/extra/httpd-vhosts.conf',
                #                              'Include /private/etc/apache2/extra/httpd-vhosts.conf'))
                # self.fout.write(line.replace('#Include /private/etc/apache2/extra/httpd-userdir.conf',
                #                              'Include /private/etc/apache2/extra/httpd-userdir.conf'))
                # self.fout.write(line.replace('DocumentRoot \"/Library/WebServer/Documents\"', 'DocumentRoot \"/User/' + self.user_name + '/Documents\"'))
                # self.fout.write(line.replace('<Directory \"/Library/WebServer/Documents\">', '<Directory \"/User/' + self.user_name + '/Documents\">'))
                # self.fout.write(line.replace('AllowOverride none', 'AllowOverride All'))
                print('Done with changes that was required in httpd.conf.bk')


def get_file_pointer(self):
    # print('Creating backup file for httpd.conf as httpd.conf.bk in same directory')
    # os.system('sudo cp /etc/apache2/httpd.conf /etc/apache2/httpd.conf.bk')
    # os.system('sudo cp /etc/apache2/httpd.conf /etc/apache2/httpd.conf.original')
    print('Giving rwx permission to every party for httpd.conf.bk file')
    os.system('sudo chmod 777 /etc/apache2/httpd.conf.bk')

    self.fin = open("/etc/apache2/httpd.conf", "rt")
    self.fout = open("/etc/apache2/httpd.conf.bk", "wt")


def close_pointer(self):
    self.fin.close()
    self.fout.close()


class HttpdUserDirModification:
    def __init__(self, user_name):
        self.user_name = user_name

    def process(self):
        self.get_file_pointer()
        self.find_pattern_and_uncomment()
        self.close_file_pointer()

    def find_pattern_and_uncomment(self):
        print('Uncommenting line in httpd-userdir.conf.bk as required to setup local server')
        for line in self.fin:
            self.fout.write(line.replace('#Include /private/etc/apache2/users/*.conf',
                                         'Include /private/etc/apache2/users/*.conf'))
        print('Done with changes that was required in httpd-userdir.conf.bk')

    def get_file_pointer(self):
        print('Creating backup file for httpd-userdir.conf as httpd-userdir.conf.bk in same directory')
        os.system('sudo cp /etc/apache2/extra/httpd-userdir.conf /etc/apache2/extra/httpd-userdir.conf.bk')
        os.system('sudo cp /etc/apache2/extra/httpd-userdir.conf /etc/apache2/extra/httpd-userdir.conf.original')
        os.system('sudo chmod 777 /etc/apache2/extra/httpd-userdir.conf.bk')

        self.fin = open("/etc/apache2/extra/httpd-userdir.conf", "rt")
        self.fout = open("/etc/apache2/extra/httpd-userdir.conf.bk", "wt")

    def close_file_pointer(self):
        self.fin.close()
        self.fout.close()


class HttpdVhostConf:
    def __init__(self, user_name):
        self.user_name = user_name

    def process(self):
        self.create_file_backup_and_give_permission()
        self.write_content()

    def write_content(self):
        print('Adding lines to httpd-vhosts.conf.bk for local setup')
        template = "<VirtualHost *:80>\nDocumentRoot \"/Users/" + self.user_name + "/Sites\"\nServerName localhost\n</VirtualHost>\n<VirtualHost *:80>\nDocumentRoot \"/Users/" + self.user_name + "/Sites/justride-api/public\"\nServerName api.drivezy\n</VirtualHost>"
        with open("/etc/apache2/extra/httpd-vhosts.conf.bk", "a") as myfile:
            myfile.write(template)
        print('Done with changes in httpd-vhosts.conf.bk')

    def create_file_backup_and_give_permission(self):
        print('Creating backup file for httpd-vhost.conf as httpd-vhost.conf.bk in same directory')
        os.system('sudo cp /etc/apache2/extra/httpd-vhosts.conf /etc/apache2/extra/httpd-vhosts.conf.bk')
        os.system('sudo cp /etc/apache2/extra/httpd-vhosts.conf /etc/apache2/extra/httpd-vhosts.conf.original')
        print('Changing permission of httpd-vhost.conf.bk to rwx to all three parties')
        os.system('sudo chmod 777 /etc/apache2/extra/httpd-vhosts.conf.bk')


class CreateUserConfFile:
    def __init__(self, user_name):
        self.user_name = user_name

    def process(self):
        self.get_file_pointer()
        self.write_on_file()
        self.close_file_pointer()

    def write_on_file(self):
        self.fout.write(self.template)

    def get_file_pointer(self):
        print(
            'Creating backup file for ' + self.user_name + '.conf as ' + self.user_name + '.conf.bk in same directory')
        os.system('sudo touch /etc/apache2/users/' + self.user_name + '.conf.bk')
        os.system('sudo chmod 777 /etc/apache2/users/' + self.user_name + '.conf.bk')

        # modify the below code
        self.template = "<Directory \"/Users/" + self.user_name + "/Sites/\">\nAllowOverride All\nOptions Indexes MultiViews FollowSymLinks\nRequire all granted\n</Directory>"
        self.fout = open("/etc/apache2/users/" + self.user_name + ".conf.bk", "wt")

    def close_file_pointer(self):
        self.fout.close()


class HostsModification:
    def __init__(self, user_name):
        self.user_name = user_name

    def process(self):
        self.create_file_backup_and_give_permission()
        self.write_content()

    def write_content(self):
        print('Adding lines to httpd-vhosts.conf.bk for local setup')
        template = "127.0.0.1\tapi.drivezy"
        with open("/etc/hosts.bk", "a") as myfile:
            myfile.write(template)
        print('Done with changes in hosts.bk')

    def create_file_backup_and_give_permission(self):
        print('Creating backup file for hosts as hosts.bk in same directory')
        os.system('sudo cp /etc/hosts /etc/hosts.bk')
        os.system('sudo cp /etc/hosts /etc/hosts.original')
        print('Changing permission of host.bk to rwx to all three parties')
        os.system('sudo chmod 777 /etc/hosts.bk')


class MoveBackupFileToOriginal:
    def __init__(self, user_name):
        self.user_name = user_name

    def process(self):
        self.move_files_and_restore_permission()

    def move_files_and_restore_permission(self):
        print('Replacing the modified file with original ones, and restoring permission')
        os.system('sudo mv /etc/apache2/httpd.conf.bk /etc/apache2/httpd.conf')
        os.system('sudo chmod 644 /etc/apache2/httpd.conf')

        os.system('sudo mv /etc/apache2/extra/httpd-userdir.conf.bk /etc/apache2/extra/httpd-userdir.conf')
        os.system('sudo chmod 644 /etc/apache2/extra/httpd-userdir.conf')

        os.system('sudo mv /etc/apache2/extra/httpd-vhosts.conf.bk /etc/apache2/extra/httpd-vhosts.conf')
        os.system('sudo chmod 644 /etc/apache2/extra/httpd-vhosts.conf')

        os.system(
            'sudo mv /etc/apache2/users/' + self.user_name + '.conf.bk /etc/apache2/users/' + self.user_name + '.conf')
        os.system('sudo chmod 644 /etc/apache2/users/' + self.user_name + '.conf')

        os.system('sudo mv /etc/hosts.bk /etc/hosts')
        os.system('sudo chmod 644 /etc/hosts')
        print('Replaced all the files')
