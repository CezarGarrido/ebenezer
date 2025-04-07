import json
import os
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk, WebKit2, Gdk, GLib

CONFIG_PATH = "config.json"

def load_server_url():
    if not os.path.exists(CONFIG_PATH):
        return None
    with open(CONFIG_PATH) as f:
        data = json.load(f)
        return data.get("server_url")

def save_server_url(url):
    with open(CONFIG_PATH, "w") as f:
        json.dump({"server_url": url}, f)

class UrlDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Configurar URL do servidor", parent, 0)
        self.set_default_size(400, 100)

        box = self.get_content_area()
        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("http://192.168.1.100:8000")
        box.add(self.entry)

        self.add_button("Cancelar", Gtk.ResponseType.CANCEL)
        self.add_button("Salvar", Gtk.ResponseType.OK)
        self.show_all()

    def get_url(self):
        return self.entry.get_text()

class BrowserWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Cliente Django")
        self.set_default_size(1024, 768)

        # Cor de fundo
        rgba = Gdk.RGBA()
        rgba.parse("#f0f0f0")

        self.webview = WebKit2.WebView()
        self.webview.set_background_color(rgba)

        self.loading_overlay = Gtk.Overlay()
        self.loading_overlay.add(self.webview)

        # Label de carregando
        self.loading_label = Gtk.Label(label="Carregando...")
        self.loading_label.get_style_context().add_class("title")
        self.loading_overlay.add_overlay(self.loading_label)
        self.loading_label.set_halign(Gtk.Align.CENTER)
        self.loading_label.set_valign(Gtk.Align.CENTER)
        self.loading_label.set_visible(False)

        self.add(self.loading_overlay)
        self.connect("key-press-event", self.on_key_press)

        # Sinal para saber quando começa e termina o carregamento
        self.webview.connect("load-changed", self.on_load_changed)

        server_url = load_server_url()
        if server_url:
            self.webview.load_uri(server_url)
        else:
            self.show_config_dialog()

    def show_loading(self, visible):
        self.loading_label.set_visible(visible)

    def on_load_changed(self, webview, load_event):
        if load_event == WebKit2.LoadEvent.STARTED:
            self.show_loading(True)
        elif load_event == WebKit2.LoadEvent.FINISHED:
            self.show_loading(False)

    def show_config_dialog(self):
        dialog = UrlDialog(self)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            url = dialog.get_url()
            if url:
                save_server_url(url)
                self.webview.load_uri(url)

        dialog.destroy()

    def on_key_press(self, widget, event):
        if event.keyval == 65471:  # F2
            self.show_config_dialog()

def main():
    win = BrowserWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
