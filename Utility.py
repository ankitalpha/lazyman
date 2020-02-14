class Utility:
    @staticmethod
    def check_string_replace_it(search, w_pointer, r_pointer):
        if r_pointer.find(search) >= 0:
            w_pointer.write(r_pointer.replace(search, search.strip('#')))
            return True
        return False

