# استيراد المكتبات الضرورية
from flet import (
    View,  # الفئة الأساسية لإنشاء واجهات المستخدم
    ScrollMode,  # لتحديد وضع التمرير (Auto, Always, Hidden, etc.)
    Ref,  # لإنشاء مراجع للعناصر
    TextField,  # لحقول إدخال النص
    Container,  # حاوية لتجميع العناصر وتطبيق الأنماط
    Column,  # لتنظيم العناصر في أعمدة
    ResponsiveRow,  # لتنظيم العناصر في صفوف متجاوبة
    Text,  # لعرض النصوص
    FontWeight,  # لتحديد وزن الخط (عريض، عادي، إلخ)
    IconButton,  # زر يحتوي على أيقونة
    AppBar,  # شريط التطبيق العلوي
    Icon,  # لعرض الأيقونات
    icons,  # مكتبة الأيقونات المدمجة
    ListTile,  # عنصر قائمة
    PopupMenuButton,  # زر قائمة منبثقة
    PopupMenuItem,  # عنصر في القائمة المنبثقة
    PopupMenuPosition,  # لتحديد موقع القائمة المنبثقة
    SnackBar,  # لعرض الرسائل العابرة
    ProgressRing,  # حلقة التحميل
    alignment,  # لمحاذاة العناصر
    border,  # لتحديد الحدود
    border_radius,  # لتحديد زوايا مدورة للحاويات أو العناصر
    TextStyle,  # لتخصيص نمط النصوص
    TextAlign,  # لمحاذاة النصوص
    CrossAxisAlignment,  # لمحاذاة العناصر أفقيًا
    MainAxisAlignment,  # لمحاذاة العناصر عموديًا
    TextButton,  # زر نصي
    ButtonStyle,  # لتخصيص نمط الأزرار
)
import requests  # لإرسال طلبات HTTP

