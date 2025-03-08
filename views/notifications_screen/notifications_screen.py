# استيراد المكتبات الضرورية
from flet import *
import requests

# تعريف فئة MoreInfoAboutNotifications التي تمثل شاشة تفاصيل التنبيه
class MoreInfoAboutNotifications(View):
    def __init__(self, route, page):
        super().__init__(route=route)  # استدعاء دالة البناء للفئة الأم (View)
        self.scroll = ScrollMode.AUTO  # تعيين وضع التمرير إلى تلقائي
        self.bgcolor = "#ffffff"  # لون الخلفية
        self.page = page  # حفظ صفحة التطبيق

        # تعريف AppBar (شريط التطبيق العلوي)
        self.appbar = AppBar(
            leading=IconButton(
                icon=icons.ARROW_BACK,
                icon_color="#ffffff",
                on_click=lambda x: self.page.go("/notifications"),  # حدث النقر للرجوع إلى صفحة الإشعارات
            ),
            title=Text(
                "حماية الاطفال",
                size=20,
                weight=FontWeight.BOLD,
                color="#ffffff",
                font_family="ElMessiri",
            ),
            toolbar_height=100,
        )

    # دالة تُستدعى عند تحميل الواجهة
    def did_mount(self):
        loader = self.loaderUi()  # عرض واجهة التحميل
        self.controls.clear()
        self.controls.append(loader)
        self.update()
        self.loadNote()  # تحميل تفاصيل التنبيه

    # دالة لبناء واجهة تفاصيل التنبيه
    def buildUi(self, note):
        self.scroll = ScrollMode.AUTO
        self.controls.clear()
        self.controls.append(
            ResponsiveRow(
                controls=[
                    Container(height=20),
                    Text(
                        "معلومات التنبيه",
                        style=TextStyle(
                            size=12,
                            weight=FontWeight.BOLD,
                            font_family="ElMessiri",
                        ),
                        color="#666666",
                        expand=True,
                        text_align=TextAlign.CENTER,
                    ),
                    Container(
                        content=Column(
                            controls=[
                                ResponsiveRow(
                                    controls=[
                                        Container(
                                            content=ListTile(
                                                leading=Icon(icons.PERSON),
                                                title=Text(
                                                    f"تنبيه بخصوص ابنك {note['child_first_name']}",
                                                    style=TextStyle(
                                                        size=15,
                                                        weight=FontWeight.BOLD,
                                                        font_family="ElMessiri",
                                                    ),
                                                ),
                                                subtitle=Text(
                                                    "ابنك يشاهد محتوى مقيد بالفئة العمرية",
                                                    style=TextStyle(
                                                        size=8,
                                                        weight=FontWeight.BOLD,
                                                        font_family="ElMessiri",
                                                    ),
                                                ),
                                            ),
                                        ),
                                    ],
                                ),
                                ResponsiveRow(
                                    controls=[
                                        Container(
                                            content=ListTile(
                                                leading=Icon(icons.TIMER),
                                                title=Text(
                                                    "وقت حدوث البلاغ",
                                                    style=TextStyle(
                                                        size=15,
                                                        weight=FontWeight.BOLD,
                                                        font_family="ElMessiri",
                                                    ),
                                                ),
                                                subtitle=Text(
                                                    f"{note['dateOfNotification']}",
                                                    style=TextStyle(
                                                        size=10,
                                                        weight=FontWeight.BOLD,
                                                        font_family="ElMessiri",
                                                    ),
                                                ),
                                            ),
                                        ),
                                    ],
                                ),
                                ResponsiveRow(
                                    controls=[
                                        Container(
                                            content=ListTile(
                                                leading=Icon(icons.IMAGE),
                                                title=Text(
                                                    "محتوى البلاغ",
                                                    style=TextStyle(
                                                        size=15,
                                                        weight=FontWeight.BOLD,
                                                        font_family="ElMessiri",
                                                    ),
                                                ),
                                                subtitle=Text(
                                                    "محتوى الشاشة الذي تم التقاطه",
                                                    style=TextStyle(
                                                        size=10,
                                                        weight=FontWeight.BOLD,
                                                        font_family="ElMessiri",
                                                    ),
                                                ),
                                            ),
                                        ),
                                    ],
                                ),
                                Container(
                                    content=Image(
                                        src=f"{MoreInfoAboutNotifications.baseUrl}{note['imageOfNotification'].replace('/uploads_images' , '')}",
                                        width=150,
                                    ),
                                    border_radius=border_radius.all(10),
                                    width=300,
                                ),
                            ],
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            alignment=MainAxisAlignment.CENTER,
                        ),
                        bgcolor="#ffffff",
                        border=border.all(0.5, "#110b22"),
                        border_radius=border_radius.all(5),
                    ),
                ],
                expand=True,
            )
        )
        self.update()

    # دالة لعرض واجهة التحميل
    def loaderUi(self):
        self.scroll = None
        return Column(
            controls=[
                Container(
                    content=ProgressRing(visible=True),  # عرض حلقة التحميل
                    alignment=alignment.center,
                    height=float("inf"),  # جعل الحاوية تأخذ المساحة الكاملة
                    expand=True,  # توسيع الحاوية لملء المساحة المتاحة
                ),
            ],
            expand=True,  # توسيع العمود لملء المساحة المتاحة
        )

    # دالة لعرض واجهة الخطأ
    def ErrorUi(self):
        self.scroll = None
        self.controls.clear()
        self.controls.append(
            Column(
                controls=[
                    Container(
                        content=Text(
                            "حدث خطأ الرجاء اعادة المحاولة"
                        ),  # عرض رسالة الخطأ
                        alignment=alignment.center,
                        height=float("inf"),  # جعل الحاوية تأخذ المساحة الكاملة
                        expand=True,  # توسيع الحاوية لملء المساحة المتاحة
                    ),
                ],
                expand=True,  # توسيع العمود لملء المساحة المتاحة
            )
        )
        self.update()

    # دالة لتحميل تفاصيل التنبيه
    def loadNote(self):
        result = self.page.run_task(self.page.client_storage.get_async, "note").result()
        if result:
            self.buildUi(result)  # بناء واجهة تفاصيل التنبيه
        else:
            self.ErrorUi()  # عرض واجهة الخطأ

