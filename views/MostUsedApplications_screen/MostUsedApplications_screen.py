# استيراد المكتبات الضرورية
from flet import (
    View,  # الفئة الأساسية لإنشاء واجهات المستخدم
    ScrollMode,  # لتحديد وضع التمرير (Auto, Always, Hidden, etc.)
    Container,  # حاوية لتجميع العناصر وتطبيق الأنماط
    Column,  # لتنظيم العناصر في أعمدة
    ResponsiveRow,  # لتنظيم العناصر في صفوف متجاوبة
    border_radius,  # لتحديد زوايا مدورة للحاويات أو العناصر
    Text,  # لعرض النصوص
    FontWeight,  # لتحديد وزن الخط (عريض، عادي، إلخ)
    ButtonStyle,  # لتخصيص نمط الأزرار
    TextStyle,  # لتخصيص نمط النصوص
    CrossAxisAlignment,  # لمحاذاة العناصر أفقيًا
    MainAxisAlignment,  # لمحاذاة العناصر عموديًا
    Icon,  # لعرض الأيقونات
    icons,  # مكتبة الأيقونات المدمجة
    IconButton,  # زر يحتوي على أيقونة
    AppBar,  # شريط التطبيق العلوي
    ListTile,  # عنصر قائمة
    ProgressBar,  # شريط التقدم
    ProgressRing,  # حلقة التحميل
    alignment,  # لمحاذاة العناصر
    TextButton,  # زر نصي
    Icons,
    TextAlign,
    border,
)
import requests

# تعريف فئة MostUsedApplications التي تمثل شاشة التطبيقات الأكثر استخدامًا
class MostUsedApplications(View):
    def __init__(self, route, page):
        super().__init__(route=route)  # استدعاء دالة البناء للفئة الأم (View)
        self.scroll = ScrollMode.AUTO  # تعيين وضع التمرير إلى تلقائي
        self.apps = []  # قائمة التطبيقات
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
            "com.android.vending": ("متجر جوجل بلاي", Icons.SHOPPING_CART),  # Google Play Store
            "com.microsoft.teams": ("مايكروسوفت تيمز", Icons.WORK),  # Microsoft Teams
            "com.skype.raider": ("سكايب", Icons.CALL),  # Skype
            "com.netflix.mediaclient": ("نتفليكس", Icons.MOVIE),  # Netflix
            "com.spotify.music": ("سبوتيفاي", Icons.MUSIC_NOTE),  # Spotify
        }

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

    # دالة لبناء واجهة التطبيقات الأكثر استخدامًا
    def buildUi(self):
        self.scroll = ScrollMode.AUTO
        self.controls.clear()
        self.controls.append(
            ResponsiveRow(
                controls=[
                    Container(height=10),
                    Column(
                        controls=[
                            Container(height=30),
                            ResponsiveRow(
                                controls=[
                                    Text(
                                        "قائمة التطبيقات",
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
                                    self.apps
                                    if len(self.apps) > 0
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
                                        )
                                    ]
                                ),
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

    # دالة تُستدعى عند تحميل الواجهة
    def did_mount(self):
        loader = self.loaderUi()  # عرض واجهة التحميل
        self.controls.clear()
        self.controls.append(loader)
        self.update()
        self.loadMostUseApps()  # تحميل التطبيقات الأكثر استخدامًا

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
                url=f"{MostUsedApplications.baseUrl}/{url}/",
                params=body,
                headers=headers
            )

            print(response.status_code)

            try:
                json_data = response.json()
            except:
                json_data = {}

            if response.status_code == 200:
                return [True, json_data]
            else:
                return [False, json_data]

        except requests.exceptions.Timeout:
            return [False, "اتصال الانترنت بطئ"]
        except requests.exceptions.ConnectionError:
            return [False, "حدث خطأ في الاتصال بالخادم. تحقق من اتصالك بالإنترنت."]
        except Exception as e:
            print(e)
            return [False, "اتصال الانترنت بطئ"]

    # دالة لتحميل التطبيقات الأكثر استخدامًا
    def loadMostUseApps(self):
        childId = self.page.run_task(
            self.page.client_storage.get_async, "ChildUser"
        ).result()
        print(childId)
        state, result = self.page.run_task(
            self.sendGetRequest, "mostUseApps", {"ChildUser": childId}
        ).result()
        if state:
            self.apps = [
                Container(
                    content=ResponsiveRow(
                        controls=[
                            ListTile(
                                title=Text(
                                    self.app_icons.get(
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
                                    self.app_icons.get(
                                        f"{app['appName']}",
                                        (f"{app['appName']}", Icons.APPS),
                                    )[1],
                                ),
                                subtitle=ProgressBar(
                                    value=self.get_usage_percentage(
                                        f"{app['appName']}", f"{app['hour']}"
                                    )
                                ),
                            )
                        ],
                    ),
                    bgcolor="#ffffff",
                    border=border.all(0.5, "#110b22"),
                    border_radius=border_radius.all(5),
                    alignment=alignment.center,
                )
                for app in result
            ]
            self.buildUi()  # بناء واجهة التطبيقات الأكثر استخدامًا
        else:
            self.ErrorUi()  # عرض واجهة الخطأ

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