import os


class UserName:

    def get_user_name(self):
        print('Fetching your username for macbook')
        os.system('whoami > username.tmp')
        f = open("username.tmp", "r")
        file_array = f.readlines();
        user_name = file_array[0]
        user_name = user_name.strip('\n')
        print('Your user name is : ' + user_name)
        return user_name
