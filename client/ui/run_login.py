from PySide6.QtWidgets import QApplication, QWidget
from ui.login import Ui_Form  # 导入 UI 类

class LoginForm(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(LoginForm, self).__init__(parent)
        self.setupUi(self)  # 初始化 UI

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = LoginForm()
    form.show()
    sys.exit(app.exec())
