# استيراد المكتبات الضرورية
from flet import *
import requests

# تعريف فئة Login التي تمثل شاشة تسجيل الدخول
class Login(View):
    def __init__(self, route, page):
        super().__init__(route=route)  # استدعاء دالة البناء للفئة الأم (View)
        self.rtl = True  # تعيين اتجاه النص من اليمين إلى اليسار
        self.scroll = ScrollMode.AUTO  # تعيين وضع التمرير إلى تلقائي

        # تعريف حقل إدخال اسم المستخدم
        self.userNameTextBox = TextField(
            label="اســـم المــستخدم",  # تسمية الحقل باللغة العربية
            border_radius=border_radius.all(22),  # زوايا مدورة للحقل
            border_color="#171335",  # لون الحدود
            text_style=TextStyle(size=15, font_family="ElMessiri"),  # تخصيص نمط النص
            label_style=TextStyle(size=18, font_family="ElMessiri"),  # تخصيص نمط التسمية
        )

        # تعريف حقل إدخال كلمة المرور
        self.passwordTextBox = TextField(
            label="كــلمة المــرور",  # تسمية الحقل باللغة العربية
            password=True,  # إخفاء النص
            can_reveal_password=True,  # إمكانية إظهار النص
            border_radius=border_radius.all(22),  # زوايا مدورة للحقل
            border_color="#171335",  # لون الحدود
            text_style=TextStyle(size=15, font_family="ElMessiri"),  # تخصيص نمط النص
            label_style=TextStyle(size=18, font_family="ElMessiri"),  # تخصيص نمط التسمية
        )

    # دالة تُستدعى عند تحميل الواجهة
    def did_mount(self):
        self.loginUi()

    # دالة لبناء واجهة تسجيل الدخول
    def loginUi(self):
        self.scroll = ScrollMode.AUTO
        self.controls.clear()  # مسح العناصر الحالية
        self.controls.append(
            ResponsiveRow(  # صف متجاوب لتنظيم العناصر
                controls=[
                    Row(  # صف لعرض زر الرجوع
                        controls=[
                            IconButton(
                                icon=icons.ARROW_BACK,  # أيقونة الرجوع
                                on_click=lambda x: self.page.go("/"),  # حدث النقر للرجوع إلى الصفحة الرئيسية
                            )
                        ],
                        expand=False,
                        alignment=MainAxisAlignment.START,  # محاذاة الزر إلى اليسار
                    ),
                    Column(  # عمود لتجميع العناصر
                        controls=[
                            ResponsiveRow(  # صف متجاوب لعرض الصورة
                                controls=[
                                    Image(
                                        src="/images/logo.png",  # مصدر الصورة
                                        fit=ImageFit.COVER,  # ضبط الصورة لتغطية المساحة المحددة
                                        border_radius=border_radius.all(20.0),  # زوايا مدورة للصورة
                                        col={  # تحديد حجم الصورة بناءً على حجم الشاشة
                                            "xs": 10,
                                            "sm": 10,
                                            "md": 7,
                                            "lg": 5,
                                            "xl": 5,
                                        },
                                    ),
                                ],
                                expand=False,
                                alignment=MainAxisAlignment.CENTER,  # محاذاة الصورة في المنتصف
                            ),
                            Text(  # نص عنوان الشاشة
                                "حماية الاطفال",  # العنوان باللغة العربية
                                size=20,
                                weight=FontWeight.BOLD,
                                font_family="ElMessiri",
                            ),
                            Container(height=10),  # حاوية فارغة لخلق مسافة
                            self.userNameTextBox,  # عرض حقل اسم المستخدم
                            Container(height=10),  # حاوية فارغة لخلق مسافة
                            self.passwordTextBox,  # عرض حقل كلمة المرور
                            Container(height=20),  # حاوية فارغة لخلق مسافة
                            ResponsiveRow(  # صف متجاوب لعرض زر تسجيل الدخول
                                controls=[
                                    ElevatedButton(
                                        "تسجيل الدخول",  # تسمية الزر باللغة العربية
                                        style=ButtonStyle(  # تخصيص نمط الزر
                                            shape=RoundedRectangleBorder(radius=22),  # زوايا مدورة للزر
                                            bgcolor="#171335",  # لون خلفية الزر
                                            color="#ffffff",  # لون النص
                                            text_style=TextStyle(
                                                size=15,
                                                weight=FontWeight.BOLD,
                                                font_family="ElMessiri",  # تخصيص نمط النص
                                            ),
                                            padding=5,  # إضافة حشوة داخلية للزر
                                        ),
                                        on_click=lambda e: self.LoginEvent(),  # حدث النقر لتسجيل الدخول
                                    ),
                                ]
                            ),
                        ],
                        horizontal_alignment=CrossAxisAlignment.CENTER,  # محاذاة العناصر أفقياً في المنتصف
                        alignment=MainAxisAlignment.CENTER,  # محاذاة العناصر عمودياً في المنتصف
                    ),
                ],
                expand=True,  # توسيع الصف لملء المساحة المتاحة
            )
        )
        self.update()  # تحديث الواجهة

    # دالة لعرض واجهة التحميل
    def loaderUi(self):
        self.scroll = None
        self.controls.clear()  # مسح العناصر الحالية
        self.controls.append(
            Column(
                controls=[
                    Container(
                        content=ProgressRing(visible=True),  # عرض حلقة التحميل
                        alignment=alignment.center,  # محاذاة الحلقة في المنتصف
                        height=float("inf"),  # جعل الحاوية تأخذ المساحة الكاملة
                        expand=True,  # توسيع الحاوية لملء المساحة المتاحة
                    ),
                ],
                expand=True,  # توسيع العمود لملء المساحة المتاحة
            )
        )
        self.update()  # تحديث الواجهة

    # دالة للتحقق من صحة البيانات المدخلة
    def checkTextBoxes(self):
        if not self.userNameTextBox.value:  # التحقق من أن حقل اسم المستخدم غير فارغ
            self.userNameTextBox.error = Text("الرجاء ادخال اسم المستخدم")  # عرض رسالة الخطأ
            self.update()  # تحديث الواجهة
            return False
        elif not self.passwordTextBox.value:  # التحقق من أن حقل كلمة المرور غير فارغ
            self.passwordTextBox.error = Text("الرجاء ادخال كلمة المرور")  # عرض رسالة الخطأ
            self.update()
            return False
        else:
            self.userNameTextBox.error = None  # إزالة رسالة الخطأ
            self.passwordTextBox.error = None  # إزالة رسالة الخطأ
            self.update()
            return True

    # دالة غير متزامنة لإرسال طلب تسجيل الدخول
    async def loginRequest(self, userName, password):
        body = {"username": userName, "password": password, "userType": 0}
        try:
            response = requests.post(url=f"{Login.baseUrl}/login/", data=body, timeout=5)
            json = response.json()
            if response.status_code == 200:
                await self.page.client_storage.set_async("access", json["access"])  # حفظ توكن الوصول
                await self.page.client_storage.set_async("refresh", json["refresh"])  # حفظ توكن التحديث
                userData = {
                    "username": json["username"],
                    "gender": json["gender"],
                    "first_name": json["first_name"],
                    "last_name": json["last_name"],
                    "profileImage": json["profileImage"],
                }
                await self.page.client_storage.set_async("userData", userData)  # حفظ بيانات المستخدم
                return [True, json]
            else:
                return [False, json["non_field_errors"][0]]  # إرجاع رسالة الخطأ
        except requests.exceptions.Timeout:
            return [False, "اتصال الانترنت بطئ"]
        except requests.exceptions.ConnectionError:
            return [False, "حدث خطأ في الاتصال بالخادم. تحقق من اتصالك بالإنترنت."]

    # دالة لمعالجة حدث تسجيل الدخول
    def LoginEvent(self):
        if self.checkTextBoxes():  # التحقق من صحة البيانات المدخلة
            self.loaderUi()  # عرض واجهة التحميل
            authState = self.page.run_task(
                self.loginRequest, self.userNameTextBox.value, self.passwordTextBox.value
            ).result()  # إرسال طلب تسجيل الدخول
            if authState[0]:  # إذا تم تسجيل الدخول بنجاح
                self.page.go("/home")  # الانتقال إلى الصفحة الرئيسية
            else:  # إذا فشل تسجيل الدخول
                self.controls.clear()  # مسح العناصر الحالية
                self.loginUi()  # إعادة عرض واجهة تسجيل الدخول
                snack_bar = SnackBar(  # عرض رسالة الخطأ
                    content=Text(
                        f"{authState[1]}",
                        style=TextStyle(size=15, font_family="ElMessiri"),
                    ),
                    show_close_icon=True,
                )
                self.page.open(snack_bar)
                self.update()  # تحديث الواجهة