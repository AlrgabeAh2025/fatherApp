import flet as ft
from PIL import ImageGrab
import time

def main(page: ft.Page):
    page.title = "التقاط صورة للشاشة باستخدام Flet وPillow"
    page.window_always_on_top = True

    def take_screenshot(e):
        # التقاط صورة للشاشة
        screenshot = ImageGrab.grab()
        # حفظ الصورة في ملف
        timestamp = int(time.time())
        file_path = f"screenshot_{timestamp}.png"
        screenshot.save(file_path)
        # عرض الصورة في التطبيق
        page.image_container.controls.append(ft.Image(src=file_path, fit="contain"))
        page.update()

    # زر لالتقاط الصورة
    capture_button = ft.ElevatedButton("التقاط صورة للشاشة", on_click=take_screenshot)
    # حاوية لعرض الصور الملتقطة
    page.image_container = ft.Column()
    # إضافة العناصر إلى الصفحة
    page.add(capture_button, page.image_container)
    page.scroll = "auto"

ft.app(target=main)
