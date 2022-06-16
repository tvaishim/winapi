import os
import win32con
import win32gui_struct
import win32gui


class SysTrayIcon(object):

    FIRST_ID = 1023

    def __init__(self, icon, hover_text, menu_options):

        self._hInstance = win32gui.GetModuleHandle(None)
        self._icon = icon
        self._hover_text = hover_text
        self._class_name = "SysTrayIconPy"
        self._menu = {self.FIRST_ID + i: menu_options[i] for i in range(len(menu_options))}
        self._window_class = None
        self._hwnd = None
        self._class_atom = None
        self._run = False

        print("menu ", self._hInstance)

    def is_open(self):
        return self._run

    def show(self):
        self._run = True
        # Register the Window class.
        self._window_class = win32gui.WNDCLASS()
        self._window_class.hInstance = self._hInstance
        self._window_class.lpszClassName = self._class_name
        self._window_class.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW
        self._window_class.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
        self._window_class.hbrBackground = win32con.COLOR_WINDOW
        self._window_class.lpfnWndProc = self.wndProc

        try:
            self._class_atom = win32gui.RegisterClass(self._window_class)
        except Exception as e:
            print(e)
            raise e

        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self._hwnd = win32gui.CreateWindow(
            self._class_atom,
            self._class_name,
            style,
            0,
            0,
            win32con.CW_USEDEFAULT,
            win32con.CW_USEDEFAULT,
            0,
            0,
            self._hInstance,
            None
        )

        win32gui.UpdateWindow(self._hwnd)
        hicon = self._load_icon(self._icon)
        message = win32gui.NIM_ADD
        notify_id = (
            self._hwnd,
            0,
            win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP,
            win32con.WM_USER + 20,
            hicon,
            self._hover_text
        )
        win32gui.Shell_NotifyIcon(message, notify_id)

        while self._run:
            # lmsg = win32gui.PeekMessage(self._hwnd, 0, 0, win32con.PM_REMOVE)
            lmsg = win32gui.GetMessage(self._hwnd, 0, 0)
            # print(lmsg)
            if lmsg[0] == 1:
                msg = lmsg[1]
                win32gui.TranslateMessage(msg)
                win32gui.DispatchMessage(msg)

        # win32gui.PumpMessages()

        print("end of loop")

    def hide(self):
        print("hide")
        win32gui.PostMessage(self._hwnd, win32con.WM_CLOSE, None, None)

    def wndProc(self, hWnd, message, wParam, lParam):

        if message == win32con.WM_CLOSE:
            print('win32con.WM_CLOSE')
            win32gui.DestroyWindow(self._hwnd)
            win32gui.UnregisterClass(self._class_atom, None)
            return 0

        elif message == win32con.WM_DESTROY:
            print('win32con.WM_DESTROY')
            nid = (hWnd, 0)
            win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
            self._run = False
            win32gui.PostQuitMessage(0)
            return 0

        elif message == win32con.WM_COMMAND:
            print('win32con.WM_COMMAND')
            pid = win32gui.LOWORD(wParam)
            menu_action = self._menu[pid][1]
            menu_action()
            return 0

        elif message == win32con.WM_USER + 20:
            if lParam == win32con.WM_RBUTTONUP:
                self._show_menu()
            return 0

        else:
            return win32gui.DefWindowProc(hWnd, message, wParam, lParam)

    def _load_icon(self, icon):
        if os.path.isfile(icon):
            icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
            hicon = win32gui.LoadImage(
                self._hInstance,
                icon,
                win32con.IMAGE_ICON,
                0,
                0,
                icon_flags
            )
        else:
            hicon = win32gui.LoadIcon(
                0,
                win32con.IDI_APPLICATION
            )
        return hicon

    def _show_menu(self):
        hmenu = win32gui.CreatePopupMenu()

        menu_items = list(self._menu.items())
        menu_items.reverse()

        for mid, mval in menu_items:
            item, extras = win32gui_struct.PackMENUITEMINFO(text=mval[0], wID=mid)
            win32gui.InsertMenuItem(hmenu, 0, 1, item)

        pos_x, pos_y = win32gui.GetCursorPos()
        win32gui.SetForegroundWindow(self._hwnd)
        win32gui.TrackPopupMenu(
            hmenu,
            win32con.TPM_LEFTALIGN,
            pos_x - 50,
            pos_y - 5,
            0,
            self._hwnd,
            None
        )
        win32gui.PostMessage(
            self._hwnd,
            win32con.WM_NULL,
            0,
            0
        )
