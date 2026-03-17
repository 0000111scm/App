import flet as ft
import os
import threading

def main(page: ft.Page):
    page.title = "Optimizer S24 FE"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#000000"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20
    page.window_prevent_close = True

    icone = ft.Icon(ft.icons.SPEED, color="#0a84ff", size=80)
    titulo = ft.Text("OTIMIZADOR S24 FE", size=28, weight="bold", color="#ffffff")
    status_text = ft.Text("STATUS: AGUARDANDO", color="#555555", size=14)
    btn_executar = ft.ElevatedButton(
        "EXECUTAR OTIMIZAÇÃO",
        style=ft.ButtonStyle(
            bgcolor="#0a84ff",
            color="#ffffff",
            padding=20,
            shape=ft.RoundedRectangleBorder(radius=10)
        )
    )
    btn_perm = ft.TextButton(
        "CONFIGURAR PERMISSÕES",
        on_click=lambda e: page.request_permission(ft.PermissionType.MANAGE_EXTERNAL_STORAGE)
    )

    page.add(
        ft.Column([
            icone,
            titulo,
            ft.Container(height=20),
            status_text,
            ft.Container(height=30),
            btn_executar,
            ft.Container(height=10),
            btn_perm,
            ft.Divider(color="#1c1c1e", height=40),
            ft.Text("© 2026 - Engine Pro", color="#8e8e93", size=12)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5)
    )

    def atualizar_status(msg, cor="#555555"):
        status_text.value = msg
        status_text.color = cor
        page.update()

    def tarefa_otimizacao():
        atualizar_status("VARRENDO ARQUIVOS...", "#0a84ff")
        extensoes = ['.tmp', '.log', '.cache', '.temp', '.thumb', '.bak', '.old']
        base_paths = ["/storage/emulated/0/"]
        total_liberto = 0
        arquivos_removidos = 0

        for base in base_paths:
            if not os.path.exists(base):
                continue
            try:
                for root, dirs, files in os.walk(base):
                    if any(p in root for p in ["/Android/data/", "/Android/obb/", "/."]):
                        continue
                    for file in files:
                        if any(file.lower().endswith(ext) for ext in extensoes):
                            caminho = os.path.join(root, file)
                            try:
                                tam = os.path.getsize(caminho)
                                os.remove(caminho)
                                total_liberto += tam
                                arquivos_removidos += 1
                            except:
                                pass
            except Exception as e:
                print(f"Erro: {e}")

        if total_liberto > 0:
            mb = total_liberto / (1024 * 1024)
            atualizar_status(f"LIBERTADO: {mb:.2f} MB ({arquivos_removidos} ARQUIVOS)", "#30d158")
        else:
            atualizar_status("NENHUM ARQUIVO ENCONTRADO", "#ff9f0a")
        btn_executar.disabled = False
        page.update()

    def executar_click(e):
        btn_executar.disabled = True
        page.update()
        threading.Thread(target=tarefa_otimizacao, daemon=True).start()

    btn_executar.on_click = executar_click

    def on_perm_result(e):
        if e.granted:
            atualizar_status("PERMISSÃO CONCEDIDA", "#30d158")
        else:
            atualizar_status("PERMISSÃO NEGADA", "#ff453a")
    page.on_permission_result = on_perm_result

ft.app(target=main)
