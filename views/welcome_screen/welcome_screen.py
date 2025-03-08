# استيراد المكتبات الضرورية
from flet import (
    View,  # الفئة الأساسية لإنشاء واجهات المستخدم
    ScrollMode,  # لتحديد وضع التمرير (Auto, Always, Hidden, etc.)
    ResponsiveRow,  # لتنظيم العناصر في صفوف متجاوبة
    Container,  # حاوية لتجميع العناصر وتطبيق الأنماط
    Column,  # لتنظيم العناصر في أعمدة
    Image,  # لعرض الصور
    ImageFit,  # لتحديد كيفية ضبط الصورة داخل الحاوية
    border_radius,  # لتحديد زوايا مدورة للحاويات أو العناصر
    Text,  # لعرض النصوص
    FontWeight,  # لتحديد وزن الخط (عريض، عادي، إلخ)
    ElevatedButton,  # لعرض الأزرار المرفوعة
    ButtonStyle,  # لتخصيص نمط الأزرار
    RoundedRectangleBorder,  # لتحديد زوايا مدورة للأزرار
    TextStyle,  # لتخصيص نمط النصوص
    CrossAxisAlignment,  # لمحاذاة العناصر أفقيًا
    MainAxisAlignment,  # لمحاذاة العناصر عموديًا
)


# تعريف فئة Welcome التي تمثل شاشة الترحيب
class Welcome(View):

    # دالة البناء (Constructor) للفئة
    def __init__(self, route, page):
        super().__init__(route=route)  # استدعاء دالة البناء للفئة الأم (View)
        self.scroll = ScrollMode.HIDDEN  # تعيين وضع التمرير إلى تلقائي
        self.page = page
        self.controls.append(  # إضافة عناصر التحكم إلى الواجهة
            ResponsiveRow(  # استخدام ResponsiveRow لتنظيم العناصر بشكل متجاوب
                controls=[
                    Container(height=10),  # حاوية فارغة لخلق مسافة
                    Column(  # عمود لتجميع العناصر بشكل رأسي
                        controls=[
                            ResponsiveRow(  # صف متجاوب لعرض الصورة
                                controls=[
                                    Image(  # عرض صورة الشعار
                                        src="images/logo.png",
                                        fit=ImageFit.COVER,  # ضبط الصورة لتغطية المساحة المحددة
                                        border_radius=border_radius.all(
                                            20.0
                                        ),  # تعيين زوايا مدورة للصورة
                                        col={
                                            "xs": 10,
                                            "sm": 10,
                                            "md": 7,
                                            "lg": 5,
                                            "xl": 5,
                                        },  # تحديد حجم الصورة بناءً على حجم الشاشة
                                    ),
                                ],
                                expand=False,  # عدم توسيع الصف لملء المساحة المتاحة
                                alignment=MainAxisAlignment.CENTER,  # محاذاة العناصر في المنتصف
                            ),
                            Container(height=10),  # حاوية فارغة لخلق مسافة
                            Text(  # نص عنوان الشاشة
                                "حماية الاطفال",
                                size=20,  # حجم النص
                                weight=FontWeight.BOLD,  # وزن النص (عريض)
                                font_family="ElMessiri",  # نوع الخط
                            ),
                            Container(height=10),  # حاوية فارغة لخلق مسافة
                            Text(  # نص وصف الشاشة
                                "حارسك لأمان عائلتك",
                                size=20,  # حجم النص
                                weight=FontWeight.NORMAL,  # وزن النص (عادي)
                                font_family="ElMessiri",  # نوع الخط
                            ),
                            Container(height=10),  # حاوية فارغة لخلق مسافة
                            ResponsiveRow(  # صف متجاوب لعرض زر تسجيل الدخول
                                controls=[
                                    ElevatedButton(  # زر تسجيل الدخول
                                        "تسجيل الدخول",
                                        style=ButtonStyle(  # تخصيص نمط الزر
                                            shape=RoundedRectangleBorder(
                                                radius=22
                                            ),  # زوايا مدورة للزر
                                            bgcolor="#171335",  # لون خلفية الزر
                                            color="#ffffff",  # لون النص
                                            text_style=TextStyle(  # تخصيص نمط النص
                                                size=15,
                                                weight=FontWeight.BOLD,
                                                font_family="ElMessiri",
                                            ),
                                            padding=5,  # إضافة حشوة داخلية للزر
                                        ),
                                        on_click=lambda e: self.page.go(
                                            "/login"
                                        ),  # حدث النقر لتوجيه المستخدم إلى شاشة تسجيل الدخول
                                    ),
                                ]
                            ),
                            Container(height=10),  # حاوية فارغة لخلق مسافة
                            ResponsiveRow(  # صف متجاوب لعرض زر إنشاء حساب
                                controls=[
                                    ElevatedButton(  # زر إنشاء حساب
                                        "انشاء حساب",
                                        style=ButtonStyle(  # تخصيص نمط الزر
                                            shape=RoundedRectangleBorder(
                                                radius=22
                                            ),  # زوايا مدورة للزر
                                            bgcolor="#171335",  # لون خلفية الزر
                                            color="#ffffff",  # لون النص
                                            text_style=TextStyle(  # تخصيص نمط النص
                                                size=15,
                                                weight=FontWeight.BOLD,
                                                font_family="ElMessiri",
                                            ),
                                            padding=5,  # إضافة حشوة داخلية للزر
                                        ),
                                        on_click=lambda e: self.page.go(
                                            "/signup"
                                        ),  # حدث النقر لتوجيه المستخدم إلى شاشة إنشاء حساب
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
