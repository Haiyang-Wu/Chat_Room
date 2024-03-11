"""
core logic

"""

import socket
import pickle
import sys

from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox, QLabel, QListWidgetItem
from PyQt6.QtCore import Qt, QCoreApplication


from lib.common import *
from ui.login import Ui_Form as LoginUiMixin
from ui.chat import Ui_Form as ChatUiMixin


class MySocket:
    def __init__(self, host='localhost', port=9000):
        self.host = host
        self.port = port
        self.user = None
        self.token = None
        self.online_users = tuple()
        self.socket = None


    def send(self, data):
        self.socket.send(data)

    def recv(self, recv_len):
        return self.socket.recv(recv_len)


    def recv_data(self):
        len_bytes = self.recv(PROTOCOL_LENGTH)
        if not len_bytes:
            raise ConnectionResetError
        stream_len = int.from_bytes(len_bytes, byteorder='big')
        dic_bytes = bytes()
        while stream_len > 0:
            if stream_len < 4096:
                temp = self.recv(stream_len)
            else:
                temp = self.recv(4096)
            if not temp:
                raise ConnectionResetError
            dic_bytes += temp
            stream_len -= len(temp)
        response_dic = pickle.loads(dic_bytes)
        return response_dic

        # receive data of file


    def send_data(self, dic):
        dic_bytes = pickle.dumps(dic)
        len_bytes = len(dic_bytes).to_bytes(PROTOCOL_LENGTH, byteorder='big')
        self.send(len_bytes)
        self.send(dic_bytes)
        LOGGER.debug('send dictionary successfully')
        if dic.get('mode') != REQUEST_FILE:
            return

        # send files

    def connect(self):
        for i in range(1,4):
            try:
                self.socket = socket.socket()
                self.socket.connect((self.host, self.port))
                LOGGER.debug('connected to server successfully!')
                return True
            except Exception as e:
                ERROR_LOGGER.error('fail to connect to server, reconnect times:{}! {}'.format(i, e))
                self.socket.close()

    def close(self):
        self.socket.close()

    def __enter__(self):
        if self.connect():
            return self
        else:
            exit()
            # return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class LoginWindow(LoginUiMixin, QWidget):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.setupUi(self)
        self.tip_label = QLabel()
        self.tip_label.setWindowFlag(Qt.WindowType.FramelessWindowHint)  # hide the windows
        self.tip_label.setWindowModality(Qt.WindowModality.ApplicationModal)  # model windows
        self.tip_label.setStyleSheet("background-color: gray")

        self.chat_window = None

    @reconnect
    def get(self,dic):
        self.client.send_data(dic)  # send data
        # wait the result of registration
        response_dic = self.client.recv_data()  # receive data
        return response_dic



    def register(self):
        LOGGER.debug('register')
        user = self.lineEdit_3.text().strip()
        pwd = self.lineEdit_4.text().strip()
        re_pwd = self.lineEdit_5.text().strip()
        if not user or not pwd or not re_pwd:
            QMessageBox.warning(self, 'WARNING', 'PLEASE ENTER ENTIRELY!')
            return
        if pwd != re_pwd:
            QMessageBox.warning(self, 'WARNING', 'TWO PASSWORDS DO NOT MATCH!')
            return
        request_dic = RequestData.register_dic(user, pwd)
        response_dic = self.get(request_dic)
        if not response_dic:    # reconnected successfully
            return
        QMessageBox.about(self, 'hint', response_dic.get('msg'))
        if response_dic.get('code') != 200:
            return

        self.lineEdit_3.setText('')
        self.lineEdit_4.setText('')
        self.lineEdit_5.setText('')
        self.open_login_page()
        self.lineEdit.setText(user)
        self.lineEdit_2.setFocus()



    def login(self):
        LOGGER.debug('login')
        user = self.lineEdit.text().strip()
        pwd = self.lineEdit_2.text().strip()
        if not user or not pwd:
            QMessageBox.warning(self, 'WARNING', 'PLEASE ENTER ENTIRELY!')
            return
        if not self.checkBox.isChecked():
            QMessageBox.warning(self, 'WARNING', 'PLEASE TICK SERVICE CONTRACT!')
            return

        request_dic = RequestData.login_dic(user, pwd)
        response_dic = self.get(request_dic)
        if not response_dic:  # reconnected successfully
            return
        if response_dic.get('code') != 200:
            QMessageBox.about(self, 'hint', response_dic.get('msg'))
            return

        self.client.user = user
        self.client.token = response_dic.get('token')
        notice = response_dic.get('notice')
        users = response_dic.get('users')
        # open the chat window, close the login window
        self.chat_window = ChatWindow(self, notice, users)
        self.chat_window.show()
        self.close()



    def open_register_page(self):
        LOGGER.debug('open register page')
        self.stackedWidget.setCurrentIndex(1)

    def open_login_page(self):
        LOGGER.debug('open login page')
        self.stackedWidget.setCurrentIndex(0)

    def protocol(self):
        LOGGER.debug('check protocol')
        QMessageBox.about(self, 'service contract', 'this program is a cooperate coursework!')


class ChatWindow(ChatUiMixin, QWidget):
    def __init__(self, login_window, notice, users):
        super().__init__()
        self.client = login_window.client
        self.login_window = login_window
        self.setupUi(self)
        self.tip_label = QLabel()
        self.tip_label.setWindowFlag(Qt.WindowType.FramelessWindowHint)  # hide the windows
        self.tip_label.setWindowModality(Qt.WindowModality.ApplicationModal)  # model windows
        self.tip_label.setStyleSheet("background-color: gray")

        self.label.close()
        self.textBrowser.clear()
        self.textEdit.clear()
        self.textEdit_2.setText(notice)
        self.set_online_users(users)

    def set_online_users(self, users):
        self.listWidget.clear()
        _translate = QCoreApplication.translate
        self.label_3.setText('Online users: {}'.format(len(users)))
        for user in users:
            item = QListWidgetItem()
            self.listWidget.addItem(item)
            item.setText(_translate("Form", user))





def run():
    import sys
    # connect server
    with MySocket(HOST, PORT)as client:
        # show interface of log in
        app = QApplication(sys.argv)
        login_window = LoginWindow(client)
        login_window.show()
        sys.exit(app.exec())