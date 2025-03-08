# استيراد المكتبات الضرورية
from flet import (
    View,  # الفئة الأساسية لإنشاء واجهات المستخدم
    ScrollMode,  # لتحديد وضع التمرير (Auto, Always, Hidden, etc.)
    TextField,  # لحقول إدخال النص
    Container,  # حاوية لتجميع العناصر وتطبيق الأنماط
    Column,  # لتنظيم العناصر في أعمدة
    ResponsiveRow,  # لتنظيم العناصر في صفوف متجاوبة
    Image,  # لعرض الصور
    border_radius,  # لتحديد زوايا مدورة للحاويات أو العناصر
    Text,  # لعرض النصوص
    FontWeight,  # لتحديد وزن الخط (عريض، عادي، إلخ)
    ElevatedButton,  # لعرض الأزرار المرفوعة
    ButtonStyle,  # لتخصيص نمط الأزرار
    RoundedRectangleBorder,  # لتحديد زوايا مدورة للأزرار
    TextStyle,  # لتخصيص نمط النصوص
    CrossAxisAlignment,  # لمحاذاة العناصر أفقيًا
    MainAxisAlignment,  # لمحاذاة العناصر عموديًا
    icons,  # مكتبة الأيقونات المدمجة
    IconButton,  # زر يحتوي على أيقونة
    Dropdown,  # قائمة منسدلة
    dropdown,  # لتحديد خيارات القائمة المنسدلة
    Row,  # دائرة لعرض المحتوى
    SnackBar,  # لعرض الرسائل العابرة
    ProgressRing,  # حلقة التحميل
    alignment,  # لمحاذاة العناصر
    ImageFit,  # لإضافة حشوة داخلية
    TextAlign,
)
import requests


