import ctypes
from ctypes import cdll, c_void_p, c_char_p, c_float, c_int, c_uint, c_uint16, c_uint32, c_int32, c_size_t

TEXT_ALIGN_LEFT = 0
TEXT_ALIGN_RIGHT = 1
TEXT_ALIGN_CENTER = 2

FONT_STYLE_REGULAR = 0,
FONT_STYLE_ITALIC = 1,
FONT_STYLE_BOLD = 2,
FONT_STYLE_UNDERLINE = 4

QNI_ENTRY_CALLBACK = ctypes.CFUNCTYPE(None, c_void_p)


class QniBinding():
    def __init__(self):
        self.core = cdll.LoadLibrary('libqni.core.so')
        self.connector_ws = cdll.LoadLibrary('libqni.connector.ws.so')

        self.core.qni_hub_new.argtypes = [QNI_ENTRY_CALLBACK]
        self.core.qni_hub_new.restype = c_void_p
        self.core.qni_hub_exit.argtypes = [c_void_p]
        self.core.qni_hub_delete.argtypes = [c_void_p]

        self.core.qni_print.argtypes = [c_void_p, c_char_p, c_size_t]
        self.core.qni_print_line.argtypes = [c_void_p, c_char_p, c_size_t]
        self.core.qni_new_line.argtypes = [c_void_p]
        self.core.qni_delete_line.argtypes = [c_void_p, c_uint32]
        self.core.qni_set_font.argtypes = [
            c_void_p, c_char_p, c_size_t, c_float, c_uint]
        self.core.qni_set_text_align.argtypes = [c_void_p, c_uint32]
        self.core.qni_set_text_color.argtypes = [c_void_p, c_uint32]
        self.core.qni_set_back_color.argtypes = [c_void_p, c_uint32]
        self.core.qni_set_highlight_color.argtypes = [c_void_p, c_uint32]

        self.core.qni_wait_int.argtypes = [c_void_p]
        self.core.qni_wait_int.restype = c_int32

        self.connector_ws.qni_connector_ws_start.argtypes = [
            c_void_p, c_char_p, c_uint16, c_int]

        self.connector_ws.qni_connector_ws_start.restype = c_int

    def hub_new(self, entry: QNI_ENTRY_CALLBACK):
        return self.core.qni_hub_new(entry)

    def hub_exit(self, hub: c_void_p):
        self.core.qni_hub_exit(hub)

    def hub_delete(self, hub: c_void_p):
        self.core.qni_hub_delete(hub)

    def wait_int(self, ctx: c_void_p):
        return self.core.qni_wait_int(ctx)

    def print(self, ctx: c_void_p, text: str):
        text = text.encode('utf-8')
        self.core.qni_print(ctx, text, len(text) + 1)

    def print_line(self, ctx: c_void_p, text: str):
        text = text.encode('utf-8')
        self.core.qni_print_line(
            ctx, text, len(text) + 1)

    def new_line(self, ctx: c_void_p):
        self.core.qni_new_line(ctx)

    def delete_line(self, ctx: c_void_p, count: int):
        self.core.qni_delete_line(ctx, count)

    def set_font(self, ctx: c_void_p, font_family: str, font_size: float, font_style: int):
        font_family = font_family.encode('utf-8')
        self.core.qni_set_font(ctx, font_family, len(
            font_family) + 1, font_size, font_style)

    def set_text_align(self, ctx: c_void_p, align: int):
        self.core.qni_set_text_align(ctx, align)

    def set_text_color(self, ctx: c_void_p, color: int):
        self.core.qni_set_text_color(ctx, color)

    def set_back_color(self, ctx: c_void_p, color: int):
        self.core.qni_set_back_color(ctx, color)

    def set_highlight_color(self, ctx: c_void_p, color: int):
        self.core.qni_set_highlight_color(ctx, color)

    def connector_ws_start(self, hub: c_void_p, host: str, port: int, epoll_size: int):
        return self.connector_ws.qni_connector_ws_start(hub, host.encode('utf-8'), port, epoll_size)
