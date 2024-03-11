"""
core logic

"""

import socket
import time
import pickle
import sys

from PyQt6.QtGui import QTextCursor
from PyQt6.QtWidgets import QApplication, QWidget, QTextEdit, QLabel, QListWidgetItem
from PyQt6.QtCore import Qt, QCoreApplication, QThread, QEventLoop, pyqtSignal, QTimer, QMargins

from lib.common import *
from ui.login import Ui_Form as LoginUiMixin
from ui.chat import Ui_Form as ChatUiMixin

class MyTextEdit(QTextEdit):
    returnPressed = pyqtSignal()

    def keyPressEvent(self, e) -> None:
        if e.key() == Qt.Key.Key_Return and not e.modifiers():
            self.returnPressed.emit()
            return
        super().keyPressEvent(e)



class MySocket:
    def __init__(self, host='localhost', port=9000):
        self.host = host
        self.port = port
        self.user = None
        self.token = None
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
            time.sleep(2)

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
    _translate = QCoreApplication.translate

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

        self.route_mode = {
            'reconnect': self.reconnect_res,
            'broadcast': self.broadcast_res,
            'chat': self.chat_res
        }
        self.signal_route ={
            'show_tip': self.show_tip,
            'close_tip': self.tip_label.close,
            'over': self.over
        }

        # pytz, dateutil, ....
        self.last_time = datetime.utcfromtimestamp(0).replace(tzinfo=timezone.utc).astimezone().replace(tzinfo=None)

        self.my_thread = MyThread(self.client)
        self.my_thread.reconnected.connect(self.t_signal)
        self.my_thread.received.connect(self.dic_handle)
        self.my_thread.start()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.close_broadcast)
        self.textEdit.returnPressed.connect(self.send_msg)

        self.textBrowser.setViewportMargins(QMargins(0, 0, 8, 0))

    @reconnect
    def put(self, request_dic):
        self.client.send_data(request_dic)
        return True

    def send_msg(self):
        msg = self.textEdit.toPlainText().strip()
        if not msg:
            QMessageBox.warning(self, 'WARNING', 'Message cannot be empty')
            return
        request_dic = RequestData.chat_dic(self.client.user, msg, self.client.token)
        if not self.put(request_dic):
            return
        self.textEdit.setText('')

        self.append_time(request_dic.get('time'))

        cursor = self.textBrowser.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.textBrowser.setTextCursor(cursor)
        self.textBrowser.insertHtml(f"""
        <tr style="text-align:right">
        <p>
        <a style="color:{USER_COLOR}">ME</a>
        <br>
        <a style="color:{MSG_COLOR}">{msg}</a>
        </p>
        </tr>
        """)
        LOGGER.info('ME says: {}'.format(msg))

    def dic_handle(self, response_dic):
        fn = self.route_mode.get(response_dic.get('mode'))
        fn(response_dic)

    def append_time(self, local_time):
        if (local_time - self.last_time).total_seconds() > INTERVAL:
            cursor = self.textBrowser.textCursor()
            cursor.movePosition(cursor.MoveOperation.End)
            self.textBrowser.setTextCursor(cursor)
            self.textBrowser.insertHtml(f"""
                            <tr style="text-align:center">
                            <p>
                            <a style="color:{USER_COLOR}">{local_time}</a>
                            </p>
                            </tr>
                            """)
        self.last_time = local_time

    def chat_res(self, response_dic, *args, **kwargs):
        user = response_dic.get('user')
        msg = response_dic.get('msg')
        utc_time = response_dic.get('time')
        local_time = utc_time.astimezone().replace(tzinfo=None)
        self.append_time(local_time)
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.textBrowser.setTextCursor(cursor)
        self.textBrowser.insertHtml(f"""
                <tr style="text-align:left">
                <p>
                <a style="color:{USER_COLOR}">{user}</a>
                <br>
                <a style="color:{MSG_COLOR}">{msg}</a>
                
                </p>
                </tr>
                """)
        LOGGER.info('{} says: {}'.format(user, msg))

    def reconnect_res(self, response_dic, *args, **kwargs):
        code = response_dic.get('code')
        if code != 200:
            QMessageBox.warning(self, 'hint', '{}\nstatus_code: {}'.format(
                response_dic.get('msg'), code
            ))
            self.login_window.show()
            self.close()
            return

        users = response_dic.get('users')
        self.set_online_users(users)

    def close_broadcast(self):
        # hide the broadcast label
        self.label.close()
        self.timer.stop()

    def broadcast_res(self, response_dic, *args, **kwargs):
        user = response_dic.get('user')
        if response_dic.get('status') == REQUEST_ONLINE:
            if self.listWidget.findItems(user, Qt.MatchFlag.MatchExactly):
                return

            item = QListWidgetItem()
            self.listWidget.addItem(item)
            if user == self.client.user:
                user = 'ME'
            item.setText(self._translate("Form", user))

            self.label_3.setText('Online users: {}'.format(self.listWidget.count()))

            self.label.show()
            self.label.setText('{} have entered the chat room'.format(user))
        else:
            item = self.listWidget.findItems(user, Qt.MatchFlag.MatchExactly)[0]
            self.listWidget.takeItem(self.listWidget.row(item))
            self.label_3.setText('Online users: {}'.format(self.listWidget.count()))

            self.label.show()
            self.label.setText('{} have left the chat room'.format(user))
        self.timer.start(5000)


    def set_online_users(self, users):
        self.listWidget.clear()
        self.label_3.setText('Online users: {}'.format(len(users)))
        for user in users:
            item = QListWidgetItem()
            self.listWidget.addItem(item)
            if user == self.client.user:
                user = 'ME'
            item.setText(self._translate("Form", user))

    def t_signal(self, s):
        self.signal_route.get(s)()

    def show_tip(self):
        self.tip_label.setText('Connection down, reconnecting...')
        self.tip_label.adjustSize()
        self.tip_label.setFixedSize(self.tip_label.size())
        self.tip_label.show()

        x = self.geometry().center().x()
        y = self.geometry().center().y()
        self.tip_label.move(x - self.tip_label.width() / 2, y - self.tip_label.height() / 2)

    def over(self):
        QMessageBox.warning(self, 'hint', 'Fail to connect to server, program will be terminated')
        exit()


class MyThread(QThread):
    reconnected = pyqtSignal(str)
    received = pyqtSignal(dict)

    def __init__(self, client):
        self.client = client
        super().__init__()

    def run(self):
        self.loop_recv()

    @reconnect_t
    def get(self):
        return self.client.recv_data()

    @reconnect_t
    def put(self, dic):
        self.client.send_data(dic)
        return True

    def loop_recv(self):
        while True:
            response_dic = self.get()
            if not response_dic:
                # if reconnected, send request to update data
                while True:
                    request_dic = RequestData.reconnect_dic(self.client.user, self.client.token)
                    if not self.put(request_dic):
                        continue
                    LOGGER.info('Reconnect dictionary send successfully!')
                    break
                continue
            self.received.emit(response_dic)




def run():
    import sys
    # connect server
    with MySocket(HOST, PORT)as client:
        # show interface of log in
        app = QApplication(sys.argv)
        login_window = LoginWindow(client)
        login_window.show()
        sys.exit(app.exec())