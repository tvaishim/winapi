import win32api
import win32con
import win32gui
import threading

import traymenu


VERSION = "ftps v.3.01 09.06.22"


class ThreadWindow(threading.Thread):
    def __init__(self, window):
        super(ThreadWindow, self).__init__()
        self._window = window

    def run(self):
        self._window.show()
        print("end of ThreadMainWindow")


class MainWindow:

    def __init__(self, parent_app):
        self._class_name = "MainWindow"
        self._parent_app = parent_app
        self._run = False
        self._window_class = None
        self._hwnd = None
        self._class_atom = None

    def is_open(self):
        return self._run

    def show(self):
        self._run = True
        # create and initialize window class
        self._window_class = win32gui.WNDCLASS()
        self._window_class.style = win32con.CS_HREDRAW | win32con.CS_VREDRAW
        self._window_class.lpfnWndProc = self.wndProc
        self._window_class.hInstance = self._parent_app.hInstance
        self._window_class.hIcon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
        self._window_class.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
        self._window_class.hbrBackground = win32gui.GetStockObject(win32con.WHITE_BRUSH)
        self._window_class.lpszClassName = self._class_name

        try:
            self._class_atom = win32gui.RegisterClass(self._window_class)
        except Exception as e:
            print(e)
            raise e

        self._hwnd = win32gui.CreateWindow(
            self._class_atom,  # it seems message dispatching only works with the atom, not the class name
            self._class_name,
            win32con.WS_OVERLAPPEDWINDOW,
            win32con.CW_USEDEFAULT,
            win32con.CW_USEDEFAULT,
            300,
            150,
            0,
            0,
            self._parent_app.hInstance,
            None)

        win32gui.ShowWindow(self._hwnd, win32con.SW_SHOWNORMAL)
        win32gui.UpdateWindow(self._hwnd)
        win32gui.SetActiveWindow(self._hwnd)

        while self._run:
            # lmsg = win32gui.PeekMessage(self._hwnd, 0, 0, win32con.PM_REMOVE)
            lmsg = win32gui.GetMessage(self._hwnd, 0, 0)
            # print(lmsg)
            if lmsg[0] == 1:
                msg = lmsg[1]
                win32gui.TranslateMessage(msg)
                win32gui.DispatchMessage(msg)
        print("end of loop ", self._class_name)


    def wndProc(self, hWnd, message, wParam, lParam):
        # print(message)
        if message == win32con.WM_CLOSE:
            print('win32con.WM_CLOSE')
            win32gui.DestroyWindow(self._hwnd)
            win32gui.UnregisterClass(self._class_atom, None)
            return 0

        elif message == win32con.WM_DESTROY:
            print('win32con.WM_DESTROY')
            self._run = False
            win32gui.PostQuitMessage(0)
            return 0

        elif message == win32con.WM_PAINT:
            hDC, paintStruct = win32gui.BeginPaint(hWnd)

            rect = win32gui.GetClientRect(hWnd)
            win32gui.DrawText(
                hDC,
                'Main Window',
                -1,
                rect,
                win32con.DT_SINGLELINE | win32con.DT_CENTER | win32con.DT_VCENTER)

            win32gui.EndPaint(hWnd, paintStruct)
            return 0

        else:
            return win32gui.DefWindowProc(hWnd, message, wParam, lParam)

    def hide(self):
        print("hide")
        # self._run = False
        win32gui.PostMessage(self._hwnd, win32con.WM_CLOSE, None, None)


