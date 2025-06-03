# استيراد المكتبات الضرورية
from flet import (
    View,  # الفئة الأساسية لإنشاء واجهات المستخدم
    ScrollMode,  # لتحديد وضع التمرير (Auto, Always, Hidden, etc.)
    Ref,  # لإنشاء مراجع للعناصر
    TextField,  # لحقول إدخال النص
    Container,  # حاوية لتجميع العناصر وتطبيق الأنماط
    Column,  # لتنظيم العناصر في أعمدة
    ResponsiveRow,  # لتنظيم العناصر في صفوف متجاوبة
    Image,  # لعرض الصور
    border_radius,  # لتحديد زوايا مدورة للحاويات أو العناصر
    Text,  # لعرض النصوص
    FontWeight,  # لتحديد وزن الخط (عريض، عادي، إلخ)
    ButtonStyle,  # لتخصيص نمط الأزرار
    TextStyle,  # لتخصيص نمط النصوص
    CrossAxisAlignment,  # لمحاذاة العناصر أفقيًا
    MainAxisAlignment,  # لمحاذاة العناصر عموديًا
    NavigationDrawer,  # القائمة الجانبية
    NavigationDrawerDestination,  # عنصر في القائمة الجانبية
    Divider,  # خط فاصل
    Icon,  # لعرض الأيقونات
    icons,  # مكتبة الأيقونات المدمجة
    IconButton,  # زر يحتوي على أيقونة
    AppBar,  # شريط التطبيق العلوي
    Dropdown,  # قائمة منسدلة
    dropdown,  # لتحديد خيارات القائمة المنسدلة
    ListTile,  # عنصر قائمة
    ProgressBar,  # شريط التقدم
    CircleAvatar,  # دائرة لعرض المحتوى
    SnackBar,  # لعرض الرسائل العابرة
    ProgressRing,  # حلقة التحميل
    alignment,  # لمحاذاة العناصر
    padding,  # لإضافة حشوة داخلية
    TextButton,  # زر نصي
    Icons,
    TextAlign,
    border,
)
import requests  # لإرسال طلبات HTTP
import asyncio  # للتعامل مع المهام غير المتزامنة


