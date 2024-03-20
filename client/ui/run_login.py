from PySide6.QtWidgets import QApplication, QWidget
from client.ui.login import Ui_Form  # Import the UI class


class LoginForm(QWidget, Ui_Form):
    """
    This class represents the login form of the application, inheriting from QWidget and the generated Ui_Form.
    """

    def __init__(self, parent=None):
        super(LoginForm, self).__init__(parent)
        self.setupUi(self)  # Initialize the UI


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    form = LoginForm()
    form.show()
    sys.exit(app.exec())
