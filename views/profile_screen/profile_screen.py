# استيراد المكتبات الضرورية
from flet import *
import requests

# تعريف فئة PersonalInformation التي تمثل شاشة تعديل المعلومات الشخصية
class PersonalInformation(View):
    def __init__(self, route, page):
        super().__init__(route=route)  # استدعاء دالة البناء للفئة الأم (View)
        self.scroll = ScrollMode.AUTO  # تعيين وضع التمرير إلى تلقائي
        self.page = page  # حفظ صفحة التطبيق

        # تعريف AppBar (شريط التطبيق العلوي)
        self.appbar = AppBar(
            leading=IconButton(
                icon=icons.ARROW_BACK,
                icon_color="#ffffff",
                on_click=lambda x: self.page.go("/Profile"),  # حدث النقر للرجوع إلى صفحة الملف الشخصي
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

        # تعريف حقول إدخال البيانات
        self.userName = Ref[TextField]()  # مرجع لحقل اسم المستخدم
        self.firstName = Ref[TextField]()  # مرجع لحقل الاسم الأول
        self.lastName = Ref[TextField]()  # مرجع لحقل الاسم الأخير

    # دالة لبناء واجهة تعديل المعلومات الشخصية
    def buildUi(self):
        self.controls.clear()
        userData = self.page.client_storage.get("userData")  # الحصول على بيانات المستخدم
        self.controls.append(
            ResponsiveRow(
                controls=[
                    Column(
                        controls=[
                            Container(
                                content=Image(
                                    src=f"{PersonalInformation.baseUrl}{userData['profileImage']}",  # عرض صورة الملف الشخصي
                                    width=250,
                                ),
                                border_radius=border_radius.all(150),  # زوايا مدورة للصورة
                                width=200,
                                height=200,
                                border=border.all(width=0.5, color="black"),  # إطار حول الصورة
                            ),
                            Container(height=20),
                            ResponsiveRow(
                                controls=[
                                    Text(
                                        "تعديل المعلومات الشخصية",
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
                            Container(height=10),
                            ResponsiveRow(
                                controls=[
                                    TextField(
                                        label="اسم المستخدم",
                                        border_radius=border_radius.all(22),  # زوايا مدورة للحقل
                                        border_color="#171335",  # لون الحدود
                                        text_style=TextStyle(size=15, font_family="ElMessiri"),  # تخصيص نمط النص
                                        label_style=TextStyle(size=14, font_family="ElMessiri"),  # تخصيص نمط التسمية
                                        ref=self.userName,  # ربط الحقل بالمرجع
                                        value=userData["username"],  # تعيين القيمة الافتراضية
                                    ),
                                ],
                            ),
                            Container(height=10),
                            ResponsiveRow(
                                controls=[
                                    TextField(
                                        label="الاسم الاول",
                                        border_radius=border_radius.all(22),
                                        border_color="#171335",
                                        text_style=TextStyle(size=15, font_family="ElMessiri"),
                                        label_style=TextStyle(size=14, font_family="ElMessiri"),
                                        ref=self.firstName,
                                        value=userData["first_name"],
                                    ),
                                ],
                            ),
                            Container(height=10),
                            ResponsiveRow(
                                controls=[
                                    TextField(
                                        label="الاسم الاخير",
                                        border_radius=border_radius.all(22),
                                        border_color="#171335",
                                        text_style=TextStyle(size=15, font_family="ElMessiri"),
                                        label_style=TextStyle(size=14, font_family="ElMessiri"),
                                        ref=self.lastName,
                                        value=userData["last_name"],
                                    ),
                                ],
                            ),
                            Container(height=10),
                            ResponsiveRow(
                                controls=[
                                    ElevatedButton(
                                        "حفظ التعديلات",
                                        style=ButtonStyle(
                                            shape=RoundedRectangleBorder(radius=22),  # زوايا مدورة للزر
                                            bgcolor="#171335",  # لون خلفية الزر
                                            color="#ffffff",  # لون النص
                                            text_style=TextStyle(
                                                size=15,
                                                weight=FontWeight.BOLD,
                                                font_family="ElMessiri",
                                            ),
                                            padding=5,  # إضافة حشوة داخلية للزر
                                        ),
                                        on_click=self.changeData,  # حدث النقر لحفظ التعديلات
                                    ),
                                ]
                            ),
                        ],
                        horizontal_alignment=CrossAxisAlignment.CENTER,  # محاذاة العناصر أفقياً في المنتصف
                        alignment=MainAxisAlignment.CENTER,  # محاذاة العناصر عمودياً في المنتصف
                    )
                ],
                vertical_alignment=CrossAxisAlignment.CENTER,  # محاذاة العناصر رأسيًا في المنتصف
                alignment=alignment.center,  # محاذاة العناصر في المنتصف
            ),
        )
        self.update()  # تحديث الواجهة

    # دالة تُستدعى عند تحميل الواجهة
    def did_mount(self):
        self.buildUi()  # بناء واجهة تعديل المعلومات الشخصية

    # دالة لإرسال طلبات PATCH إلى الخادم لتحديث البيانات
    async def sendPatchRequest(self, url, body={}):
        body = {
            "action": "updatePersonaInfo",
            "username": f"{body[0]}",
            "first_name": f"{body[1]}",
            "last_name": f"{body[2]}",
        }
        access = await self.page.client_storage.get_async("access")  # الحصول على توكن الوصول
        headers = {
            "Authorization": f"Bearer {access}",  # إضافة التوكن إلى رأس الطلب
            "Accept": "*/*",
            "Cache-Control": "no-cache",
        }
        try:
            response = requests.patch(
                url=f"{PersonalInformation.baseUrl}/{url}/", data=body, headers=headers
            )
            json = response.json()
            if response.status_code == 200:
                return [True, json]  # إرجاع النتيجة الناجحة
            else:
                return [False, json]  # إرجاع النتيجة الفاشلة
        except requests.exceptions.Timeout:
            return [False, "اتصال الانترنت بطئ"]  # التعامل مع انقطاع الاتصال
        except requests.exceptions.ConnectionError:
            return [False, "حدث خطأ في الاتصال بالخادم. تحقق من اتصالك بالإنترنت."]  # التعامل مع أخطاء الاتصال

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
                        alignment=alignment.center,
                        height=float("inf"),  # جعل الحاوية تأخذ المساحة الكاملة
                        expand=True,  # توسيع الحاوية لملء المساحة المتاحة
                    ),
                ],
                expand=True,  # توسيع العمود لملء المساحة المتاحة
            )
        )
        self.update()  # تحديث الواجهة

    # دالة للتحقق من صحة البيانات المدخلة
    def checkTextBoxData(self):
        errors = [
            True if self.userName.current.value != "" else "الرجاء ادخال اسم المستخدم",
            True if self.firstName.current.value != "" else "الرجاء ادخال اسمك الاول",
            True if self.lastName.current.value != "" else "الرجاء ادخال اسمك الاخير",
            (
                True
                if len(self.userName.current.value) > 2 and self.userName.current.value != ""
                else "يجب ان يتكون اسم المستخدم من 3 احرف على الاقل"
            ),
        ]
        textBoxes = [
            self.userName,
            self.firstName,
            self.lastName,
            self.userName,
        ]
        state = True
        for index, error in enumerate(errors):
            if error != True:
                state = False
                textBoxes[index].current.error = Text(f"{error}")  # عرض رسالة الخطأ
            else:
                textBoxes[index].current.error = None  # إزالة رسالة الخطأ
        self.update()
        textBoxes.pop()
        return [[text.current.value for text in textBoxes], state]  # إرجاع البيانات وحالة التحقق

    # دالة لعرض رسائل للمستخدم
    def showMessage(self, message):
        snack_bar = SnackBar(
            content=Text(
                f"{message}",
                style=TextStyle(size=15, font_family="ElMessiri"),
            ),
            show_close_icon=True,
        )
        self.page.open(snack_bar)  # عرض الرسالة

    # دالة لتحديث بيانات المستخدم
    def updateUserData(self, result):
        userData = {
            "username": result["username"],
            "gender": result["gender"],
            "first_name": result["first_name"],
            "last_name": result["last_name"],
            "profileImage": result["profileImage"],
        }
        self.page.client_storage.set("userData", userData)  # حفظ البيانات المحدثة

    # دالة لتغيير البيانات الشخصية
    def changeData(self, e):
        values, textBoxState = self.checkTextBoxData()  # التحقق من صحة البيانات المدخلة
        if textBoxState:
            self.loaderUi()  # عرض واجهة التحميل
            state, result = self.page.run_task(
                self.sendPatchRequest, "updateUser", values
            ).result()
            if state:
                self.updateUserData(result)  # تحديث بيانات المستخدم
                self.showMessage("تم تحديث البيانات بنجاح")  # عرض رسالة النجاح
                self.did_mount()  # إعادة تحميل الواجهة
            else:
                self.did_mount()
                self.showMessage(result)  # عرض رسالة الخطأ


# تعريف فئة SecurityPasswords التي تمثل شاشة تغيير كلمة المرور
class SecurityPasswords(View):
    def __init__(self, route, page):
        super().__init__(route=route)  # استدعاء دالة البناء للفئة الأم (View)
        self.scroll = ScrollMode.AUTO  # تعيين وضع التمرير إلى تلقائي
        self.page = page  # حفظ صفحة التطبيق

        # تعريف AppBar (شريط التطبيق العلوي)
        self.appbar = AppBar(
            leading=IconButton(
                icon=icons.ARROW_BACK,
                icon_color="#ffffff",
                on_click=lambda x: self.page.go("/Profile"),  # حدث النقر للرجوع إلى صفحة الملف الشخصي
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

        # تعريف حقول إدخال كلمات المرور
        self.currentPassword = Ref[TextField]()  # مرجع لحقل كلمة المرور الحالية
        self.newPassword = Ref[TextField]()  # مرجع لحقل كلمة المرور الجديدة
        self.newRePassword = Ref[TextField]()  # مرجع لحقل تأكيد كلمة المرور الجديدة

    # دالة لبناء واجهة تغيير كلمة المرور
    def buildUi(self):
        self.controls.clear()
        self.controls.append(
            ResponsiveRow(
                controls=[
                    Column(
                        controls=[
                            Container(height=10),
                            ResponsiveRow(
                                controls=[
                                    Text(
                                        "تغيير كلمة مرور حسابك",
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
                            Container(height=10),
                            ResponsiveRow(
                                controls=[
                                    TextField(
                                        label="كلمة المرور الحالية",
                                        border_radius=border_radius.all(22),  # زوايا مدورة للحقل
                                        border_color="#171335",  # لون الحدود
                                        text_style=TextStyle(size=15, font_family="ElMessiri"),  # تخصيص نمط النص
                                        label_style=TextStyle(size=14, font_family="ElMessiri"),  # تخصيص نمط التسمية
                                        password=True,  # إخفاء النص
                                        can_reveal_password=True,  # إمكانية إظهار النص
                                        ref=self.currentPassword,  # ربط الحقل بالمرجع
                                    ),
                                ],
                            ),
                            Container(height=10),
                            ResponsiveRow(
                                controls=[
                                    TextField(
                                        label="كلمة المرور الجديدة",
                                        border_radius=border_radius.all(22),
                                        border_color="#171335",
                                        text_style=TextStyle(size=15, font_family="ElMessiri"),
                                        label_style=TextStyle(size=14, font_family="ElMessiri"),
                                        password=True,
                                        can_reveal_password=True,
                                        ref=self.newPassword,
                                    ),
                                ],
                            ),
                            Container(height=10),
                            ResponsiveRow(
                                controls=[
                                    TextField(
                                        label="تأكيد كلمة المرور الحديدة",
                                        border_radius=border_radius.all(22),
                                        border_color="#171335",
                                        text_style=TextStyle(size=15, font_family="ElMessiri"),
                                        label_style=TextStyle(size=14, font_family="ElMessiri"),
                                        password=True,
                                        can_reveal_password=True,
                                        ref=self.newRePassword,
                                    ),
                                ],
                            ),
                            Container(height=10),
                            ResponsiveRow(
                                controls=[
                                    ElevatedButton(
                                        "حفظ التعديلات",
                                        style=ButtonStyle(
                                            shape=RoundedRectangleBorder(radius=22),  # زوايا مدورة للزر
                                            bgcolor="#171335",  # لون خلفية الزر
                                            color="#ffffff",  # لون النص
                                            text_style=TextStyle(
                                                size=15,
                                                weight=FontWeight.BOLD,
                                                font_family="ElMessiri",
                                            ),
                                            padding=5,  # إضافة حشوة داخلية للزر
                                        ),
                                        on_click=self.updatePassword,  # حدث النقر لتحديث كلمة المرور
                                    ),
                                ]
                            ),
                        ],
                        horizontal_alignment=CrossAxisAlignment.CENTER,  # محاذاة العناصر أفقياً في المنتصف
                        alignment=MainAxisAlignment.CENTER,  # محاذاة العناصر عمودياً في المنتصف
                    )
                ],
                vertical_alignment=CrossAxisAlignment.CENTER,  # محاذاة العناصر رأسيًا في المنتصف
                alignment=alignment.center,  # محاذاة العناصر في المنتصف
            ),
        )
        self.update()  # تحديث الواجهة

    # دالة تُستدعى عند تحميل الواجهة
    def did_mount(self):
        self.buildUi()  # بناء واجهة تغيير كلمة المرور

    # دالة لإرسال طلبات PATCH إلى الخادم لتحديث كلمة المرور
    async def sendPatchRequest(self, url, body={}):
        body = {
            "action": "updatePassword",
            "currentPassword": f"{body[0]}",
            "newPassword": f"{body[1]}",
            "rePassword": f"{body[2]}",
        }
        access = await self.page.client_storage.get_async("access")  # الحصول على توكن الوصول
        headers = {
            "Authorization": f"Bearer {access}",  # إضافة التوكن إلى رأس الطلب
            "Accept": "*/*",
            "Cache-Control": "no-cache",
        }
        try:
            response = requests.patch(
                url=f"{SecurityPasswords.baseUrl}/{url}/", data=body, headers=headers
            )
            json = response.json()
            if response.status_code == 200:
                return [True, json]  # إرجاع النتيجة الناجحة
            else:
                return [False, json]  # إرجاع النتيجة الفاشلة
        except requests.exceptions.Timeout:
            return [False, "اتصال الانترنت بطئ"]  # التعامل مع انقطاع الاتصال
        except requests.exceptions.ConnectionError:
            return [False, "حدث خطأ في الاتصال بالخادم. تحقق من اتصالك بالإنترنت."]  # التعامل مع أخطاء الاتصال

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
                        alignment=alignment.center,
                        height=float("inf"),  # جعل الحاوية تأخذ المساحة الكاملة
                        expand=True,  # توسيع الحاوية لملء المساحة المتاحة
                    ),
                ],
                expand=True,  # توسيع العمود لملء المساحة المتاحة
            )
        )
        self.update()  # تحديث الواجهة

    # دالة للتحقق من صحة البيانات المدخلة
    def checkTextBoxData(self):
        errors = [
            True if self.currentPassword.current.value != "" else "الرجاء ادخال كلمة السر الحالية",
            True if self.newPassword.current.value != "" else "الرجاء ادخال كلمةالسر الجديدة ",
            True if self.newRePassword.current.value != "" else "الرجاء ادخال  تأكيد كلمة المرور الجديدة",
            (
                True
                if self.newPassword.current.value == self.newRePassword.current.value 
                else "كلمة المرور غير متطابقة"
            ),
        ]
        textBoxes = [
            self.currentPassword,
            self.newPassword,
            self.newRePassword,
            self.newRePassword,
        ]
        state = True
        for index, error in enumerate(errors):
            if error != True:
                state = False
                textBoxes[index].current.error = Text(f"{error}")  # عرض رسالة الخطأ
            else:
                textBoxes[index].current.error = None  # إزالة رسالة الخطأ
        self.update()
        textBoxes.pop()
        return [[text.current.value for text in textBoxes], state]  # إرجاع البيانات وحالة التحقق

    # دالة لعرض رسائل للمستخدم
    def showMessage(self, message):
        snack_bar = SnackBar(
            content=Text(
                f"{message}",
                style=TextStyle(size=15, font_family="ElMessiri"),
            ),
            show_close_icon=True,
        )
        self.page.open(snack_bar)  # عرض الرسالة

    # دالة لتحديث بيانات المستخدم
    def updateUserData(self, result):
        userData = {
            "username": result["username"],
            "gender": result["gender"],
            "first_name": result["first_name"],
            "last_name": result["last_name"],
            "profileImage": result["profileImage"],
        }
        self.page.client_storage.set("userData", userData)  # حفظ البيانات المحدثة

    # دالة لتحديث كلمة المرور
    def updatePassword(self, e):
        values, textBoxState = self.checkTextBoxData()  # التحقق من صحة البيانات المدخلة
        if textBoxState:
            self.loaderUi()  # عرض واجهة التحميل
            state, result = self.page.run_task(
                self.sendPatchRequest, "updateUser", values
            ).result()
            if state:
                self.updateUserData(result)  # تحديث بيانات المستخدم
                self.showMessage("تم تحديث كلمة المرور بنجاح")  # عرض رسالة النجاح
                self.did_mount()  # إعادة تحميل الواجهة
            else:
                self.did_mount()
                self.showMessage(result["password"])  # عرض رسالة الخطأ


# تعريف فئة Profile التي تمثل شاشة الملف الشخصي
class Profile(View):
    def __init__(self, route, page):
        super().__init__(route=route)  # استدعاء دالة البناء للفئة الأم (View)
        self.page = page  # حفظ صفحة التطبيق
        self.scroll = ScrollMode.AUTO  # تعيين وضع التمرير إلى تلقائي

        # تعريف FilePicker لاختيار صورة الملف الشخصي
        self.selector = FilePicker(on_result=self.ChangeProfileImage)
        self.page.overlay.append(self.selector)  # إضافة FilePicker إلى الصفحة

        # تعريف BottomSheet لتغيير صورة الملف الشخصي
        self.BottomSheet = BottomSheet(
            content=Container(
                content=Column(
                    tight=True,
                    controls=[
                        TextButton(
                            text="تغيير صورة الملف الشخصي",
                            icon=icons.ADD_A_PHOTO,
                            on_click=lambda _: self.selector.pick_files(
                                allow_multiple=False,
                                allowed_extensions=["jpg", "jpeg", "png"],
                                dialog_title="اختيار صورة ملف شخصي",
                                file_type=FilePickerFileType.IMAGE,
                            ),
                            width=float("inf"),
                        ),
                    ],
                ),
                width=float("inf"),
                padding=20,
            ),
        )

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
        self.controls.clear()
        loader = self.loaderUi()  # عرض واجهة التحميل
        self.controls.append(loader)
        self.buildUi()  # بناء واجهة الملف الشخصي

    # دالة لبناء واجهة الملف الشخصي
    def buildUi(self):
        self.controls.clear()
        userData = self.page.run_task(
            self.page.client_storage.get_async, "userData"
        ).result()  # الحصول على بيانات المستخدم
        self.controls.append(
            ResponsiveRow(
                controls=[
                    Container(height=10),
                    Column(
                        controls=[
                            Container(
                                content=Image(
                                    src=f"{Profile.baseUrl}{userData['profileImage']}",  # عرض صورة الملف الشخصي
                                    width=250,
                                ),
                                border_radius=border_radius.all(150),  # زوايا مدورة للصورة
                                on_click=lambda e: self.page.open(self.BottomSheet),  # حدث النقر لفتح BottomSheet
                                width=200,
                                height=200,
                                border=border.all(width=0.5, color="black"),  # إطار حول الصورة
                            ),
                            Container(
                                content=Text(
                                    f"{userData['first_name']} {userData['last_name']}",  # عرض اسم المستخدم
                                    size=20,
                                    weight=FontWeight.BOLD,
                                    color="#666666",
                                    font_family="ElMessiri",
                                ),
                            ),
                            Container(height=30),
                            Column(
                                controls=[
                                    ResponsiveRow(
                                        controls=[
                                            Container(
                                                content=ListTile(
                                                    title=Text(
                                                        "البيانات الشخصية",
                                                        style=TextStyle(
                                                            size=15,
                                                            weight=FontWeight.BOLD,
                                                            font_family="ElMessiri",
                                                        ),
                                                    ),
                                                    trailing=IconButton(
                                                        icon=icons.PERSON,
                                                    ),
                                                ),
                                                bgcolor="#ffffff",
                                                border=border.all(0.5, "#110b22"),
                                                border_radius=border_radius.all(5),
                                                on_click=lambda x: self.page.go(
                                                    "/PersonalInformation"
                                                ),  # حدث النقر للانتقال إلى صفحة تعديل المعلومات الشخصية
                                            ),
                                        ],
                                    ),
                                    ResponsiveRow(
                                        controls=[
                                            Container(
                                                content=ListTile(
                                                    title=Text(
                                                        "الامان وكلمة المرور",
                                                        style=TextStyle(
                                                            size=15,
                                                            weight=FontWeight.BOLD,
                                                            font_family="ElMessiri",
                                                        ),
                                                    ),
                                                    trailing=IconButton(
                                                        icon=icons.LOCK,
                                                    ),
                                                ),
                                                bgcolor="#ffffff",
                                                border=border.all(0.5, "#110b22"),
                                                border_radius=border_radius.all(5),
                                                on_click=lambda x: self.page.go(
                                                    "/SecurityPasswords"
                                                ),  # حدث النقر للانتقال إلى صفحة تغيير كلمة المرور
                                            ),
                                        ],
                                    ),
                                    ResponsiveRow(
                                        controls=[
                                            Container(
                                                content=ListTile(
                                                    title=Text(
                                                        "تسجيل الخروج",
                                                        style=TextStyle(
                                                            size=15,
                                                            weight=FontWeight.BOLD,
                                                            font_family="ElMessiri",
                                                        ),
                                                    ),
                                                    trailing=IconButton(
                                                        icon=icons.LOGOUT,
                                                    ),
                                                ),
                                                bgcolor="#ffffff",
                                                border=border.all(0.5, "#110b22"),
                                                border_radius=border_radius.all(5),
                                                on_click=lambda e: self.logOut(),  # حدث النقر لتسجيل الخروج
                                            ),
                                        ],
                                    ),
                                ]
                            ),
                        ],
                        horizontal_alignment=CrossAxisAlignment.CENTER,  # محاذاة العناصر أفقياً في المنتصف
                        alignment=MainAxisAlignment.CENTER,  # محاذاة العناصر عمودياً في المنتصف
                    ),
                ],
                expand=True,
            )
        )
        self.update()  # تحديث الواجهة

    # دالة لتسجيل الخروج
    def logOut(self):
        self.page.client_storage.clear()  # مسح التخزين المحلي
        self.page.go("/")  # الانتقال إلى الصفحة الرئيسية

    # دالة لإرسال طلبات PUT إلى الخادم لتحديث صورة الملف الشخصي
    async def sendPutRequest(self, url, files={}):
        access = await self.page.client_storage.get_async("access")  # الحصول على توكن الوصول
        headers = {
            "Authorization": f"Bearer {access}",  # إضافة التوكن إلى رأس الطلب
            "Accept": "*/*",
            "Cache-Control": "no-cache",
        }
        try:
            response = requests.put(
                url=f"{Profile.baseUrl}/{url}/", files=files, headers=headers
            )
            json = response.json()
            if response.status_code == 200:
                userData = {
                    "username": json["username"],
                    "gender": json["gender"],
                    "first_name": json["first_name"],
                    "last_name": json["last_name"],
                    "profileImage": json["profileImage"],
                }
                await self.page.client_storage.set_async("userData", userData)  # حفظ البيانات المحدثة
                return [True, json]  # إرجاع النتيجة الناجحة
            else:
                return [False, json]  # إرجاع النتيجة الفاشلة
        except requests.exceptions.Timeout:
            return [False, "اتصال الانترنت بطئ"]  # التعامل مع انقطاع الاتصال
        except requests.exceptions.ConnectionError:
            return [False, "حدث خطأ في الاتصال بالخادم. تحقق من اتصالك بالإنترنت."]  # التعامل مع أخطاء الاتصال

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
        self.update()  # تحديث الواجهة

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

    # دالة لتغيير صورة الملف الشخصي
    def ChangeProfileImage(self, e):
        self.page.close(self.BottomSheet)  # إغلاق BottomSheet
        if e.files:
            self.controls.clear()
            loader = self.loaderUi()  # عرض واجهة التحميل
            self.controls.append(loader)
            self.update()
            files = {
                "Image": ("image.jpg", open(f"{e.files[0].path}", "rb"), "image/jpeg"),  # تحضير الملف للرفع
            }
            state, result = self.page.run_task(
                self.sendPutRequest, "uploadProfileImage", files
            ).result()
            if state:
                self.did_mount()  # إعادة تحميل الواجهة
            else:
                self.ErrorUi()  # عرض واجهة الخطأ