# تعريف فئة SignUp التي تمثل شاشة إنشاء الحساب
class SignUp(View):
    def __init__(self, route, page):
        super().__init__(route=route)  # استدعاء دالة البناء للفئة الأم (View)
        self.scroll = ScrollMode.HIDDEN  # تعيين وضع التمرير إلى تلقائي

        # تعريف حقل إدخال الاسم الأول
        self.firstNameTextBox = TextField(
            label="الاسم الاول",
            border_radius=border_radius.all(22),  # زوايا مدورة للحقل
            border_color="#171335",  # لون الحدود
            text_style=TextStyle(size=15, font_family="ElMessiri"),  # تخصيص نمط النص
            label_style=TextStyle(
                size=14, font_family="ElMessiri"
            ),  # تخصيص نمط التسمية
        )

        # تعريف حقل إدخال الاسم الأخير
        self.lastNameTextBox = TextField(
            label="الاسم الاخير",
            border_radius=border_radius.all(22),
            border_color="#171335",
            text_style=TextStyle(size=15, font_family="ElMessiri"),
            label_style=TextStyle(size=14, font_family="ElMessiri"),
        )

        # تعريف حقل إدخال اسم المستخدم
        self.userNameTextBox = TextField(
            label="اســـم المــستخدم",
            border_radius=border_radius.all(22),
            border_color="#171335",
            text_style=TextStyle(size=15, font_family="ElMessiri"),
            label_style=TextStyle(size=14, font_family="ElMessiri"),
        )

        # تعريف قائمة اختيار الجنس
        self.genderOptionMenu = Dropdown(
            label="الجنس",
            width=100,  # عرض القائمة
            options=[
                dropdown.Option(  # خيار "ذكر"
                    content=Text(
                        "ذكر",
                        text_align=TextAlign.RIGHT,  # محاذاة النص إلى اليمين
                        style=TextStyle(
                            size=13,
                            weight=FontWeight.NORMAL,
                            font_family="ElMessiri",
                        ),
                    ),
                    text=1,  # القيمة المرتبطة بالخيار
                    alignment=alignment.center_right,  # محاذاة الخيار إلى اليمين
                ),
                dropdown.Option(  # خيار "انثى"
                    content=Text(
                        "انثى",
                        text_align=TextAlign.RIGHT,
                        style=TextStyle(
                            size=13,
                            weight=FontWeight.NORMAL,
                            font_family="ElMessiri",
                        ),
                    ),
                    text=2,
                    alignment=alignment.center_right,
                ),
            ],
            label_style=TextStyle(  # تخصيص نمط تسمية القائمة
                size=13,
                weight=FontWeight.NORMAL,
                font_family="ElMessiri",
            ),
            border_radius=border_radius.all(22),  # زوايا مدورة للقائمة
        )

        # تعريف حقل إدخال كلمة المرور
        self.passwordTextBox = TextField(
            label="كــلمة المــرور",
            password=True,  # إخفاء النص
            can_reveal_password=True,  # إمكانية إظهار النص
            border_radius=border_radius.all(22),
            border_color="#171335",
            text_style=TextStyle(size=15, font_family="ElMessiri"),
            label_style=TextStyle(size=14, font_family="ElMessiri"),
        )

        # تعريف حقل إدخال تأكيد كلمة المرور
        self.rePasswordTextBox = TextField(
            label="تأكيد كــلمة المــرور",
            password=True,
            can_reveal_password=True,
            border_radius=border_radius.all(22),
            border_color="#171335",
            text_style=TextStyle(size=15, font_family="ElMessiri"),
            label_style=TextStyle(size=14, font_family="ElMessiri"),
        )

    # دالة تُستدعى عند تحميل الواجهة
    def did_mount(self):
        self.SignUpUi()

    # دالة لبناء واجهة إنشاء الحساب
    def SignUpUi(self):
        self.scroll = ScrollMode.HIDDEN
        self.controls.clear()  # مسح العناصر الحالية
        self.controls.append(
            ResponsiveRow(  # صف متجاوب لتنظيم العناصر
                controls=[
                    Row(  # صف لعرض زر الرجوع
                        controls=[
                            IconButton(
                                icon=icons.ARROW_BACK,  # أيقونة الرجوع
                                on_click=lambda e: self.page.go(
                                    "/"
                                ),  # حدث النقر للرجوع إلى الصفحة الرئيسية
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
                                        src="images/logo.png",
                                        fit=ImageFit.COVER,
                                        border_radius=border_radius.all(20.0),
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
                            Container(height=5),  # حاوية فارغة لخلق مسافة
                            Text(  # نص عنوان الشاشة
                                "حماية الاطفال",
                                size=20,
                                weight=FontWeight.BOLD,
                                font_family="ElMessiri",
                            ),
                            ResponsiveRow(  # صف متجاوب لعرض حقل الاسم الأول
                                controls=[self.firstNameTextBox],
                            ),
                            Container(height=5),
                            ResponsiveRow(  # صف متجاوب لعرض حقل الاسم الأخير
                                controls=[self.lastNameTextBox],
                            ),
                            Container(height=5),
                            ResponsiveRow(  # صف متجاوب لعرض قائمة اختيار الجنس
                                controls=[self.genderOptionMenu],
                            ),
                            Container(height=5),
                            self.userNameTextBox,  # عرض حقل اسم المستخدم
                            Container(height=5),
                            self.passwordTextBox,  # عرض حقل كلمة المرور
                            Container(height=5),
                            self.rePasswordTextBox,  # عرض حقل تأكيد كلمة المرور
                            Container(height=20),
                            ResponsiveRow(  # صف متجاوب لعرض زر إنشاء الحساب
                                controls=[
                                    ElevatedButton(
                                        "انــشاء حــساب",
                                        style=ButtonStyle(  # تخصيص نمط الزر
                                            shape=RoundedRectangleBorder(radius=22),
                                            bgcolor="#171335",
                                            color="#ffffff",
                                            text_style=TextStyle(
                                                size=15,
                                                weight=FontWeight.BOLD,
                                                font_family="ElMessiri",
                                            ),
                                            padding=5,
                                        ),
                                        on_click=lambda e: self.SignUpEvent(),  # حدث النقر لإنشاء الحساب
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
        self.controls.clear()
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
        self.update()

    # دالة للتحقق من صحة البيانات المدخلة
    def checkTextBoxData(self):
        errors = [
            True if self.firstNameTextBox.value != "" else "الرجاء ادخال اسمك الاول",
            True if self.lastNameTextBox.value != "" else "الرجاء ادخال اسمك الاخير",
            True if self.genderOptionMenu.value != None else "الرجاء اختيار الجنس",
            (
                True
                if len(self.userNameTextBox.value) > 2
                and self.userNameTextBox.value != ""
                else "يجب ان يتكون اسم المستخدم من 3 احرف على الاقل"
            ),
            (
                True
                if len(self.passwordTextBox.value) > 5
                and self.passwordTextBox.value != ""
                else "يجب ان تتكون كلمة المرور  من 6 احرف على الاقل"
            ),
            (
                True
                if self.rePasswordTextBox.value != ""
                else "الرجاء ادخال تاكيد كلمة المرور"
            ),
            (
                True
                if self.passwordTextBox.value == self.rePasswordTextBox.value
                else "كلمة المرور غير متطابقة"
            ),
        ]

        textBoxes = [
            self.firstNameTextBox,
            self.lastNameTextBox,
            self.genderOptionMenu,
            self.userNameTextBox,
            self.passwordTextBox,
            self.rePasswordTextBox,
            self.rePasswordTextBox,
        ]

        state = True
        for index, error in enumerate(errors):
            if error != True:
                state = False
                textBoxes[index].error = Text(f"{error}")  # عرض رسالة الخطأ
            else:
                textBoxes[index].error = None  # إزالة رسالة الخطأ
        self.update()
        textBoxes.pop()
        return [
            [text.value for text in textBoxes],
            state,
        ]  # إرجاع البيانات وحالة التحقق

    # دالة غير متزامنة لإرسال طلب إنشاء الحساب
    async def SignUpRequest(self, data):
        body = {
            "first_name": data[0],
            "last_name": data[1],
            "gender": data[2],
            "username": data[3],
            "password": data[4],
            "userType": 0,
        }
        try:
            response = requests.post(url=f"{SignUp.baseUrl}/signup/", data=body)
            json = response.json()
            if response.status_code == 200:
                await self.page.client_storage.set_async(
                    "access", json["access"]
                )  # حفظ توكن الوصول
                await self.page.client_storage.set_async(
                    "refresh", json["refresh"]
                )  # حفظ توكن التحديث
                userData = {
                    "username": json["username"],
                    "gender": json["gender"],
                    "first_name": json["first_name"],
                    "last_name": json["last_name"],
                    "profileImage": json["profileImage"],
                }
                await self.page.client_storage.set_async(
                    "userData", userData
                )  # حفظ بيانات المستخدم
                return [True, "تم انشاء الحساب بنجاح"]
            else:
                return [False, json["username"][0]]  # إرجاع رسالة الخطأ
        except requests.exceptions.Timeout:
            return [False, "اتصال الانترنت بطئ"]
        except requests.exceptions.ConnectionError:
            return [False, "حدث خطأ في الاتصال بالخادم. تحقق من اتصالك بالإنترنت."]

    # دالة لمعالجة حدث إنشاء الحساب
    def SignUpEvent(self):
        data, state = self.checkTextBoxData()  # التحقق من صحة البيانات
        if state:
            self.loaderUi()  # عرض واجهة التحميل
            authState = self.page.run_task(
                self.SignUpRequest, data
            ).result()  # إرسال طلب إنشاء الحساب
            if authState[0]:  # إذا تم إنشاء الحساب بنجاح
                self.page.go("/home")  # الانتقال إلى الصفحة الرئيسية
            else:
                self.SignUpUi()  # إعادة عرض واجهة إنشاء الحساب
                snack_bar = SnackBar(  # عرض رسالة الخطأ
                    content=Text(
                        f"{authState[1]}",
                        style=TextStyle(size=15, font_family="ElMessiri"),
                    ),
                    show_close_icon=True,
                )
                self.page.open(snack_bar)
                self.update()  # تحديث الواجهة