# تعريف فئة Notifications التي تمثل شاشة الإشعارات
class Notifications(View):
    def __init__(self, route, page):
        super().__init__(route=route)  # استدعاء دالة البناء للفئة الأم (View)
        self.scroll = ScrollMode.AUTO  # تعيين وضع التمرير إلى تلقائي
        self.bgcolor = "#ffffff"  # لون الخلفية
        self.notifications = []  # قائمة الإشعارات

        # تعريف AppBar (شريط التطبيق العلوي)
        self.appbar = AppBar(
            leading=IconButton(
                icon=icons.ARROW_BACK,
                icon_color="#ffffff",
                on_click=lambda x: self.page.go("/home"),  # حدث النقر للرجوع إلى الصفحة الرئيسية
            ),
            title=Text(
                "حماية الاطفال",
                size=20,
                weight=FontWeight.BOLD,
                color="#ffffff",
                font_family="ElMessiri",
            ),
            toolbar_height=100,
        )

    # دالة لبناء واجهة الإشعارات
    def buildUi(self):
        self.controls.clear()
        self.controls.append(
            ResponsiveRow(
                controls=[
                    Container(height=20),
                    Text(
                        "الاشعارات والتنبيهات",
                        style=TextStyle(
                            size=12,
                            weight=FontWeight.BOLD,
                            font_family="ElMessiri",
                        ),
                        color="#666666",
                        expand=True,
                        text_align=TextAlign.CENTER,
                    ),
                    Container(height=30),
                    Column(
                        controls=(
                            self.notifications
                            if self.notifications
                            else [
                                Container(
                                    content=Text(
                                        "لا يوجد اشعارات بعد",
                                        style=TextStyle(
                                            size=12,
                                            weight=FontWeight.BOLD,
                                            font_family="ElMessiri",
                                        ),
                                        color="#666666",
                                        text_align=TextAlign.START,
                                    ),
                                    padding=20,
                                )
                            ]
                        ),
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        alignment=MainAxisAlignment.CENTER,
                    ),
                ],
                expand=True,
            )
        )
        self.update()

    # دالة لعرض واجهة التحميل
    def loaderUi(self):
        self.scroll = None
        return Column(
            controls=[
                Container(
                    content=ProgressRing(visible=True),  # عرض حلقة التحميل
                    alignment=alignment.center,
                    height=float("inf"),  # جعل الحاوية تأخذ المساحة الكاملة
                    expand=True,  # توسيع الحاوية لملء المساحة المتاحة
                ),
            ],
            expand=True,  # توسيع العمود لملء المساحة المتاحة
        )

    # دالة لإرسال طلبات GET إلى الخادم
    async def sendGetRequest(self, url, body={}):
        access = await self.page.client_storage.get_async("access")
        headers = {
            "Content-Length": "165",
            "Content-Type": "multipart/form-data;",
            "Authorization": f"Bearer {access}",
            "User-Agent": "PostmanRuntime/7.39.1",
            "Accept": "*/*",
            "Cache-Control": "no-cache",
            "Host": "127.0.0.1:8000",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }
        try:
            response = requests.get(
                url=f"{Notifications.baseUrl}/{url}/", data=body, headers=headers
            )
            json = response.json()
            if response.status_code == 200:
                return [True, json]
            else:
                return [False, json]
        except requests.exceptions.Timeout:
            return [False, "اتصال الانترنت بطئ"]
        except requests.exceptions.ConnectionError:
            return [False, "حدث خطأ في الاتصال بالخادم. تحقق من اتصالك بالإنترنت."]

    # دالة لإرسال طلبات DELETE إلى الخادم
    async def sendDeleteRequest(self, url, body={}):
        access = await self.page.client_storage.get_async("access")
        headers = {
            "Content-Length": "165",  # يمكن حذف هذا إذا كنت تستخدم مكتبة requests
            "Authorization": f"Bearer {access}",
            "User-Agent": "PostmanRuntime/7.39.1",
            "Accept": "*/*",
            "Cache-Control": "no-cache",
            "Host": "127.0.0.1:8000",  # يمكن حذف هذا إذا كنت تستخدم مكتبة requests
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }
        try:
            response = requests.delete(
                url=f"{Notifications.baseUrl}/{url}/", data=body, headers=headers
            )
            json = response.json()
            if response.status_code == 200:
                return [True, json]
            else:
                return [False, json]
        except requests.exceptions.Timeout:
            return [False, "اتصال الانترنت بطئ"]
        except requests.exceptions.ConnectionError:
            return [False, "حدث خطأ في الاتصال بالخادم. تحقق من اتصالك بالإنترنت."]

    # دالة تُستدعى عند تحميل الواجهة
    def did_mount(self):
        loader = self.loaderUi()  # عرض واجهة التحميل
        self.controls.clear()
        self.controls.append(loader)
        self.update()
        self.loadNotifications()  # تحميل الإشعارات

    # دالة لعرض واجهة الخطأ
    def ErrorUi(self):
        self.scroll = None
        self.controls.clear()
        self.controls.append(
            Column(
                controls=[
                    Container(
                        content=Text(
                            "حدث خطأ الرجاء اعادة المحاولة",
                            style=TextStyle(
                                size=15,
                                weight=FontWeight.BOLD,
                                font_family="ElMessiri",
                            ),
                        ),  # عرض رسالة الخطأ
                        alignment=alignment.center,
                        expand=True,  # توسيع الحاوية لملء المساحة المتاحة
                    ),
                    Container(
                        content=TextButton(
                            icon=icons.REPLAY_OUTLINED,
                            text="اعادة المحاولة",
                            style=ButtonStyle(
                                text_style=TextStyle(
                                    size=15,
                                    weight=FontWeight.BOLD,
                                    font_family="ElMessiri",
                                ),
                            ),
                            on_click=lambda e: self.did_mount()  # حدث النقر لإعادة المحاولة
                        ),  # زر إعادة المحاولة
                        alignment=alignment.center,
                    ),
                ],
                expand=True,  # توسيع العمود لملء المساحة المتاحة
            )
        )
        self.update()

    # دالة لتحميل الإشعارات
    def loadNotifications(self):
        state, result = self.page.run_task(self.sendGetRequest, "notification").result()
        if state:
            self.notifications = [
                ResponsiveRow(
                    controls=[
                        Container(
                            content=ListTile(
                                leading=Icon(icons.ERROR, color=colors.ERROR),
                                title=Text(
                                    f"تنبيه بخصوص ابنك {note['child_first_name']}",
                                    style=TextStyle(
                                        size=15,
                                        weight=FontWeight.BOLD,
                                        font_family="ElMessiri",
                                    ),
                                ),
                                subtitle=Text(
                                    "ابنك يشاهد محتوى مقيد بالفئة العمرية",
                                    style=TextStyle(
                                        size=8,
                                        weight=FontWeight.BOLD,
                                        font_family="ElMessiri",
                                    ),
                                ),
                                trailing=PopupMenuButton(
                                    icon=icons.MORE_VERT,
                                    items=[
                                        PopupMenuItem(
                                            text="حذف",
                                            icon=icons.DELETE,
                                            data=note["id"],
                                            on_click=lambda e: self.deleteNote(e),  # حدث النقر لحذف الإشعار
                                        ),
                                    ],
                                    menu_position=PopupMenuPosition.UNDER,
                                    icon_color="#110b22",
                                    tooltip="خيارات",
                                ),
                            ),
                            bgcolor="#ffffff",
                            border=border.all(0.5, "#110b22"),
                            border_radius=border_radius.all(5),
                            on_click=lambda e: self.goToSpecificNote(e),  # حدث النقر للانتقال إلى تفاصيل الإشعار
                            data=note
                        ),
                    ],
                )
                for note in result
            ]
            self.buildUi()  # بناء واجهة الإشعارات
        else:
            self.ErrorUi()  # عرض واجهة الخطأ

    # دالة للانتقال إلى تفاصيل إشعار محدد
    def goToSpecificNote(self, e):
        self.page.client_storage.set("note", e.control.data)
        self.page.go("/MoreInfoAboutNotifications")

    # دالة لحذف إشعار
    def deleteNote(self, e):
        state, result = self.page.run_task(
            self.sendDeleteRequest, 'notification', {"NoteId": e.control.data}
        ).result()
        if state:
            self.did_mount()  # إعادة تحميل الواجهة
        else:
            self.ErrorUi()  # عرض واجهة الخطأ