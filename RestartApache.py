import os

class RestartApache:

    def process(self):
        print('Restarting apache server.')
        os.system('sudo apachectl restart')
        os.system('sudo apachectl restart')
        os.system('sudo apachectl restart')
        print('Restarted apache server.')