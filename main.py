# استيراد المكتبات والوحدات الضرورية
from flet import *
from views.login_screen.login_screen import Login
from views.signup_screen.signup_screen import SignUp
from views.welcome_screen.welcome_screen import Welcome
from views.home_screen.home_screen import Home
from views.profile_screen.profile_screen import (
    Profile,
    PersonalInformation,
    SecurityPasswords,
)
from views.notifications_screen.notifications_screen import (
    Notifications,
    MoreInfoAboutNotifications,
)
from views.devices_screen.devices_screen import Devices
from views.MostUsedApplications_screen.MostUsedApplications_screen import (
    MostUsedApplications,
)
import requests

# تعريف الدالة الرئيسية للتطبيق
def main(page: Page):

    # قاموس يحتوي على أيقونات التطبيقات الشائعة
    app_icons = {
        "com.android.chrome": Icons.LANGUAGE,  # Chrome
        "com.whatsapp": Icons.CHAT,  # WhatsApp
        "com.facebook.katana": Icons.FACEBOOK,  # Facebook (إذا وجدته)
        "com.instagram.android": Icons.CAMERA,  # Instagram
        "com.google.android.youtube": Icons.VIDEO_LIBRARY,  # YouTube
        "com.twitter.android": Icons.PUBLIC,  # Twitter
        "org.telegram.messenger": Icons.TELEGRAM,  # Telegram
    }
    
    # تعريف الخطوط المستخدمة في التطبيق
    page.fonts = {
        "LateefBoldFont": "/fonts/Lateef,Rakkas/Lateef/Lateef-Bold.ttf",
        "LateefNormalFont": "/fonts/Lateef,Rakkas/Lateef/Lateef-Medium.ttf",
        "Rakkas": "/fonts/Lateef,Rakkas/Rakkas/Rakkas-Regular.ttf",
        "ElMessiri": "/fonts/El_Messiri,Lateef,Rakkas/El_Messiri/ElMessiri-VariableFont_wght.ttf",
    }

    # تعيين أيقونات التطبيقات ووضع الثيم والنص من اليمين إلى اليسار
    page.apps = app_icons
    page.theme_mode = ThemeMode.LIGHT
    page.rtl = True
    baseUrl = "http://192.168.244.135:2010"

    # مسح التخزين المحلي للعميل
    # page.client_storage.clear()

    # تعريف الثيم الخاص بالتطبيق
    page.theme = Theme(
        font_family="LateefNormalFont",
        color_scheme_seed="#666666",
        text_theme=TextStyle(color="#110b22", font_family="LateefBoldFont"),
        appbar_theme=AppBarTheme(bgcolor="#110b22", color="#ffffff"),
        scrollbar_theme=ScrollbarTheme(
            thickness=0,
            radius=0,
            main_axis_margin=0,
            cross_axis_margin=0,
        ),
    )

    # دالة لعرض رسائل للمستخدم
    def showMessage(text):
        snack_bar = SnackBar(
            content=Text(
                f"{text}",
                style=TextStyle(size=15, font_family="ElMessiri"),
            ),
            show_close_icon=True,
        )
        page.open(snack_bar)

    # دالة لتغيير المسارات (Routes) بين الشاشات
    def route_change(e):
        routes = {
            "/": Welcome,
            "/home": Home,
            "/login": Login,
            "/signup": SignUp,
            "/Profile": Profile,
            "/PersonalInformation": PersonalInformation,
            "/SecurityPasswords": SecurityPasswords,
            "/notifications": Notifications,
            "/MoreInfoAboutNotifications": MoreInfoAboutNotifications,
            "/devices": Devices,
            "/MostUsedApplications": MostUsedApplications,
        }

        # مسح الشاشات الحالية
        page.views.clear()

        # الحصول على الفئة المناسبة للمسار الحالي
        page_class = routes.get(page.route, None)
        
        # تعيين الرابط الأساسي للفئة
        page_class.baseUrl = baseUrl

        # إضافة الشاشة المناسبة إلى القائمة
        if page_class:
            page.views.append(
                page_class(route=page.route, page=page)
            )  # إضافة الشاشة المناسبة
        else:
            page.views.append(Text("Page not found"))  # إذا لم يكن المسار موجودًا

        # تحديث الصفحة
        page.update()

    # دالة لتحديث token الوصول
    def refreshAccessToken():
        if page.client_storage.contains_key("refresh"):

            # دالة غير متزامنة لتحديث token الوصول
            async def refresh(refresh_token):
                body = {"refresh": refresh_token}
                try:
                    response = requests.post(url=f"{baseUrl}/refresh/", data=body)

                    json = response.json()
                    
                    if response.status_code == 200:
                        return [True, json]
                    else:
                        return [False, "الرجاء التحقق من اتصال الانترنت"]
                except requests.exceptions.Timeout:
                    return [False, "الرجاء التحقق من اتصال الانترنت"]
                except requests.exceptions.ConnectionError:
                    return [
                        False,
                        "لم نتمكن من الوصول الى الخادم الرجاء اعادة المحاولة",
                    ]
                

            # الحصول على token التحديث من التخزين المحلي
            refresh_token = page.client_storage.get("refresh")
            result = page.run_task(refresh, refresh_token)
           
            # التحقق من نتيجة التحديث
            if result.result()[0]:
                page.client_storage.set("access", result.result()[1]["access"])
                page.client_storage.set("refresh", result.result()[1]["refresh"])
                return [result.result()[0], result.result()[1]]
            else:
                return [result.result()[0], result.result()[1]]
        else:
            return [False, "سجل الدخول او انشئ حساب"]

    # تعيين دالة تغيير المسار كمعالج حدث
    page.on_route_change = route_change

    # محاولة تحديث token الوصول
    result = refreshAccessToken()
    if result[0]:
        page.go("/home")
    else:
        page.go("/")
        showMessage(result[1])

# تشغيل التطبيق
app(main, assets_dir="assets")