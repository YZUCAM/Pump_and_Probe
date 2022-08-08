from PyQt5.Qt import QSpinBox


class NewSpinbox(QSpinBox):

    def __init__(self, parent=None):
        super(NewSpinbox, self).__init__(parent)
        # self._dict = dict()
        self._dict = {0: 'first', 1: 'second'}
        self.setRange(0, 1)

    def get_dict(self, dict):
        self._dict = dict
        self.setRange(0, len(self._dict)-1)

    def textFromValue(self, p_int):
        # print('#'*10)
        # print(p_int)
        return self._dict.get(p_int)