# تعريف فئة Home التي تمثل الشاشة الرئيسية للتطبيق
class Home(View):
    def __init__(self, route, page):
        super().__init__(route=route)  # استدعاء دالة البناء للفئة الأم (View)
        self.scroll = ScrollMode.HIDDEN  # تعيين وضع التمرير إلى تلقائي
        self.page = page  # حفظ صفحة التطبيق
        self.innerChild = {}  # بيانات الطفل المحدد
        self.children = []  # قائمة الأطفال
        self.childrenList = []  # قائمة الأطفال لعرضها في Dropdown
        self.keyTextbox = Ref[TextField]()  # مرجع لحقل إدخال المفتاح
        self.notifications = Container(width=0, height=0)  # حاوية للإشعارات
        self.notificationsState = True  # حالة الإشعارات (مفعلة/معطلة)

        # قاموس يحتوي على أيقونات التطبيقات وأسمائها
        self.app_icons = {
            "com.android.chrome": ("متصفح كروم", Icons.LANGUAGE),  # Chrome
            "com.whatsapp": ("واتساب", Icons.CHAT),  # WhatsApp
            "com.facebook.katana": ("فيسبوك", Icons.FACEBOOK),  # Facebook
            "com.instagram.android": ("إنستجرام", Icons.CAMERA),  # Instagram
            "com.google.android.youtube": ("يوتيوب", Icons.VIDEO_LIBRARY),  # YouTube
            "com.twitter.android": ("تويتر", Icons.PUBLIC),  # Twitter (حاليًا X)
            "org.telegram.messenger": ("تيليجرام", Icons.TELEGRAM),  # Telegram
            "com.snapchat.android": ("سناب شات", Icons.SNAPCHAT),  # Snapchat
            "com.tiktok.android": ("تيك توك", Icons.VIDEO_CALL),  # TikTok
            "com.google.android.gm": ("جيميل", Icons.EMAIL),  # Gmail
            "com.android.vending": (
                "متجر جوجل بلاي",
                Icons.SHOPPING_CART,
            ),  # Google Play Store
            "com.microsoft.teams": ("مايكروسوفت تيمز", Icons.WORK),  # Microsoft Teams
            "com.skype.raider": ("سكايب", Icons.CALL),  # Skype
            "com.netflix.mediaclient": ("نتفليكس", Icons.MOVIE),  # Netflix
            "com.spotify.music": ("سبوتيفاي", Icons.MUSIC_NOTE),  # Spotify
        }

        # تعريف NavigationDrawer (القائمة الجانبية)
        self.drawer = NavigationDrawer(
            on_change=self.handle_change,  # حدث تغيير العنصر المحدد
            controls=[
                Container(height=12),
                NavigationDrawerDestination(
                    label="الرئيسية",
                    icon_content=Icon(Icons.HOME_OUTLINED),
                    selected_icon_content=Icon(Icons.HOME),
                ),
                Divider(thickness=2),
                NavigationDrawerDestination(
                    label="الاجهزة المرتبطة",
                    icon_content=Icon(Icons.PHONE_ANDROID_OUTLINED),
                    selected_icon_content=Icon(Icons.PHONE_ANDROID),
                ),
                NavigationDrawerDestination(
                    label="تسجيل الخروج",
                    icon_content=Icon(Icons.LOGOUT_OUTLINED),
                    selected_icon_content=Icon(Icons.LOGOUT),
                ),
            ],
        )

        # تعريف AppBar (شريط التطبيق العلوي)
        self.appbar = AppBar(
            actions=[
                IconButton(
                    icon=Icons.PERSON,
                    icon_color="#ffffff",
                    on_click=lambda x: self.page.go(
                        "/Profile"
                    ),  # الانتقال إلى صفحة الملف الشخصي
                ),
                IconButton(
                    icon=Icons.NOTIFICATIONS,
                    icon_color="#ffffff",
                    on_click=lambda x: self.page.go(
                        "/notifications"
                    ),  # الانتقال إلى صفحة الإشعارات
                ),
            ],
            leading=IconButton(
                icon=Icons.MENU,
                icon_color="#ffffff",
                on_click=lambda e: self.page.open(self.drawer),  # فتح القائمة الجانبية
            ),
            toolbar_height=100,
            title=Text(
                "حماية الاطفال",
                size=20,
                weight=FontWeight.BOLD,
                color="#ffffff",
                font_family="ElMessiri",
            ),
        )

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

    # دالة للتعامل مع تغيير العنصر المحدد في القائمة الجانبية
    def handle_change(self, e):
        routs = {
            "0": "/home",  # الرئيسية
            "1": "/devices",  # الأجهزة المرتبطة
            "2": "/",  # تسجيل الخروج
        }

        if routs[e.data] == "/":
            self.page.client_storage.clear()  # مسح التخزين المحلي

        self.page.go(routs[e.data])  # الانتقال إلى المسار المحدد
        self.page.close(self.drawer)  # إغلاق القائمة الجانبية

    # دالة تُستدعى عند تحميل الواجهة
    def did_mount(self):
        loader = self.loaderUi()  # عرض واجهة التحميل
        self.controls.clear()
        self.controls.append(loader)
        self.update()
        self.loadChildren()  # تحميل بيانات الأطفال
        # self.page.run_task(self.updatenotification)  # تحديث الإشعارات بشكل دوري

    # دالة لبناء واجهة عندما يكون هناك أطفال مضافين
    def buildHasChildrenUi(self):
        self.scroll = ScrollMode.HIDDEN
        self.controls.clear()
        self.controls.append(
            ResponsiveRow(
                controls=[
                    Container(
                        content=Dropdown(
                            label="اختر احد الابناء لعرض بياناته",
                            options=self.childrenList,  # قائمة الأطفال
                            label_style=TextStyle(
                                size=13,
                                weight=FontWeight.NORMAL,
                                font_family="ElMessiri",
                            ),
                            width=float("inf"),
                            on_change=self.changeSelectedChild,  # حدث تغيير الطفل المحدد
                        ),
                        width=float("inf")
                    ),
                    Container(height=10),
                    Column(
                        controls=[
                            Container(
                                content=Image(
                                    src=(
                                        "/images/BChild.png"
                                        if self.innerChild["childData"]["child_gender"]
                                        == "1"
                                        else "/images/GChild.png"
                                    ),
                                    width=150,
                                ),
                                border_radius=border_radius.all(150),
                            ),
                            Container(
                                content=Text(
                                    f"({self.innerChild['childData']['child_first_name']})",
                                    size=20,
                                    weight=FontWeight.BOLD,
                                    color="#666666",
                                    font_family="ElMessiri",
                                ),
                            ),
                            Container(
                                content=Text(
                                    "اخر موعد اتصال",
                                    size=8,
                                    weight=FontWeight.NORMAL,
                                    color="#666666",
                                    font_family="ElMessiri",
                                ),
                            ),
                            Container(height=20),
                            ResponsiveRow(
                                controls=[
                                    Text(
                                        "قائمة الاختصارات",
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
                                        content=Column(
                                            controls=[
                                                Container(),
                                                Icon(
                                                    Icons.WIDGETS,
                                                    size=50,
                                                    color="#110b22",
                                                ),
                                                Text(
                                                    "استخدام التطبيقات",
                                                    style=TextStyle(
                                                        size=11,
                                                        weight=FontWeight.BOLD,
                                                        font_family="ElMessiri",
                                                        color="#666666",
                                                    ),
                                                ),
                                            ],
                                            horizontal_alignment=CrossAxisAlignment.CENTER,
                                            alignment=MainAxisAlignment.SPACE_AROUND,
                                        ),
                                        alignment=alignment.center,
                                        height=140,
                                        border_radius=10,
                                        col={"xs": 6, "sm": 10, "md": 5, "xl": 5},
                                        border=border.all(width=1, color="#110b22"),
                                        on_click=lambda x: self.page.go(
                                            "/MostUsedApplications"
                                        ),
                                    ),
                                    Container(
                                        content=Column(
                                            controls=[
                                                self.notifications,
                                                Icon(
                                                    Icons.SECURITY,
                                                    size=50,
                                                    color="#110b22",
                                                ),
                                                Text(
                                                    "التنبيهات",
                                                    style=TextStyle(
                                                        size=11,
                                                        weight=FontWeight.BOLD,
                                                        font_family="ElMessiri",
                                                        color="#666666",
                                                    ),
                                                ),
                                            ],
                                            horizontal_alignment=CrossAxisAlignment.CENTER,
                                            alignment=MainAxisAlignment.SPACE_AROUND,
                                        ),
                                        alignment=alignment.center,
                                        height=140,
                                        border_radius=10,
                                        col={"xs": 6, "sm": 10, "md": 5, "xl": 5},
                                        border=border.all(width=1, color="#110b22"),
                                        on_click=lambda x: self.page.go(
                                            "/notifications"
                                        ),
                                    ),
                                ],
                                alignment=MainAxisAlignment.CENTER,
                                col={"sm": 2, "md": 4, "xl": 2},
                            ),
                            ResponsiveRow(
                                controls=[
                                    Text(
                                        "التطبيقات الاكثر استخدام",
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
                            Container(
                                content=ResponsiveRow(
                                    controls=(
                                        self.innerChild["apps"]
                                        if len(self.innerChild["apps"]) > 0
                                        else [
                                            Container(
                                                content=Text(
                                                    "لا يوجد تطبيقات بعد",
                                                    style=TextStyle(
                                                        size=12,
                                                        weight=FontWeight.BOLD,
                                                        font_family="ElMessiri",
                                                    ),
                                                    color="#666666",
                                                    text_align=TextAlign.START,
                                                ),
                                                padding=20,
                                            ),
                                        ]
                                    ),
                                ),
                                bgcolor="#ffffff",
                                border=border.all(0.5, "#110b22"),
                                border_radius=border_radius.all(5),
                                alignment=alignment.center,
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

    # دالة لإضافة طفل جديد
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

    # دالة للتحقق من صحة البيانات المدخلة
    def checkTextBoxData(self):
        if not self.keyTextbox.current.value:
            self.keyTextbox.current.error = Text(
                "الرجاء ادخال  المفتاح اولا",
                style=TextStyle(size=10, font_family="ElMessiri"),
            )
            self.update()
            return self.keyTextbox.current.value, False
        else:
            return self.keyTextbox.current.value, True

    # دالة لبناء واجهة عندما لا يكون هناك أطفال مضافين
    def buildHasNoChild(self):
        self.controls.clear()
        self.controls.append(
            ResponsiveRow(
                controls=[
                    Container(
                        content=Column(
                            controls=[
                                ListTile(
                                    leading=Icon(Icons.INFO),
                                    title=Text(
                                        "انت لم تضف جهاز بعد الرجاء اضافة جهاز اولا",
                                        size=13,
                                        weight=FontWeight.NORMAL,
                                        color="#666666",
                                        font_family="ElMessiri",
                                    ),
                                ),
                                Container(
                                    content=Text(
                                        "اولا تحتاج الى تحميل تطبيق الابن على هاتف أبنك ثم انشئ فيه حساب بعد ذالك يظهر مفتاح خاص بحساب الطفل ادخل هذا المفتاح في المربع النصي بالاسفل وبعدها تكون قد انتهيت",
                                        size=13,
                                        weight=FontWeight.NORMAL,
                                        color="#666666",
                                        font_family="ElMessiri",
                                    ),
                                    padding=20,
                                ),
                            ]
                        ),
                        bgcolor="#ffffff",
                        border=border.all(color="#110b22", width=1),
                        border_radius=border_radius.all(10),
                    ),
                    Container(height=30),
                    Container(
                        content=Text(
                            "ادخل مفتاح الابن لاضافة جهاز",
                            size=13,
                            weight=FontWeight.NORMAL,
                            color="#666666",
                            font_family="ElMessiri",
                        ),
                    ),
                    Container(
                        content=Column(
                            controls=[
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
                                                    icon=Icons.SEND,
                                                    on_click=self.addNewChild,
                                                    icon_size=15,
                                                ),
                                            ),
                                            bgcolor="#ffffff",
                                            border=border.all(0.5, "#110b22"),
                                            border_radius=border_radius.all(5),
                                        ),
                                    ],
                                ),
                            ],
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            alignment=MainAxisAlignment.CENTER,
                        ),
                        bgcolor="#ffffff",
                        border=border.all(color="#110b22", width=1),
                        border_radius=border_radius.all(10),
                        padding=padding.symmetric(vertical=20),
                    ),
                ],
                expand=True,
            )
        )
        self.update()

    # دالة لتغيير الطفل المحدد
    def changeSelectedChild(self, event):
        self.innerChild["childData"] = self.children[int(event.data)]["childData"]
        self.page.client_storage.set(
            "ChildUser", self.children[int(event.data)]["childData"]["ChildUser"]
        )
        self.innerChild["apps"] = self.children[int(event.data)]["apps"]
        self.buildHasChildrenUi()

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

    # دالة لتحميل بيانات الأطفال
    def loadChildren(self):
        state, result = self.page.run_task(self.sendGetRequest, "Children").result()
        notifcationsState, notifcationsResult = self.page.run_task(
            self.sendGetRequest, "notifications"
        ).result()
        if state and len(result) > 0:
            for index, childData in enumerate(result.values()):
                self.childrenList.append(
                    dropdown.Option(
                        content=Text(f'{childData[0]["child_first_name"]}'), text=index
                    )
                )
                self.children.append(
                    {
                        "childData": childData[0],
                        "apps": [
                            ListTile(
                                title=Text(
                                    self.app_Icons.get(
                                        f"{app['appName']}",
                                        (f"{app['appName']}", Icons.APPS),
                                    )[0],
                                    style=TextStyle(
                                        size=13,
                                        weight=FontWeight.BOLD,
                                        font_family="ElMessiri",
                                    ),
                                ),
                                leading=Text(
                                    f"{app['hour']}",
                                    style=TextStyle(
                                        size=14,
                                        weight=FontWeight.BOLD,
                                        font_family="ElMessiri",
                                    ),
                                ),
                                trailing=Icon(
                                    self.app_Icons.get(
                                        f"{app['appName']}",
                                        (f"{app['appName']}", Icons.APPS),
                                    )[1]
                                ),
                                subtitle=ProgressBar(
                                    value=self.get_usage_percentage(
                                        f"{app['appName']}", f"{app['hour']}"
                                    )
                                ),
                            )
                            for app in childData[1]
                        ],
                    }
                )

            self.innerChild["childData"] = self.children[0]["childData"]
            self.innerChild["apps"] = self.children[0]["apps"]
            self.page.client_storage.set(
                "ChildUser", self.children[0]["childData"]["ChildUser"]
            )
            if notifcationsState and len(notifcationsResult) > 0:
                self.notifications = Container(
                    content=CircleAvatar(
                        content=Text(
                            f"{len(notifcationsResult)}",
                            style=TextStyle(
                                size=9,
                                weight=FontWeight.BOLD,
                                font_family="ElMessiri",
                                color="#ffffff",
                            ),
                        ),
                        bgcolor="red",
                        width=20,
                    ),
                    height=13,
                    alignment=alignment.top_right,
                    width=float("inf"),
                )
            self.buildHasChildrenUi()
        elif state and len(result) == 0:
            self.buildHasNoChild()
        else:
            self.ErrorUi()

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
                url=f"{Home.baseUrl}/{url}/", data=body, headers=headers
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
                url=f"{Home.baseUrl}/{url}/", data=body, headers=headers
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

    # دالة لحساب نسبة استخدام التطبيق
    def get_usage_percentage(self, app_name: str, usage_time: str) -> float:
        NORMAL_USAGE = {
            "social": 120,  # وسائل التواصل الاجتماعي (Facebook, Instagram, TikTok)
            "messaging": 90,  # تطبيقات المراسلة (WhatsApp, Telegram)
            "browsing": 60,  # التصفح (Chrome, Safari)
            "video": 150,  # مشاهدة الفيديوهات (YouTube, Netflix)
            "gaming": 90,  # الألعاب (PUBG, Candy Crush)
            "system": 45,  # تطبيقات النظام
            "other": 60,  # أي تطبيق غير محدد
        }

        APP_CATEGORIES = {
            "com.facebook.katana": "social",
            "com.instagram.android": "social",
            "com.twitter.android": "social",
            "com.whatsapp": "messaging",
            "com.google.android.youtube": "video",
            "com.android.chrome": "browsing",
            "com.flet.child_app": "other",
            "واجهة النظام": "system",
        }

        # تحويل الوقت إلى دقائق
        h, m, s = map(int, usage_time.split(":"))
        usage_minutes = h * 60 + m + s / 60

        category = APP_CATEGORIES.get(app_name, "other")
        normal_time = NORMAL_USAGE.get(category, 60)
        return min(1.0, usage_minutes / normal_time)

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
                        ),  # Progress ring loader
                        alignment=alignment.center,
                        expand=True,  # Ensure the container expands to fill available space
                    ),
                    Container(
                        content=TextButton(
                            icon=Icons.REPLAY_OUTLINED,
                            text="اعادة المحاولة",
                            style=ButtonStyle(
                                text_style=TextStyle(
                                    size=15,
                                    weight=FontWeight.BOLD,
                                    font_family="ElMessiri",
                                ),
                            ),
                            on_click=lambda e: self.did_mount(),
                        ),  # Progress ring loader
                        alignment=alignment.center,
                    ),
                ],
                expand=True,  # Make the column expand to take up all available space
            )
        )
        self.update()

    # دالة لتحديث الإشعارات بشكل دوري
    async def updatenotification(self):
        while self.notificationsState:
            notifcationsState, notifcationsResult = await self.sendGetRequest(
                "notifications"
            )
            print(notifcationsResult)
            print(len(notifcationsResult))
            if notifcationsState and len(notifcationsResult) > 0:
                self.notifications = Container(
                    content=CircleAvatar(
                        content=Text(
                            f"{len(notifcationsResult)}",
                            style=TextStyle(
                                size=9,
                                weight=FontWeight.BOLD,
                                font_family="ElMessiri",
                                color="#ffffff",
                            ),
                        ),
                        bgcolor="red",
                        width=20,
                    ),
                    height=13,
                    alignment=alignment.top_right,
                    width=float("inf"),
                )
                self.buildHasChildrenUi()
            await asyncio.sleep(50)
            if not self.notificationsState:
                break

    # دالة تُستدعى عند إغلاق الواجهة
    def will_unmount(self):
        self.notificationsState = False












