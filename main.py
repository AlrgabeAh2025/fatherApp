import flet as ft
import os
import time
from flet_core import FilePicker

def main(page: ft.Page):
    page.title = "التقاط صورة للشاشة باستخدام Flet"
    page.window_always_on_top = True

    def take_screenshot(e):
        # اسم الملف مع التوقيت
        timestamp = int(time.time())
        file_name = f"screenshot_{timestamp}.png"
        
        # تحديد المسار المناسب على أندرويد
        save_dir = "/storage/emulated/0/Pictures/FletScreenshots"
        os.makedirs(save_dir, exist_ok=True)
        file_path = os.path.join(save_dir, file_name)

        # محاكاة حفظ الصورة
        with open(file_path, "wb") as f:
            f.write(b"This is a placeholder for the screenshot data.")  # استبدل هذا بالبيانات الحقيقية
        
        # تحديث واجهة التطبيق
        page.image_container.controls.append(ft.Text(f"تم حفظ الصورة: {file_path}"))
        page.update()

    # زر لالتقاط الصورة
    capture_button = ft.ElevatedButton("التقاط صورة للشاشة", on_click=take_screenshot)
    
    # حاوية لعرض الصور أو الرسائل
    page.image_container = ft.Column()
    
    # إضافة العناصر إلى الصفحة
    page.add(capture_button, page.image_container)
    page.scroll = "auto"

ft.app(target=main)