# تعريف فئة Devices التي تمثل شاشة إدارة الأجهزة
class Devices(View):
    def __init__(self, route, page):
        super().__init__(route=route)  # استدعاء دالة البناء للفئة الأم (View)
        self.scroll = ScrollMode.HIDDEN  # تعيين وضع التمرير إلى تلقائي
        self.page = page  # حفظ صفحة التطبيق
        self.devices = []  # قائمة الأجهزة
        self.keyTextbox = Ref[TextField]()  # مرجع لحقل إدخال المفتاح

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
                            on_click=lambda e: self.did_mount(),  # حدث النقر لإعادة المحاولة
                        ),  # زر إعادة المحاولة
                        alignment=alignment.center,
                    ),
                ],
                expand=True,  # توسيع العمود لملء المساحة المتاحة
            )
        )
        self.update()

    # دالة تُستدعى عند تحميل الواجهة
    def did_mount(self):
        self.loaderUi()  # عرض واجهة التحميل
        self.getDevices()  # تحميل الأجهزة

    # دالة لعرض واجهة التحميل
    def loaderUi(self):
        self.scroll = None
        self.controls.clear()
        self.controls.append(
            Column(
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
        )
        self.update()

    # دالة لبناء واجهة الأجهزة
    def buildUi(self):
        self.controls.clear()
        self.controls.append(
            ResponsiveRow(
                controls=[
                    Container(height=10),
                    Column(
                        controls=[
                            ResponsiveRow(
                                controls=[
                                    Text(
                                        "اضافة المزيد الاجهزة",
                                        style=TextStyle(
                                            size=12,
                                            weight=FontWeight.BOLD,
                                            font_family="ElMessiri",
                                        ),
                                        color="#666666",
                                        text_align=TextAlign.START,
                                    ),
                                ],
                            ),
                            ResponsiveRow(
                                controls=[
                                    Container(
                                        content=ListTile(
                                            title=TextField(
                                                label="ادخل المفتاح الذي نسخته من هاتف الابن",
                                                text_style=TextStyle(
                                                    size=15, font_family="ElMessiri"
                                                ),
                                                label_style=TextStyle(
                                                    size=12, font_family="ElMessiri"
                                                ),
                                                ref=self.keyTextbox,
                                                border=None,
                                                border_width=0,
                                            ),
                                            trailing=IconButton(
                                                icon=icons.SEND,
                                                on_click=self.addNewChild,  # حدث النقر لإضافة جهاز جديد
                                                icon_size=15,
                                            ),
                                        ),
                                        bgcolor="#ffffff",
                                        border=border.all(0.5, "#110b22"),
                                        border_radius=border_radius.all(5),
                                    ),
                                ],
                            ),
                            Container(height=30),
                            ResponsiveRow(
                                controls=[
                                    Text(
                                        "الاجهزة التي اضفتها سابقا",
                                        style=TextStyle(
                                            size=12,
                                            weight=FontWeight.BOLD,
                                            font_family="ElMessiri",
                                        ),
                                        color="#666666",
                                        text_align=TextAlign.START,
                                    ),
                                ],
                            ),
                            Column(
                                controls=(
                                    self.devices
                                    if len(self.devices) > 0
                                    else [
                                        Container(
                                            content=Text(
                                                "لا يوجد اجهزة  بعد",
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
                                )
                            ),
                        ],
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        alignment=MainAxisAlignment.CENTER,
                    ),
                ],
                expand=True,
            )
        )
        self.update()

    # دالة لعرض رسائل للمستخدم
    def showMessage(self, message):
        snack_bar = SnackBar(
            content=Text(
                f"{message}",
                style=TextStyle(size=15, font_family="ElMessiri"),
            ),
            show_close_icon=True,
        )
        self.page.open(snack_bar)

    # دالة لحذف جهاز
    def deleteUser(self, e):
        self.loaderUi()  # عرض واجهة التحميل
        if e.control.data:
            _, result = self.page.run_task(
                self.sendDeleteRequest, "Children", {"key": e.control.data}
            ).result()
            print(result)
            self.did_mount()  # إعادة تحميل الواجهة
            self.showMessage(f"{result['key']}")  # عرض رسالة النتيجة

    # دالة للتحقق من صحة البيانات المدخلة
    def checkTextBoxData(self):
        if not self.keyTextbox.current.value:
            self.keyTextbox.current.error = Text(
                f"الرجاء ادخال  المفتاح اولا",
                style=TextStyle(size=10, font_family="ElMessiri"),
            )
            self.update()
            return self.keyTextbox.current.value, False
        else:
            return self.keyTextbox.current.value, True

    # دالة لإضافة جهاز جديد
    def addNewChild(self, e):
        values, state = self.checkTextBoxData()  # التحقق من صحة البيانات المدخلة
        if state:
            self.loaderUi()  # عرض واجهة التحميل
            state, result = self.page.run_task(
                self.sendPostRequest, "Children", {"key": values}
            ).result()
            if state:
                self.showMessage(result["key"])  # عرض رسالة نجاح
                self.did_mount()  # إعادة تحميل الواجهة
            else:
                self.did_mount()
                self.showMessage(result["key"])  # عرض رسالة خطأ

    # دالة لتحميل الأجهزة
    def getDevices(self):
        state, result = self.page.run_task(self.sendGetRequest, "Children").result()
        if state:
            devices = []
            for childData in result.values():
                devices.append(
                    ResponsiveRow(
                        controls=[
                            Container(
                                content=ListTile(
                                    leading=Icon(
                                        icons.PHONE_ANDROID_OUTLINED,
                                        color="#110b22",
                                    ),
                                    title=Text(
                                        f"جهاز  {childData[0]['child_first_name']}",
                                        style=TextStyle(
                                            size=15,
                                            weight=FontWeight.BOLD,
                                            font_family="ElMessiri",
                                        ),
                                    ),
                                    subtitle=Text(
                                        f"{childData[0]['key']}",
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
                                                data=childData[0]["key"],
                                                icon=icons.DELETE,
                                                on_click=self.deleteUser,  # حدث النقر لحذف الجهاز
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
                            ),
                        ],
                    )
                )
            self.devices = devices
            self.buildUi()  # بناء واجهة الأجهزة
        else:
            self.buildUi()
            self.showMessage("حدث خطا غير متوقع")  # عرض رسالة خطأ

    # دالة لإرسال طلبات DELETE إلى الخادم
    async def sendDeleteRequest(self, url, body={}):
        access = await self.page.client_storage.get_async("access")
        headers = {
            "Authorization": f"Bearer {access}",
            "Accept": "*/*",
            "Cache-Control": "no-cache",
        }
        try:
            response = requests.delete(
                url=f"{Devices.baseUrl}/{url}/", data=body, headers=headers
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

    # دالة لإرسال طلبات POST إلى الخادم
    async def sendPostRequest(self, url, body={}):
        access = await self.page.client_storage.get_async("access")
        headers = {
            "Authorization": f"Bearer {access}",
            "Accept": "*/*",
            "Cache-Control": "no-cache",
        }
        try:
            response = requests.post(
                url=f"{Devices.baseUrl}/{url}/", data=body, headers=headers
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

    # دالة لإرسال طلبات GET إلى الخادم
    async def sendGetRequest(self, url, body={}):
        access = await self.page.client_storage.get_async("access")
        headers = {
            "Authorization": f"Bearer {access}",
            "Accept": "*/*",
            "Cache-Control": "no-cache",
        }
        try:
            response = requests.get(
                url=f"{Devices.baseUrl}/{url}/", data=body, headers=headers
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