class InfoWindow:
    def __init__(self, parent_app):
        self._class_name = "InfoWindow"
        self._parent_app = parent_app
        self._run = False
        self._window_class = None
        self._hwnd = None
        self._class_atom = None

    def is_open(self):
        return self._run

    def show(self):
        self._run = True
        # create and initialize window class
        self._window_class = win32gui.WNDCLASS()
        self._window_class.style = win32con.CS_HREDRAW | win32con.CS_VREDRAW
        self._window_class.lpfnWndProc = self.wndProc
        self._window_class.hInstance = self._parent_app.hInstance
        self._window_class.hIcon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
        self._window_class.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
        self._window_class.hbrBackground = win32gui.GetStockObject(win32con.WHITE_BRUSH)
        self._window_class.lpszClassName = self._class_name

        try:
            self._class_atom = win32gui.RegisterClass(self._window_class)
        except Exception as e:
            print(e)
            raise e

        self._hwnd = win32gui.CreateWindow(
            self._class_atom,  # it seems message dispatching only works with the atom, not the class name
            self._class_name,
            win32con.WS_OVERLAPPEDWINDOW,
            win32con.CW_USEDEFAULT,
            win32con.CW_USEDEFAULT,
            win32con.CW_USEDEFAULT,
            win32con.CW_USEDEFAULT,
            0,
            0,
            self._parent_app.hInstance,
            None)

        win32gui.ShowWindow(self._hwnd, win32con.SW_SHOWNORMAL)
        win32gui.UpdateWindow(self._hwnd)
        win32gui.SetActiveWindow(self._hwnd)
        win32gui.SetWindowPos(self._hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

        while self._run:
            # lmsg = win32gui.PeekMessage(self._hwnd, 0, 0, win32con.PM_REMOVE)
            lmsg = win32gui.GetMessage(self._hwnd, 0, 0)
            # print(lmsg)
            if lmsg[0] == 1:
                msg = lmsg[1]
                win32gui.TranslateMessage(msg)
                win32gui.DispatchMessage(msg)

        # win32gui.PumpMessages()
        print("end of loop ", self._class_name)

    def wndProc(self, hWnd, message, wParam, lParam):
        # print(message)
        if message == win32con.WM_CLOSE:
            print('win32con.WM_CLOSE')
            win32gui.DestroyWindow(self._hwnd)
            win32gui.UnregisterClass(self._class_atom, None)
            return 0

        elif message == win32con.WM_DESTROY:
            print('win32con.WM_DESTROY')
            self._run = False
            win32gui.PostQuitMessage(0)
            return 0

        elif message == win32con.WM_PAINT:
            hDC, paintStruct = win32gui.BeginPaint(hWnd)

            rect = win32gui.GetClientRect(hWnd)
            win32gui.DrawText(
                hDC,
                'info',
                -1,
                rect,
                win32con.DT_SINGLELINE | win32con.DT_CENTER | win32con.DT_VCENTER)

            win32gui.EndPaint(hWnd, paintStruct)
            return 0

        else:
            return win32gui.DefWindowProc(hWnd, message, wParam, lParam)

    def hide(self):
        print("hide")
        # self._run = False
        win32gui.PostMessage(self._hwnd, win32con.WM_CLOSE, None, None)


class App:
    def __init__(self):
        self.hInstance = win32api.GetModuleHandle()

        print(self.hInstance)

        self.main_window = MainWindow(self)
        self.info_window = InfoWindow(self)
        menu_options = (
            ("Main", self.menu_1),
            ("Info", self.menu_2),
            ("Выход", self.menu_3),
        )
        self.tray_menu = traymenu.SysTrayIcon("icon.ico", VERSION, menu_options)

        self.thread_menu = ThreadWindow(self.tray_menu)
        self.thread_menu.start()

        print("end APP")

    def menu_1(self):
        if not self.main_window.is_open():
            self.thread_main_window = ThreadWindow(self.main_window)
            self.thread_main_window.start()

    def menu_2(self):
        if not self.info_window.is_open():
            self.thread_info_window = ThreadWindow(self.info_window)
            self.thread_info_window.start()

    def menu_3(self):
        if self.main_window.is_open():
            print("main_window.hide")
            self.main_window.hide()
        if self.info_window.is_open():
            print("info_window.hide")
            self.info_window.hide()
        if self.tray_menu.is_open():
            print("tray_menu.hide")
            self.tray_menu.hide()


if __name__ == '__main__':
    app = App()
