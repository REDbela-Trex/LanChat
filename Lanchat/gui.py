import flet as ft
from server import start_tcp_server, start_udp_broadcast
from client import scan_lan_servers, connect_to_server, send_message

def start_gui(page: ft.Page):
    page.title = "Modüler LAN Chat"
    
    chat_display = ft.Column(scroll="auto", expand=True)
    message_box = ft.TextField(hint_text="Mesaj yaz...", expand=True)
    username_box = ft.TextField(label="Kullanıcı Adı", value="Ben", expand=True)
    
    server_list_column = ft.Column(scroll="auto", expand=True)
    client_sock = {"sock": None}
    
    def update_ui(msg):
        chat_display.controls.append(ft.Text(msg))
        page.update()
    
    def update_server_list(servers):
        server_list_column.controls.clear()
        for ip, name in servers.items():
            def make_connect(ip=ip, port=int(name.split("(")[1][:-1])):
                return lambda e: connect(ip, port)
            server_list_column.controls.append(ft.ElevatedButton(name, on_click=make_connect()))
        page.update()
    
    def start_server_click(e):
        threading.Thread(target=start_tcp_server, args=(update_ui,), daemon=True).start()
        threading.Thread(target=start_udp_broadcast, args=("BenimSunucum",), daemon=True).start()
    
    def connect(ip, port):
        sock = connect_to_server(ip, port, update_ui)
        client_sock["sock"] = sock
    
    def send_msg(e):
        msg = message_box.value.strip()
        if not msg:
            return
        full_msg = f"{username_box.value}: {msg}"
        if client_sock["sock"]:
            send_message(client_sock["sock"], full_msg)
        else:
            update_ui(full_msg)
        message_box.value = ""
        message_box.focus()
        page.update()

        message_box.on_submit = send_msg
    
    page.add(
        ft.Row([username_box]),
        ft.Row([ft.ElevatedButton("Sunucuyu Başlat", on_click=start_server_click)]),
        ft.Text("LAN’daki Sunucular:"),
        server_list_column,
        chat_display,
        ft.Row([message_box, ft.IconButton(icon=ft.Icons.SEND, on_click=send_msg)])
    )
    
    import threading
    threading.Thread(target=scan_lan_servers, args=(update_server_list,), daemon=True).start()
    
def run():
    ft.app(target=start_gui)
