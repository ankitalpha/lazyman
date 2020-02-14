import os


class InstallSoftware:
    def __init__(self, username):
        self.username = username

    def process(self):
        self.install_php_storm()
        self.install_source_tree()
        self.install_postman()
        self.install_hangout()
        self.install_iterm2()
        self.install_google_chrome()
        self.install_sublime_text()

    def install_php_storm(self):
        os.system('brew cask install phpstorm')

    def install_source_tree(self):
        os.system('brew cask install sourcetree')

    def install_postman(self):
        os.system('brew cask install postman')

    def install_hangout(self):
        os.system('brew cask install google-hangouts')

    def install_iterm2(self):
        os.system('brew cask install iterm2')

    def install_google_chrome(self):
        os.system('brew cask install google-chrome')

    def install_sublime_text(self):
        os.system('brew cask install sublime-text')
