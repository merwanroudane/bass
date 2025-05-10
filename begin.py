import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import arabic_reshaper
from bidi.algorithm import get_display

# تعديل عرض النص العربي في الرسومات
plt.rcParams['font.family'] = 'Arial'


# وظيفة لعرض النص العربي بشكل صحيح
def display_arabic_text(text):
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    return bidi_text


# إعداد صفحة التطبيق
st.set_page_config(
    page_title="أساسيات القياس الاقتصادي",
    page_icon="📊",
    layout="wide"
)

# تصميم الواجهة الرئيسية
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 42px;
        color: #1E88E5;
        margin-bottom: 20px;
    }
    .section-title {
        font-size: 28px;
        color: #0D47A1;
        margin-top: 30px;
        margin-bottom: 15px;
    }
    .subsection-title {
        font-size: 22px;
        color: #1565C0;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .content-text {
        font-size: 18px;
        text-align: right;
        direction: rtl;
    }
    .highlighted {
        background-color: #E3F2FD;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .tip-box {
        background-color: #FFECB3;
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #FFC107;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">دليل أساسيات القياس الاقتصادي للمبتدئين</h1>', unsafe_allow_html=True)

# القائمة الجانبية
st.sidebar.title("المحتويات")
sections = [
    "المقدمة",
    "أنواع البيانات",
    "تحليل البيانات الوصفي",
    "نموذج الانحدار الخطي البسيط",
    "نموذج الانحدار المتعدد",
    "مشاكل الانحدار وحلولها",
    "اختبار الفرضيات",
    "تقييم النماذج",
    "تطبيق عملي"
]
section = st.sidebar.radio("اختر القسم", sections)

# بيانات عشوائية للأمثلة
np.random.seed(42)
n = 100
X1 = np.random.normal(size=n)
X2 = np.random.normal(size=n)
X3 = 0.5 * X1 + 0.3 * X2 + np.random.normal(size=n, scale=0.5)
Y = 3 + 2 * X1 + 1.5 * X2 + 0.5 * X3 + np.random.normal(size=n)

data = pd.DataFrame({
    'الدخل': X1 * 1000 + 5000,
    'الاستهلاك': Y * 500 + 2000,
    'الاستثمار': X2 * 300 + 1000,
    'الإنفاق الحكومي': X3 * 200 + 800
})

# المقدمة
if section == "المقدمة":
    st.markdown('<h2 class="section-title">المقدمة لعلم القياس الاقتصادي</h2>', unsafe_allow_html=True)

    st.markdown('<div class="content-text">', unsafe_allow_html=True)
    st.markdown("""
    ### واش راك خويا/أختي! مرحبا بيك في عالم القياس الاقتصادي 📊

    القياس الاقتصادي (Econometrics) هو علم يجمع بين الاقتصاد، الرياضيات والإحصاء باش نقدرو نحللو البيانات الاقتصادية ونبنيو نماذج تساعدنا نفهمو العلاقات بين المتغيرات ونتنبأو بالمستقبل.

    ### علاه مهم نتعلمو القياس الاقتصادي؟

    1. **تحليل الظواهر الاقتصادية**: يساعدنا نفهمو كيفاش يتأثر الاقتصاد بالعوامل المختلفة
    2. **اتخاذ القرارات**: يعاون صناع القرار يتخذو قرارات مبنية على أدلة وبيانات
    3. **التنبؤ**: يمكننا من التنبؤ بالتغيرات الاقتصادية المستقبلية
    4. **اختبار النظريات**: نقدرو نختبرو النظريات الاقتصادية بالأرقام والتحليل

    ### واش راح نتعلمو في هذا الدليل؟

    - كيفاش نجمعو ونحضرو البيانات
    - كيفاش نديرو تحليل وصفي للبيانات
    - كيفاش نبنيو نماذج الانحدار البسيط والمتعدد
    - كيفاش نتعاملو مع مشاكل النماذج
    - كيفاش نقيمو النماذج ونختارو الأفضل
    - كيفاش نطبقو هاد المعرفة على مشاكل حقيقية
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="tip-box content-text">', unsafe_allow_html=True)
    st.markdown("""
    ### نصيحة للطلبة المبتدئين:

    ما تقلقش! القياس الاقتصادي يبان صعيب في البداية، لكن مع الممارسة والصبر راح تفهمو وتحبو. خود وقتك، طبق اللي تعلمتو على بيانات حقيقية، وما تخافش تسأل وتناقش مع زملائك والأساتذة. الطريق للخبرة يبدأ بالخطوة الأولى!
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# أنواع البيانات
elif section == "أنواع البيانات":
    st.markdown('<h2 class="section-title">أنواع البيانات في القياس الاقتصادي</h2>', unsafe_allow_html=True)

    st.markdown('<div class="content-text">', unsafe_allow_html=True)
    st.markdown("""
    ### أنواع البيانات اللي نستخدموها في القياس الاقتصادي:

    #### 1. بيانات السلاسل الزمنية (Time Series Data)
    هي بيانات متغير واحد أو أكثر مسجلة عبر فترات زمنية متتالية. مثلا: معدل البطالة في الجزائر من 2000 ل 2023.

    #### 2. بيانات مقطعية (Cross-Sectional Data)
    هي بيانات لعدة وحدات (أفراد، شركات، دول) في وقت معين. مثلا: دخل الأسر في ولايات الجزائر في سنة 2023.

    #### 3. بيانات البانل (Panel Data)
    تجمع بين النوعين السابقين، يعني بيانات لعدة وحدات على مدى فترة زمنية. مثلا: معدلات النمو لـ 10 دول عربية من 2010 لـ 2023.

    #### 4. بيانات كمية ونوعية:
    - **البيانات الكمية**: أرقام قابلة للقياس مثل الدخل، الأسعار، معدل البطالة
    - **البيانات النوعية**: متغيرات وصفية مثل الجنس، المستوى التعليمي، المنطقة الجغرافية

    ### كيفاش نحصلو على البيانات؟

    1. **مصادر رسمية**: 
       - الديوان الوطني للإحصائيات (ONS)
       - بنك الجزائر
       - الوزارات المختلفة

    2. **مصادر دولية**:
       - البنك الدولي
       - صندوق النقد الدولي
       - منظمة الأمم المتحدة

    3. **المسوحات والاستبيانات**: جمع البيانات الأولية من خلال استبيانات أو مقابلات
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    # عرض مثال لكل نوع
    st.markdown('<h3 class="subsection-title">أمثلة على أنواع البيانات</h3>', unsafe_allow_html=True)

    # مثال بيانات سلسلة زمنية
    years = np.arange(2010, 2024)
    gdp_growth = np.array([3.6, 2.8, 3.4, 2.8, 3.8, 3.7, 3.2, 1.3, 1.2, 0.8, -4.9, 3.5, 3.1, 4.1])

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years, gdp_growth, marker='o', linewidth=2, color='#1976D2')
    ax.set_title(display_arabic_text('معدل نمو الناتج المحلي الإجمالي في الجزائر (2010-2023)'), fontsize=16)
    ax.set_xlabel(display_arabic_text('السنة'), fontsize=12)
    ax.set_ylabel(display_arabic_text('معدل النمو (%)'), fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.axhline(y=0, color='red', linestyle='-', alpha=0.3)

    for i, txt in enumerate(gdp_growth):
        ax.annotate(f"{txt}%", (years[i], gdp_growth[i]), textcoords="offset points",
                    xytext=(0, 10), ha='center', fontsize=9)

    st.pyplot(fig)

    # مثال بيانات مقطعية
    wilayas = ['الجزائر', 'وهران', 'قسنطينة', 'عنابة', 'سطيف', 'بجاية', 'تلمسان', 'ورقلة']
    unemployment = np.array([9.8, 11.2, 12.5, 10.3, 13.5, 14.2, 11.8, 8.7])

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(wilayas, unemployment, color='#2196F3')
    ax.set_title(display_arabic_text('معدل البطالة حسب الولايات (2023)'), fontsize=16)
    ax.set_xlabel(display_arabic_text('الولاية'), fontsize=12)
    ax.set_ylabel(display_arabic_text('معدل البطالة (%)'), fontsize=12)
    ax.set_ylim(0, 20)

    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height}%',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=10)

    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.markdown('<div class="tip-box content-text">', unsafe_allow_html=True)
    st.markdown("""
    ### نصائح للتعامل مع البيانات:

    1. **تحقق من مصدر البيانات**: استخدم مصادر موثوقة ورسمية
    2. **انتبه للبيانات المفقودة**: كيفاش تتعامل مع القيم الناقصة؟
    3. **الانتباه للقيم الشاذة**: شوف واش كاين قيم بعيدة بزاف على المتوسط
    4. **معالجة البيانات قبل التحليل**: تنظيف البيانات من الأخطاء والتحقق من دقتها
    5. **توثيق مصادر البيانات**: سجل من وين جبت البيانات وكيفاش عالجتها
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# تحليل البيانات الوصفي
elif section == "تحليل البيانات الوصفي":
    st.markdown('<h2 class="section-title">تحليل البيانات الوصفي</h2>', unsafe_allow_html=True)

    st.markdown('<div class="content-text">', unsafe_allow_html=True)
    st.markdown("""
    ### تحليل البيانات الوصفي - المفهوم والأهمية

    التحليل الوصفي هو الخطوة الأولى في تحليل البيانات، ويساعدنا نفهمو خصائص البيانات قبل ما نبداو في بناء النماذج.

    ### مقاييس النزعة المركزية:

    1. **المتوسط (Mean)**: مجموع القيم مقسوم على عددها
    2. **الوسيط (Median)**: القيمة اللي في وسط البيانات بعد ترتيبها
    3. **المنوال (Mode)**: القيمة الأكثر تكرارًا في البيانات

    ### مقاييس التشتت:

    1. **المدى (Range)**: الفرق بين أكبر وأصغر قيمة
    2. **الانحراف المعياري (Standard Deviation)**: يقيس تشتت القيم عن المتوسط
    3. **التباين (Variance)**: مربع الانحراف المعياري
    4. **الربيعيات (Quartiles)**: تقسم البيانات إلى أربعة أقسام متساوية
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    # عرض بيانات عشوائية
    st.markdown('<h3 class="subsection-title">لنشوفو مثال على البيانات:</h3>', unsafe_allow_html=True)
    st.write(data.head())

    # الإحصاءات الوصفية
    st.markdown('<h3 class="subsection-title">الإحصاءات الوصفية للبيانات:</h3>', unsafe_allow_html=True)
    st.write(data.describe())

    # رسم توزيعات البيانات
    st.markdown('<h3 class="subsection-title">توزيع المتغيرات:</h3>', unsafe_allow_html=True)

    # هيستوجرام للمتغيرات
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle(display_arabic_text('توزيع المتغيرات الاقتصادية'), fontsize=16)

    axes[0, 0].hist(data['الدخل'], bins=15, color='#1976D2', alpha=0.7)
    axes[0, 0].set_title(display_arabic_text('توزيع الدخل'), fontsize=12)

    axes[0, 1].hist(data['الاستهلاك'], bins=15, color='#2E7D32', alpha=0.7)
    axes[0, 1].set_title(display_arabic_text('توزيع الاستهلاك'), fontsize=12)

    axes[1, 0].hist(data['الاستثمار'], bins=15, color='#C62828', alpha=0.7)
    axes[1, 0].set_title(display_arabic_text('توزيع الاستثمار'), fontsize=12)

    axes[1, 1].hist(data['الإنفاق الحكومي'], bins=15, color='#7B1FA2', alpha=0.7)
    axes[1, 1].set_title(display_arabic_text('توزيع الإنفاق الحكومي'), fontsize=12)

    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    st.pyplot(fig)

    # رسم العلاقة بين متغيرين
    st.markdown('<h3 class="subsection-title">العلاقة بين المتغيرات:</h3>', unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(data['الدخل'], data['الاستهلاك'], alpha=0.7, color='#1976D2')
    ax.set_title(display_arabic_text('العلاقة بين الدخل والاستهلاك'), fontsize=16)
    ax.set_xlabel(display_arabic_text('الدخل (دج)'), fontsize=12)
    ax.set_ylabel(display_arabic_text('الاستهلاك (دج)'), fontsize=12)

    # إضافة خط الانحدار
    z = np.polyfit(data['الدخل'], data['الاستهلاك'], 1)
    p = np.poly1d(z)
    ax.plot(data['الدخل'], p(data['الدخل']), "r--", alpha=0.8)

    st.pyplot(fig)

    # مصفوفة الارتباط
    st.markdown('<h3 class="subsection-title">مصفوفة الارتباط:</h3>', unsafe_allow_html=True)

    corr = data.corr()
    st.write(corr)

    # رسم مصفوفة الارتباط
    fig, ax = plt.subplots(figsize=(10, 8))
    mask = np.triu(np.ones_like(corr, dtype=bool))
    cmap = sns.diverging_palette(220, 10, as_cmap=True)

    sns.heatmap(corr, mask=mask, cmap=cmap, vmax=1, vmin=-1, center=0,
                annot=True, fmt=".2f", square=True, linewidths=.5)

    ax.set_title(display_arabic_text('مصفوفة الارتباط'), fontsize=16)
    st.pyplot(fig)

    st.markdown('<div class="tip-box content-text">', unsafe_allow_html=True)
    st.markdown("""
    ### نصائح لتحليل البيانات الوصفي:

    1. **دائما ابدأ بالتحليل الوصفي**: يعطيك فكرة أولية عن البيانات
    2. **انتبه للقيم الشاذة**: حاول تفهم سببها واش تحذفها ولا تعالجها
    3. **تفحص التوزيع**: شوف واش البيانات تتبع التوزيع الطبيعي ولا لا
    4. **ادرس العلاقات**: شوف قوة واتجاه العلاقة بين المتغيرات من خلال معاملات الارتباط
    5. **استخدم الرسوم البيانية**: الصورة تغنيك عن ألف كلمة
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# نموذج الانحدار الخطي البسيط
elif section == "نموذج الانحدار الخطي البسيط":
    st.markdown('<h2 class="section-title">نموذج الانحدار الخطي البسيط</h2>', unsafe_allow_html=True)

    st.markdown('<div class="content-text">', unsafe_allow_html=True)
    st.markdown("""
    ### واش هو نموذج الانحدار الخطي البسيط؟

    هو نموذج إحصائي يستخدم لدراسة العلاقة بين متغيرين: متغير مستقل (X) ومتغير تابع (Y).

    ### المعادلة العامة للنموذج:

    Y = β₀ + β₁X + ε

    حيث:
    - Y: المتغير التابع (المتغير اللي حابين نتنبأو به)
    - X: المتغير المستقل (المتغير المفسر)
    - β₀: الثابت (قيمة Y لما X تساوي صفر)
    - β₁: معامل الانحدار (مقدار تغير Y عندما تتغير X بوحدة واحدة)
    - ε: الخطأ العشوائي (الفرق بين القيم الحقيقية والقيم المتوقعة)

    ### كيفاش نقدرو معلمات النموذج؟

    نستخدم طريقة المربعات الصغرى العادية (OLS) اللي تختار قيم β₀ و β₁ بحيث تقلل مجموع مربعات الأخطاء.

    ### كيفاش نفسرو النتائج؟

    1. **معامل الانحدار (β₁)**:
       - إذا كان موجب: العلاقة طردية بين X و Y
       - إذا كان سالب: العلاقة عكسية بين X و Y
       - القيمة تعبر عن مقدار تغير Y لكل تغير وحدة واحدة في X

    2. **الثابت (β₀)**:
       - قيمة Y المتوقعة عندما X تساوي صفر (إذا كان له معنى اقتصادي)

    3. **معامل التحديد (R²)**:
       - يقيس نسبة التباين في Y اللي يفسرها النموذج
       - تتراوح قيمته بين 0 و 1، وكلما اقتربت من 1 كان النموذج أفضل
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    # مثال على الانحدار الخطي البسيط
    st.markdown('<h3 class="subsection-title">مثال على الانحدار الخطي البسيط:</h3>', unsafe_allow_html=True)

    st.markdown('<div class="content-text">', unsafe_allow_html=True)
    st.markdown("""
    لنفترض أننا ندرس العلاقة بين الدخل والاستهلاك في الجزائر. وفقًا للنظرية الاقتصادية، كلما زاد الدخل يزيد الاستهلاك.

    نموذج الانحدار هنا يكون:

    الاستهلاك = β₀ + β₁ * الدخل + ε
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    # تقدير النموذج
    X = data['الدخل'].values.reshape(-1, 1)
    y = data['الاستهلاك'].values

    model = LinearRegression()
    model.fit(X, y)

    # معلمات النموذج
    slope = model.coef_[0]
    intercept = model.intercept_

    # التنبؤات
    predictions = model.predict(X)

    # حساب R²
    r2 = r2_score(y, predictions)

    # عرض نتائج النموذج
    st.markdown('<h3 class="subsection-title">نتائج نموذج الانحدار:</h3>', unsafe_allow_html=True)

    st.markdown(f"""
    - معادلة الانحدار المقدرة: الاستهلاك = {intercept:.2f} + {slope:.2f} × الدخل
    - معامل الانحدار (β₁): {slope:.4f}
    - الثابت (β₀): {intercept:.4f}
    - معامل التحديد (R²): {r2:.4f}
    """)

    # رسم العلاقة والنموذج المقدر
    fig, ax = plt.subplots(figsize=(10, 6))

    # رسم نقاط البيانات
    ax.scatter(X, y, color='#1976D2', alpha=0.6, label=display_arabic_text('البيانات الفعلية'))

    # رسم خط الانحدار
    ax.plot(X, predictions, color='red', linewidth=2, label=display_arabic_text('خط الانحدار المقدر'))

    # إضافة معلومات النموذج على الرسم
    equation_text = f"الاستهلاك = {intercept:.2f} + {slope:.2f} × الدخل"
    r2_text = f"R² = {r2:.4f}"

    # وضع المعادلة على الرسم
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.05, 0.95, display_arabic_text(equation_text), transform=ax.transAxes, fontsize=12,
            verticalalignment='top', bbox=props)
    ax.text(0.05, 0.87, display_arabic_text(r2_text), transform=ax.transAxes, fontsize=12,
            verticalalignment='top', bbox=props)

    ax.set_title(display_arabic_text('نموذج الانحدار الخطي البسيط: العلاقة بين الدخل والاستهلاك'), fontsize=16)
    ax.set_xlabel(display_arabic_text('الدخل (دج)'), fontsize=12)
    ax.set_ylabel(display_arabic_text('الاستهلاك (دج)'), fontsize=12)
    ax.legend(loc='lower right')
    ax.grid(True, linestyle='--', alpha=0.7)

    st.pyplot(fig)

    # اختبار معنوية النموذج
    st.markdown('<h3 class="subsection-title">اختبار معنوية النموذج:</h3>', unsafe_allow_html=True)

    # إضافة عمود ثابت للمتغير المستقل
    X_sm = sm.add_constant(X)

    # تقدير النموذج باستخدام statsmodels
    model_sm = sm.OLS(y, X_sm).fit()

    # عرض ملخص النموذج
    st.text(model_sm.summary().as_text())

    st.markdown('<div class="content-text">', unsafe_allow_html=True)
    st.markdown("""
    ### كيفاش نفسرو ملخص النموذج؟

    1. **مستوى المعنوية (p-value)**: 
       - إذا كانت قيمة p-value أقل من 0.05، فهذا يعني أن المعلمة معنوية إحصائيًا
       - في هذا المثال، معامل الانحدار معنوي مما يؤكد وجود علاقة بين الدخل والاستهلاك

    2. **R-squared**: 
       - يبين أن الدخل يفسر نسبة كبيرة من التغيرات في الاستهلاك

    3. **F-statistic**: 
       - اختبار لمعنوية النموذج ككل، وفي هذه الحالة النموذج معنوي
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="tip-box content-text">', unsafe_allow_html=True)
    st.markdown("""
    ### نصائح ومحاذير:

    1. **الارتباط مش سببية**: وجود علاقة ارتباط قوية بين متغيرين ما يعنيش بالضرورة وجود علاقة سببية

    2. **حدود التنبؤ**: احذر من التنبؤ خارج نطاق البيانات المستخدمة في تقدير النموذج

    3. **افحص الافتراضات**: نموذج الانحدار الخطي يستند على افتراضات معينة:
       - خطية العلاقة
       - استقلالية الأخطاء
       - ثبات تباين الأخطاء (التجانس)
       - التوزيع الطبيعي للأخطاء

    4. **ربط النتائج بالنظرية**: دائمًا حاول تفسير النتائج في ضوء النظرية الاقتصادية
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# نموذج الانحدار المتعدد
elif section == "نموذج الانحدار المتعدد":
    st.markdown('<h2 class="section-title">نموذج الانحدار الخطي المتعدد</h2>', unsafe_allow_html=True)

    st.markdown('<div class="content-text">', unsafe_allow_html=True)
    st.markdown("""
    ### واش هو نموذج الانحدار المتعدد؟

    هو امتداد لنموذج الانحدار البسيط، بحيث نستخدمو أكثر من متغير مستقل لتفسير المتغير التابع.

    ### المعادلة العامة للنموذج:

    Y = β₀ + β₁X₁ + β₂X₂ + ... + βₙXₙ + ε

    حيث:
    - Y: المتغير التابع
    - X₁, X₂, ..., Xₙ: المتغيرات المستقلة
    - β₀: الثابت
    - β₁, β₂, ..., βₙ: معاملات الانحدار للمتغيرات المستقلة
    - ε: الخطأ العشوائي

    ### ليش نستخدمو الانحدار المتعدد؟

    1. **تحسين القدرة التفسيرية**: إضافة متغيرات مستقلة مناسبة تزيد من قدرة النموذج على تفسير التغيرات في المتغير التابع

    2. **تقليل تحيز المعلمات**: في حالة وجود ارتباط بين المتغيرات، استخدام نموذج بسيط قد يؤدي إلى تحيز في تقدير المعلمات

    3. **فهم أفضل للظاهرة**: معظم الظواهر الاقتصادية متعددة الأبعاد وتتأثر بعدة عوامل
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    # مثال على الانحدار المتعدد
    st.markdown('<h3 class="subsection-title">مثال على الانحدار المتعدد:</h3>', unsafe_allow_html=True)

    st.markdown('<div class="content-text">', unsafe_allow_html=True)
    st.markdown("""
    لندرس العوامل المؤثرة في الاستهلاك. وفقًا للنظرية الاقتصادية، الاستهلاك يتأثر بالدخل وكذلك بعوامل أخرى مثل الاستثمار والإنفاق الحكومي.

    نموذج الانحدار المتعدد هنا يكون:

    الاستهلاك = β₀ + β₁ × الدخل + β₂ × الاستثمار + β₃ × الإنفاق الحكومي + ε
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    # تقدير النموذج المتعدد
    X_multi = data[['الدخل', 'الاستثمار', 'الإنفاق الحكومي']]
    y = data['الاستهلاك']

    # تقسيم البيانات
    X_train, X_test, y_train, y_test = train_test_split(X_multi, y, test_size=0.2, random_state=42)

    # بناء النموذج
    model_multi = LinearRegression()
    model_multi.fit(X_train, y_train)

    # معلمات النموذج
    coefficients = model_multi.coef_
    intercept = model_multi.intercept_

    # التنبؤات
    y_pred_train = model_multi.predict(X_train)
    y_pred_test = model_multi.predict(X_test)

    # حساب R²
    r2_train = r2_score(y_train, y_pred_train)
    r2_test = r2_score(y_test, y_pred_test)

    # عرض نتائج النموذج
    st.markdown('<h3 class="subsection-title">نتائج نموذج الانحدار المتعدد:</h3>', unsafe_allow_html=True)

    st.markdown(f"""
    معادلة الانحدار المقدرة:

    الاستهلاك = {intercept:.2f} + {coefficients[0]:.2f} × الدخل + {coefficients[1]:.2f} × الاستثمار + {coefficients[2]:.2f} × الإنفاق الحكومي

    - معامل الدخل: {coefficients[0]:.4f}
    - معامل الاستثمار: {coefficients[1]:.4f}
    - معامل الإنفاق الحكومي: {coefficients[2]:.4f}
    - الثابت: {intercept:.4f}
    - معامل التحديد (R²) للبيانات التدريبية: {r2_train:.4f}
    - معامل التحديد (R²) للبيانات الاختبارية: {r2_test:.4f}
    """)

    # اختبار معنوية النموذج
    st.markdown('<h3 class="subsection-title">اختبار معنوية النموذج:</h3>', unsafe_allow_html=True)

    # إضافة عمود ثابت
    X_multi_sm = sm.add_constant(X_multi)

    # تقدير النموذج باستخدام statsmodels
    model_multi_sm = sm.OLS(y, X_multi_sm).fit()

    # عرض ملخص النموذج
    st.text(model_multi_sm.summary().as_text())

    # مقارنة القيم الفعلية بالمتوقعة
    st.markdown('<h3 class="subsection-title">مقارنة القيم الفعلية بالمتوقعة:</h3>', unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=(10, 6))

    # رسم الخط المرجعي
    ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)

    # رسم القيم المتوقعة مقابل الفعلية
    ax.scatter(y_test, y_pred_test, alpha=0.7, color='#1976D2')

    ax.set_title(display_arabic_text('مقارنة القيم الفعلية والمتوقعة للاستهلاك'), fontsize=16)
    ax.set_xlabel(display_arabic_text('القيم الفعلية'), fontsize=12)
    ax.set_ylabel(display_arabic_text('القيم المتوقعة'), fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)

    # إضافة معلومات عن دقة النموذج
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.05, 0.95, f"R² = {r2_test:.4f}", transform=ax.transAxes, fontsize=12,
            verticalalignment='top', bbox=props)

    st.pyplot(fig)

    # الأهمية النسبية للمتغيرات
    st.markdown('<h3 class="subsection-title">الأهمية النسبية للمتغيرات المستقلة:</h3>', unsafe_allow_html=True)

    # حساب المعاملات المعيارية
    from sklearn.preprocessing import StandardScaler

    scaler_X = StandardScaler()
    scaler_y = StandardScaler()

    X_scaled = scaler_X.fit_transform(X_multi)
    y_scaled = scaler_y.fit_transform(y.values.reshape(-1, 1)).ravel()

    model_scaled = LinearRegression()
    model_scaled.fit(X_scaled, y_scaled)

    # المعاملات المعيارية
    std_coefficients = model_scaled.coef_

    # رسم بياني للأهمية النسبية
    fig, ax = plt.subplots(figsize=(10, 6))

    features = ['الدخل', 'الاستثمار', 'الإنفاق الحكومي']
    colors = ['#1976D2', '#2E7D32', '#C62828']

    bars = ax.bar(features, np.abs(std_coefficients), color=colors, alpha=0.7)

    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.4f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=10)

    ax.set_title(display_arabic_text('الأهمية النسبية للمتغيرات المستقلة'), fontsize=16)
    ax.set_ylabel(display_arabic_text('المعامل المعياري المطلق'), fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    st.pyplot(fig)

    st.markdown('<div class="tip-box content-text">', unsafe_allow_html=True)
    st.markdown("""
    ### مشاكل شائعة في نماذج الانحدار المتعدد:

    1. **الازدواج الخطي (Multicollinearity)**:
       - يحدث عندما تكون المتغيرات المستقلة مرتبطة فيما بينها
       - يؤدي إلى عدم استقرار المعلمات وصعوبة تفسيرها
       - الحل: حذف المتغيرات المرتبطة أو استخدام تقنيات مثل تحليل المكونات الرئيسية

    2. **انتقاء المتغيرات**:
       - إضافة متغيرات غير مهمة تؤدي إلى تعقيد النموذج دون تحسين أدائه
       - الحل: استخدام تقنيات انتقاء المتغيرات مثل Stepwise Regression أو LASSO

    3. **الافراط في التخصيص (Overfitting)**:
       - النموذج يتعلم ضوضاء البيانات بدل العلاقات الحقيقية
       - الحل: تقسيم البيانات والتحقق من أداء النموذج على بيانات الاختبار

    4. **عدم خطية العلاقة**:
       - الحل: استخدام تحويلات للمتغيرات أو نماذج غير خطية
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# مشاكل الانحدار وحلولها
elif section == "مشاكل الانحدار وحلولها":
    st.markdown('<h2 class="section-title">مشاكل الانحدار وحلولها</h2>', unsafe_allow_html=True)

    st.markdown('<div class="content-text">', unsafe_allow_html=True)
    st.markdown("""
    ### المشاكل الشائعة في نماذج الانحدار والحلول المناسبة لها:

    #### 1. عدم تجانس التباين (Heteroscedasticity)

    **المشكلة**: تباين حدود الخطأ غير ثابت عبر المشاهدات

    **الكشف عنها**:
    - اختبار White أو Breusch-Pagan
    - فحص رسم البواقي مقابل القيم المتوقعة

    **الحلول**:
    - استخدام الأخطاء المعيارية القوية (Robust Standard Errors)
    - تحويل المتغير التابع (مثل اللوغاريتم)
    - استخدام نموذج الانحدار الموزون (WLS)

    #### 2. الارتباط الذاتي (Autocorrelation)

    **المشكلة**: حدود الخطأ غير مستقلة عن بعضها، خاصة في بيانات السلاسل الزمنية

    **الكشف عنها**:
    - اختبار Durbin-Watson
    - رسم البواقي مع الزمن

    **الحلول**:
    - تضمين متغيرات مبطأة (Lagged Variables)
    - استخدام نماذج ARIMA
    - تصحيح Cochrane-Orcutt

    #### 3. الازدواج الخطي (Multicollinearity)

    **المشكلة**: ارتباط قوي بين المتغيرات المستقلة

    **الكشف عنها**:
    - عامل تضخم التباين (VIF)
    - مصفوفة الارتباط بين المتغيرات المستقلة

    **الحلول**:
    - حذف بعض المتغيرات المرتبطة
    - استخدام تحليل المكونات الرئيسية (PCA)
    - تطبيق Ridge Regression أو LASSO

    #### 4. سوء تعيين النموذج (Model Misspecification)

    **المشكلة**: تعيين خاطئ لشكل العلاقة بين المتغيرات

    **الكشف عنها**:
    - اختبار Ramsey RESET
    - تحليل البواقي

    **الحلول**:
    - إضافة متغيرات جديدة
    - إدخال تحويلات غير خطية
    - استخدام نماذج أكثر مرونة
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    # تطبيق عملي: عدم تجانس التباين
    st.markdown('<h3 class="subsection-title">تطبيق عملي: الكشف عن عدم تجانس التباين</h3>', unsafe_allow_html=True)

    # إنشاء بيانات تعاني من عدم تجانس التباين
    np.random.seed(123)
    n = 100
    X_hetero = np.linspace(1, 10, n)
    noise = np.random.normal(0, X_hetero, n)  # الخطأ يزداد مع زيادة X
    y_hetero = 2 + 3 * X_hetero + noise

    df_hetero = pd.DataFrame({
        'X': X_hetero,
        'y': y_hetero
    })

    # تقدير النموذج
    X_h = df_hetero['X'].values.reshape(-1, 1)
    y_h = df_hetero['y'].values

    model_hetero = LinearRegression()
    model_hetero.fit(X_h, y_h)

    # التنبؤات والبواقي
    predictions_h = model_hetero.predict(X_h)
    residuals_h = y_h - predictions_h

    # رسم العلاقة والبواقي
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # رسم نقاط البيانات والنموذج المقدر
    axes[0].scatter(X_h, y_h, alpha=0.6, color='#1976D2', label=display_arabic_text('البيانات الفعلية'))
    axes[0].plot(X_h, predictions_h, color='red', linewidth=2, label=display_arabic_text('خط الانحدار المقدر'))
    axes[0].set_title(display_arabic_text('بيانات تعاني من عدم تجانس التباين'), fontsize=14)
    axes[0].set_xlabel('X', fontsize=12)
    axes[0].set_ylabel('Y', fontsize=12)
    axes[0].legend()
    axes[0].grid(True, linestyle='--', alpha=0.7)

    # رسم البواقي مقابل القيم المتوقعة
    axes[1].scatter(predictions_h, residuals_h, alpha=0.6, color='#1976D2')
    axes[1].axhline(y=0, color='red', linestyle='-', alpha=0.3)
    axes[1].set_title(display_arabic_text('البواقي مقابل القيم المتوقعة'), fontsize=14)
    axes[1].set_xlabel(display_arabic_text('القيم المتوقعة'), fontsize=12)
    axes[1].set_ylabel(display_arabic_text('البواقي'), fontsize=12)
    axes[1].grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    st.pyplot(fig)

    st.markdown('<div class="content-text">', unsafe_allow_html=True)
    st.markdown("""
    في الرسم البياني للبواقي مقابل القيم المتوقعة، نلاحظ أن البواقي تتشتت بشكل أكبر كلما زادت القيمة المتوقعة، مما يشير إلى وجود مشكلة عدم تجانس التباين.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    # الحل: تطبيق تحويل لوغاريتمي
    st.markdown('<h3 class="subsection-title">الحل: تطبيق التحويل اللوغاريتمي</h3>', unsafe_allow_html=True)

    # تطبيق التحويل اللوغاريتمي
    df_log = pd.DataFrame({
        'X': df_hetero['X'],
        'log_X': np.log(df_hetero['X']),
        'log_y': np.log(df_hetero['y'])
    })

    # تقدير النموذج بعد التحويل
    X_log = df_log['log_X'].values.reshape(-1, 1)
    y_log = df_log['log_y'].values

    model_log = LinearRegression()
    model_log.fit(X_log, y_log)

    # التنبؤات والبواقي بعد التحويل
    predictions_log = model_log.predict(X_log)
    residuals_log = y_log - predictions_log

    # رسم النتائج بعد التحويل
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # رسم العلاقة بعد التحويل
    axes[0].scatter(X_log, y_log, alpha=0.6, color='#1976D2', label=display_arabic_text('البيانات بعد التحويل'))
    axes[0].plot(X_log, predictions_log, color='red', linewidth=2, label=display_arabic_text('خط الانحدار المقدر'))
    axes[0].set_title(display_arabic_text('العلاقة بعد التحويل اللوغاريتمي'), fontsize=14)
    axes[0].set_xlabel(display_arabic_text('لوغاريتم X'), fontsize=12)
    axes[0].set_ylabel(display_arabic_text('لوغاريتم Y'), fontsize=12)
    axes[0].legend()
    axes[0].grid(True, linestyle='--', alpha=0.7)

    # رسم البواقي بعد التحويل
    axes[1].scatter(predictions_log, residuals_log, alpha=0.6, color='#1976D2')
    axes[1].axhline(y=0, color='red', linestyle='-', alpha=0.3)
    axes[1].set_title(display_arabic_text('البواقي بعد التحويل اللوغاريتمي'), fontsize=14)
    axes[1].set_xlabel(display_arabic_text('القيم المتوقعة'), fontsize=12)
    axes[1].set_ylabel(display_arabic_text('البواقي'), fontsize=12)
    axes[1].grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    st.pyplot(fig)

    st.markdown('<div class="content-text">', unsafe_allow_html=True)
    st.markdown("""
    بعد تطبيق التحويل اللوغاريتمي، نلاحظ أن البواقي أصبحت أكثر تجانسًا وتتوزع بشكل عشوائي حول الصفر، مما يشير إلى تحسن في مشكلة عدم تجانس التباين.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    # مشكلة الازدواج الخطي
    st.markdown('<h3 class="subsection-title">الكشف عن الازدواج الخطي</h3>', unsafe_allow_html=True)

    # إنشاء بيانات بها ازدواج خطي
    np.random.seed(123)
    X1_multi = np.random.normal(size=100)
    X2_multi = 0.8 * X1_multi + 0.2 * np.random.normal(size=100)  # مرتبط بشدة مع X1
    X3_multi = np.random.normal(size=100)

    y_multi = 2 + 3 * X1_multi + 4 * X2_multi + 1.5 * X3_multi + np.random.normal(size=100)

    df_multi = pd.DataFrame({
        'X1': X1_multi,
        'X2': X2_multi,
        'X3': X3_multi,
        'y': y_multi
    })

    # حساب مصفوفة الارتباط
    corr_matrix = df_multi[['X1', 'X2', 'X3']].corr()

    # عرض مصفوفة الارتباط
    st.write(display_arabic_text("مصفوفة الارتباط بين المتغيرات المستقلة:"))
    st.write(corr_matrix)

    # رسم مصفوفة الارتباط
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    ax.set_title(display_arabic_text('مصفوفة الارتباط بين المتغيرات المستقلة'), fontsize=14)
    st.pyplot(fig)

    # حساب VIF
    from statsmodels.stats.outliers_influence import variance_inflation_factor

    X_vif = df_multi[['X1', 'X2', 'X3']]
    vif_data = pd.DataFrame()
    vif_data["متغير"] = X_vif.columns
    vif_data["VIF"] = [variance_inflation_factor(X_vif.values, i) for i in range(X_vif.shape[1])]

    st.write(display_arabic_text("عامل تضخم التباين (VIF):"))
    st.write(vif_data)

    st.markdown('<div class="content-text">', unsafe_allow_html=True)
    st.markdown("""
    نلاحظ أن قيمة الارتباط بين X1 و X2 مرتفعة (حوالي 0.8)، كما أن قيمة VIF للمتغيرين X1 و X2 أكبر من 5، مما يشير إلى وجود مشكلة الازدواج الخطي.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="tip-box content-text">', unsafe_allow_html=True)
    st.markdown("""
    ### نصائح للتعامل مع مشاكل الانحدار:

    1. **دائمًا افحص افتراضات النموذج**: قبل ما تعتمد على نتائج النموذج، تأكد من أن الافتراضات الأساسية محققة

    2. **استخدم الاختبارات الإحصائية**: هناك اختبارات خاصة للكشف عن كل مشكلة، استخدمها للتحقق

    3. **الرسوم البيانية مهمة**: الفحص البصري للبواقي والعلاقات يمكن أن يكشف مشاكل غير ظاهرة في الإحصاءات

    4. **جرب عدة تحويلات**: في حالة المشاكل، جرب تحويلات مختلفة (لوغاريتم، جذر تربيعي، إلخ)

    5. **استشر النظرية الاقتصادية**: الحلول الفنية مهمة، لكن دائمًا راجع النظرية الاقتصادية لتأكيد معنى النتائج

    6. **تذكر أن النموذج تبسيط للواقع**: كل نموذج فيه قصور، المهم هو فهم حدود النموذج وتفسير النتائج بحذر
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# اختبار الفرضيات
elif section == "اختبار الفرضيات":
    st.markdown('<h2 class="section-title">اختبار الفرضيات في القياس الاقتصادي</h2>', unsafe_allow_html=True)

    st.markdown('<div class="content-text">', unsafe_allow_html=True)
    st.markdown("""
    ### واش معنى اختبار الفرضيات؟

    اختبار الفرضيات هو أسلوب إحصائي يستخدم للتحقق من صحة فرضية معينة حول معلمات المجتمع باستخدام بيانات العينة.

    ### خطوات اختبار الفرضيات:

    1. **تحديد الفرضيات**:
       - الفرضية الصفرية (H₀): عادة تفترض عدم وجود تأثير أو علاقة
       - الفرضية البديلة (H₁): تمثل البديل للفرضية الصفرية

    2. **اختيار مستوى المعنوية (α)**:
       - عادة يكون 0.05 (5%) أو 0.01 (1%)

    3. **حساب إحصائية الاختبار**:
       - مثل t، F، Chi-square

    4. **حساب القيمة الاحتمالية (p-value)**

    5. **اتخاذ القرار**:
       - إذا كانت p-value < α، نرفض الفرضية الصفرية
       - إذا كانت p-value > α، لا نستطيع رفض الفرضية الصفرية

    ### أنواع الاختبارات الشائعة في القياس الاقتصادي:

    1. **اختبار t للمعلمات الفردية**:
       - يستخدم لاختبار معنوية معلمة واحدة (مثل β₁)
       - H₀: β₁ = 0 (المتغير ليس له تأثير معنوي)
       - H₁: β₁ ≠ 0 (المتغير له تأثير معنوي)

    2. **اختبار F للنموذج ككل**:
       - يختبر المعنوية الإجمالية للنموذج
       - H₀: β₁ = β₂ = ... = βₙ = 0 (النموذج غير معنوي)
       - H₁: على الأقل واحدة من المعلمات تختلف عن الصفر

    3. **اختبار القيود (Restriction tests)**:
       - لاختبار قيود محددة على المعلمات
       - مثل: H₀: β₁ = β₂
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    # تطبيق عملي: اختبار معنوية معلمات النموذج
    st.markdown('<h3 class="subsection-title">تطبيق عملي: اختبار معنوية معلمات النموذج</h3>', unsafe_allow_html=True)

    # نبني نموذج انحدار متعدد
    X = data[['الدخل', 'الاستثمار', 'الإنفاق الحكومي']]
    y = data['الاستهلاك']

    # إضافة ثابت
    X_sm = sm.add_constant(X)

    # تقدير النموذج
    model = sm.OLS(y, X_sm).fit()

    # عرض نتائج النموذج
    st.text(model.summary().as_text())

    st.markdown('<div class="content-text">', unsafe_allow_html=True)
    st.markdown("""
    ### تفسير نتائج اختبار t:

    لكل معلمة في الجدول أعلاه، لدينا:

    - **Coefficient**: قيمة المعلمة المقدرة
    - **Std Error**: الخطأ المعياري للمعلمة
    - **t-statistic**: إحصائية t محسوبة كـ (Coefficient / Std Error)
    - **P>|t|**: القيمة الاحتمالية (p-value)

    لاختبار معنوية كل معلمة، نقارن p-value مع مستوى المعنوية α (عادة 0.05):

    - إذا كانت p-value < 0.05: المعلمة معنوية إحصائيًا (نرفض الفرضية الصفرية)
    - إذا كانت p-value > 0.05: المعلمة غير معنوية إحصائيًا (لا نستطيع رفض الفرضية الصفرية)

    ### تفسير نتائج اختبار F:

    في أسفل الجدول، نجد:

    - **F-statistic**: قيمة إحصائية F للنموذج ككل
    - **Prob (F-statistic)**: القيمة الاحتمالية لاختبار F

    إذا كانت Prob (F-statistic) < 0.05، فهذا يعني أن النموذج ككل معنوي إحصائيًا.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    # اختبار قيد على المعلمات
    st.markdown('<h3 class="subsection-title">اختبار قيد على المعلمات</h3>', unsafe_allow_html=True)

    st.markdown('<div class="content-text">', unsafe_allow_html=True)
    st.markdown("""
    نفترض أننا نريد اختبار الفرضية التالية:

    H₀: معامل الدخل = معامل الاستثمار
    H₁: معامل الدخل ≠ معامل الاستثمار

    يمكننا استخدام اختبار Wald لهذا الغرض:
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    # تطبيق اختبار Wald
    from statsmodels.stats.sandwich_covariance import cov_hac

    # تعريف القيد: معامل الدخل - معامل الاستثمار = 0
    restriction = ['x1 = x2']

    # تطبيق الاختبار
    wald_test = model.wald_test(restriction)

    st.write(f"إحصائية F: {wald_test.fvalue[0][0]:.4f}")
    st.write(f"القيمة الاحتمالية (p-value): {wald_test.pvalue:.4f}")

    # تفسير النتيجة
    if wald_test.pvalue < 0.05:
        st.write("النتيجة: نرفض الفرضية الصفرية، أي أن معامل الدخل يختلف معنويًا عن معامل الاستثمار.")
    else:
        st.write(
            "النتيجة: لا نستطيع رفض الفرضية الصفرية، أي لا يوجد دليل كافي على أن معامل الدخل يختلف عن معامل الاستثمار.")

    # اختبار فترة الثقة للمعلمات
    st.markdown('<h3 class="subsection-title">فترات الثقة للمعلمات</h3>', unsafe_allow_html=True)

    # حساب فترات الثقة
    conf_int = model.conf_int(alpha=0.05)
    conf_int.columns = ['الحد الأدنى (95%)', 'الحد الأعلى (95%)']

    st.write("فترات الثقة للمعلمات عند مستوى ثقة 95%:")
    st.write(conf_int)

    # رسم فترات الثقة
    fig, ax = plt.subplots(figsize=(10, 6))

    coef_names = ['الثابت', 'الدخل', 'الاستثمار', 'الإنفاق الحكومي']
    coefs = model.params
    errors = model.bse

    y_pos = np.arange(len(coef_names))

    # رسم المعلمات
    ax.errorbar(coefs, y_pos, xerr=1.96 * errors, fmt='o', capsize=5, color='#1976D2',
                ecolor='#1976D2', markersize=8)

    ax.axvline(x=0, color='red', linestyle='--', alpha=0.7)
    ax.set_yticks(y_pos)
    ax.set_yticklabels([display_arabic_text(name) for name in coef_names])
    ax.set_xlabel(display_arabic_text('قيمة المعلمة'), fontsize=12)
    ax.set_title(display_arabic_text('المعلمات المقدرة وفترات الثقة 95%'), fontsize=16)
    ax.grid(axis='x', linestyle='--', alpha=0.7)

    plt.tight_layout()
    st.pyplot(fig)

    st.markdown('<div class="tip-box content-text">', unsafe_allow_html=True)
    st.markdown("""
    ### نصائح لاختبار الفرضيات:

    1. **اختر الفرضيات بناءً على النظرية الاقتصادية**: لازم تكون الفرضيات مبنية على أساس نظري مش عشوائية

    2. **انتبه لمشكلة الاختبارات المتعددة**: عند إجراء عدة اختبارات، زيد احتمال الوقوع في خطأ من النوع الأول

    3. **لا تخلط بين المعنوية الإحصائية والأهمية العملية**: معلمة قد تكون معنوية إحصائيًا لكن تأثيرها في الواقع صغير

    4. **تفسير النتائج في سياقها**: التفسير يعتمد على السياق الاقتصادي وليس فقط على النتائج الإحصائية

    5. **استخدم أخطاء معيارية قوية**: في حالة وجود مشاكل في النموذج، استخدم أخطاء معيارية قوية لتحسين الاستدلال
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# تقييم النماذج
elif section == "تقييم النماذج":
    st.markdown('<h2 class="section-title">تقييم النماذج والمفاضلة بينها</h2>', unsafe_allow_html=True)

    st.markdown('<div class="content-text">', unsafe_allow_html=True)
    st.markdown("""
    ### أهمية تقييم النماذج:

    تقييم النماذج ضروري للتأكد من أن النموذج يمثل البيانات بشكل جيد ويمكن استخدامه للتنبؤ بدقة مقبولة.

    ### معايير تقييم النماذج:

    #### 1. معايير الملاءمة (Goodness of fit):

    - **معامل التحديد (R²)**:
      - يقيس نسبة التباين في المتغير التابع المفسرة بواسطة النموذج
      - تتراوح قيمته بين 0 و 1، وكلما اقتربت من 1 كان النموذج أفضل

    - **معامل التحديد المعدل (Adjusted R²)**:
      - يعدل R² ليأخذ في الاعتبار عدد المتغيرات المستقلة
      - يستخدم للمقارنة بين نماذج بأعداد مختلفة من المتغيرات

    #### 2. معايير الخطأ:

    - **متوسط مربعات الخطأ (MSE)**:
      - متوسط مربعات الفروق بين القيم الحقيقية والمتوقعة
      - كلما قلت قيمته كان النموذج أفضل

    - **الجذر التربيعي لمتوسط مربعات الخطأ (RMSE)**:
      - الجذر التربيعي لـ MSE، ويكون بنفس وحدة قياس المتغير التابع

    - **متوسط القيمة المطلقة للخطأ (MAE)**:
      - متوسط القيم المطلقة للفروق بين القيم الحقيقية والمتوقعة

    #### 3. معايير المعلومات:

    - **معيار أكايكي (AIC)**:
      - يوازن بين جودة النموذج وتعقيده
      - كلما قلت قيمته كان النموذج أفضل

    - **معيار شوارتز البياني (BIC/SBC)**:
      - مشابه لـ AIC لكنه يفرض عقوبة أكبر على تعقيد النموذج
      - يفضل النماذج الأبسط أكثر من AIC

    #### 4. التحقق المتقاطع (Cross-Validation):

    - تقسيم البيانات إلى مجموعة تدريب ومجموعة اختبار
    - تقدير النموذج على بيانات التدريب واختباره على بيانات الاختبار
    - يساعد في تجنب مشكلة الافراط في التخصيص (Overfitting)
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    # تطبيق عملي: مقارنة نماذج مختلفة
    st.markdown('<h3 class="subsection-title">تطبيق عملي: مقارنة بين نماذج مختلفة</h3>', unsafe_allow_html=True)

    # إعداد البيانات
    X = data[['الدخل', 'الاستثمار', 'الإنفاق الحكومي']]
    y = data['الاستهلاك']

    # تقسيم البيانات
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # بناء النماذج المختلفة
    # نموذج 1: الدخل فقط
    X1_train = X_train[['الدخل']]
    X1_test = X_test[['الدخل']]
    model1 = LinearRegression()
    model1.fit(X1_train, y_train)
    y1_pred = model1.predict(X1_test)

    # نموذج 2: الدخل والاستثمار
    X2_train = X_train[['الدخل', 'الاستثمار']]
    X2_test = X_test[['الدخل', 'الاستثمار']]
    model2 = LinearRegression()
    model2.fit(X2_train, y_train)
    y2_pred = model2.predict(X2_test)

    # نموذج 3: كل المتغيرات
    X3_train = X_train
    X3_test = X_test
    model3 = LinearRegression()
    model3.fit(X3_train, y_train)
    y3_pred = model3.predict(X3_test)


    # حساب معايير التقييم
    def calculate_metrics(y_true, y_pred):
        mse = mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        mae = np.mean(np.abs(y_true - y_pred))
        r2 = r2_score(y_true, y_pred)
        return {
            'MSE': mse,
            'RMSE': rmse,
            'MAE': mae,
            'R²': r2
        }


    metrics1 = calculate_metrics(y_test, y1_pred)
    metrics2 = calculate_metrics(y_test, y2_pred)
    metrics3 = calculate_metrics(y_test, y3_pred)

    # عرض النتائج في جدول
    metrics_df = pd.DataFrame({
        'النموذج 1 (الدخل فقط)': metrics1,
        'النموذج 2 (الدخل والاستثمار)': metrics2,
        'النموذج 3 (كل المتغيرات)': metrics3
    }).T

    st.write(display_arabic_text("مقارنة معايير تقييم النماذج:"))
    st.write(metrics_df)

    # رسم بياني لمقارنة أداء النماذج
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle(display_arabic_text('مقارنة معايير تقييم النماذج المختلفة'), fontsize=16)

    metrics_names = ['MSE', 'RMSE', 'MAE', 'R²']
    models = ['النموذج 1', 'النموذج 2', 'النموذج 3']

    for i, metric in enumerate(metrics_names):
        row, col = i // 2, i % 2
        values = [metrics1[metric], metrics2[metric], metrics3[metric]]

        bars = axes[row, col].bar(models, values, color=['#1976D2', '#2E7D32', '#C62828'], alpha=0.7)

        axes[row, col].set_title(display_arabic_text(metric), fontsize=14)

        for bar in bars:
            height = bar.get_height()
            axes[row, col].annotate(f'{height:.2f}',
                                    xy=(bar.get_x() + bar.get_width() / 2, height),
                                    xytext=(0, 3),
                                    textcoords="offset points",
                                    ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    st.pyplot(fig)

    # رسم المقارنة بين القيم الفعلية والمتوقعة
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle(display_arabic_text('مقارنة بين القيم الفعلية والمتوقعة للنماذج'), fontsize=16)

    # نموذج 1
    axes[0].scatter(y_test, y1_pred, alpha=0.7, color='#1976D2')
    axes[0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
    axes[0].set_title(display_arabic_text('النموذج 1 (الدخل فقط)'), fontsize=14)
    axes[0].set_xlabel(display_arabic_text('القيم الفعلية'), fontsize=12)
    axes[0].set_ylabel(display_arabic_text('القيم المتوقعة'), fontsize=12)
    axes[0].grid(True, linestyle='--', alpha=0.7)

    # نموذج 2
    axes[1].scatter(y_test, y2_pred, alpha=0.7, color='#2E7D32')
    axes[1].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
    axes[1].set_title(display_arabic_text('النموذج 2 (الدخل والاستثمار)'), fontsize=14)
    axes[1].set_xlabel(display_arabic_text('القيم الفعلية'), fontsize=12)
    axes[1].set_ylabel(display_arabic_text('القيم المتوقعة'), fontsize=12)
    axes[1].grid(True, linestyle='--', alpha=0.7)

    # نموذج 3
    axes[2].scatter(y_test, y3_pred, alpha=0.7, color='#C62828')
    axes[2].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
    axes[2].set_title(display_arabic_text('النموذج 3 (كل المتغيرات)'), fontsize=14)
    axes[2].set_xlabel(display_arabic_text('القيم الفعلية'), fontsize=12)
    axes[2].set_ylabel(display_arabic_text('القيم المتوقعة'), fontsize=12)
    axes[2].grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    st.pyplot(fig)

    st.markdown('<div class="content-text">', unsafe_allow_html=True)
    st.markdown("""
    ### تحليل النتائج:

    من خلال مقارنة معايير التقييم للنماذج الثلاثة، نستنتج:

    1. **النموذج 3 (كل المتغيرات)** يقدم أفضل أداء من حيث:
       - أقل MSE، RMSE، MAE (أخطاء أقل)
       - أعلى R² (قدرة تفسيرية أعلى)

    2. **النموذج 2 (الدخل والاستثمار)** يأتي في المرتبة الثانية، مما يشير إلى أن إضافة متغير الاستثمار يحسن النموذج مقارنة بالاعتماد على الدخل فقط

    3. **النموذج 1 (الدخل فقط)** هو الأبسط، لكنه الأقل دقة

    ### الاختيار بين النماذج:

    اختيار النموذج المناسب يعتمد على:

    1. **دقة التنبؤ**: إذا كان الهدف الرئيسي هو التنبؤ بدقة عالية، فالنموذج 3 هو الأفضل

    2. **البساطة**: إذا كنت تبحث عن نموذج بسيط وسهل التفسير، فقد تفضل النموذج 2

    3. **سياق المشكلة**: في بعض الحالات، تكون البساطة أهم من الدقة القصوى
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="tip-box content-text">', unsafe_allow_html=True)
    st.markdown("""
    ### نصائح لتقييم واختيار النماذج:

    1. **تجنب الإفراط في التخصيص (Overfitting)**: نموذج معقد جدًا قد يؤدي أداءً جيدًا على بيانات التدريب لكنه ضعيف في التنبؤ ببيانات جديدة

    2. **استخدم التحقق المتقاطع**: خاصة مع البيانات المحدودة لتقييم أداء النموذج بشكل أفضل

    3. **وازن بين الدقة والتفسير**: نموذج بسيط قابل للتفسير أحيانًا أفضل من نموذج معقد غير مفهوم

    4. **راعي الهدف من النموذج**: إذا كان الهدف هو التنبؤ، ركز على معايير الخطأ. إذا كان الهدف هو التفسير، ركز على المعنوية الإحصائية والاقتصادية

    5. **اختبر أداء النموذج على بيانات خارج العينة**: هذا هو الاختبار الحقيقي لقوة النموذج
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# تطبيق عملي
elif section == "تطبيق عملي":
    st.markdown('<h2 class="section-title">تطبيق عملي على نموذج اقتصادي</h2>', unsafe_allow_html=True)

    st.markdown('<div class="content-text">', unsafe_allow_html=True)
    st.markdown("""
    ### نموذج دالة الاستهلاك الكينزية

    راح نطبق الآن ما تعلمناه في مثال عملي كامل لتقدير دالة الاستهلاك الكينزية.

    وفقًا للنظرية الكينزية، الاستهلاك يعتمد بشكل أساسي على الدخل المتاح. المعادلة العامة لدالة الاستهلاك هي:

    C = C₀ + cY

    حيث:
    - C: الاستهلاك
    - C₀: الاستهلاك التلقائي (الاستهلاك عندما يكون الدخل صفر)
    - c: الميل الحدي للاستهلاك (نسبة التغير في الاستهلاك إلى التغير في الدخل)
    - Y: الدخل المتاح

    راح ندرس هذه العلاقة ونشوف مدى صحتها وكيفاش نقدر نستخدمها للتنبؤ.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    # إنشاء بيانات افتراضية للاقتصاد الجزائري
    st.markdown('<h3 class="subsection-title">البيانات المستخدمة</h3>', unsafe_allow_html=True)

    # بيانات افتراضية للدخل والاستهلاك في الجزائر (2010-2023)
    years = np.arange(2010, 2024)

    # الدخل المتاح (بالمليار دينار)
    income = np.array([10500, 11200, 12100, 12800, 13500, 14000, 14300, 14700,
                       15200, 15600, 14800, 15500, 16300, 17100])

    # الاستهلاك (بالمليار دينار)
    consumption = np.array([8800, 9300, 9900, 10400, 10900, 11300, 11500, 11800,
                            12100, 12400, 12000, 12500, 13000, 13600])

    # إنشاء DataFrame
    consumption_data = pd.DataFrame({
        'السنة': years,
        'الدخل المتاح': income,
        'الاستهلاك': consumption
    })

    st.write(display_arabic_text("بيانات الدخل المتاح والاستهلاك في الجزائر (2010-2023):"))
    st.write(consumption_data)

    # رسم البيانات
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(years, income, 'o-', color='#1976D2', linewidth=2, label=display_arabic_text('الدخل المتاح'))
    ax.plot(years, consumption, 'o-', color='#C62828', linewidth=2, label=display_arabic_text('الاستهلاك'))

    ax.set_title(display_arabic_text('تطور الدخل المتاح والاستهلاك في الجزائر (2010-2023)'), fontsize=16)
    ax.set_xlabel(display_arabic_text('السنة'), fontsize=12)
    ax.set_ylabel(display_arabic_text('القيمة (مليار دينار)'), fontsize=12)
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.7)

    # تعيين المحور السيني ليظهر كل السنوات
    ax.set_xticks(years)
    ax.set_xticklabels(years, rotation=45)

    st.pyplot(fig)

    # تحليل وصفي للبيانات
    st.markdown('<h3 class="subsection-title">التحليل الوصفي للبيانات</h3>', unsafe_allow_html=True)

    st.write(display_arabic_text("الإحصاءات الوصفية:"))
    st.write(consumption_data.describe())

    # رسم العلاقة بين الدخل والاستهلاك
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.scatter(income, consumption, color='#1976D2', s=80, alpha=0.7)

    # إضافة تسميات النقاط (السنوات)
    for i, year in enumerate(years):
        ax.annotate(str(year), (income[i], consumption[i]),
                    xytext=(5, 5), textcoords='offset points', fontsize=9)

    ax.set_title(display_arabic_text('العلاقة بين الدخل المتاح والاستهلاك'), fontsize=16)
    ax.set_xlabel(display_arabic_text('الدخل المتاح (مليار دينار)'), fontsize=12)
    ax.set_ylabel(display_arabic_text('الاستهلاك (مليار دينار)'), fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)

    st.pyplot(fig)

    # حساب معامل الارتباط
    correlation = np.corrcoef(income, consumption)[0, 1]
    st.write(f"معامل الارتباط بين الدخل والاستهلاك: {correlation:.4f}")

    # تقدير نموذج الانحدار
    st.markdown('<h3 class="subsection-title">تقدير دالة الاستهلاك</h3>', unsafe_allow_html=True)

    # تجهيز البيانات للانحدار
    X = income.reshape(-1, 1)
    y = consumption

    # تقدير النموذج
    model = LinearRegression()
    model.fit(X, y)

    # معلمات النموذج
    intercept = model.intercept_
    slope = model.coef_[0]

    st.markdown('<div class="content-text">', unsafe_allow_html=True)
    st.markdown(f"""
    ### نتائج تقدير دالة الاستهلاك:

    معادلة دالة الاستهلاك المقدرة:

    الاستهلاك = {intercept:.2f} + {slope:.2f} × الدخل المتاح

    حيث:
    - {intercept:.2f} هو الاستهلاك التلقائي (C₀)
    - {slope:.2f} هو الميل الحدي للاستهلاك (c)

    ### تفسير النتائج:

    - **الاستهلاك التلقائي**: يقدر بـ {intercept:.2f} مليار دينار، وهو الاستهلاك الذي يحدث حتى لو كان الدخل صفر (من خلال الاقتراض أو استخدام المدخرات)

    - **الميل الحدي للاستهلاك**: يقدر بـ {slope:.2f}، وهذا يعني أن كل زيادة في الدخل بمقدار 1 مليار دينار تؤدي إلى زيادة في الاستهلاك بمقدار {slope:.2f} مليار دينار
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    # رسم خط الانحدار مع البيانات
    fig, ax = plt.subplots(figsize=(10, 6))

    # البيانات الفعلية
    ax.scatter(income, consumption, color='#1976D2', s=80, alpha=0.7, label=display_arabic_text('البيانات الفعلية'))

    # خط الانحدار المقدر
    income_range = np.linspace(income.min() - 500, income.max() + 500, 100)
    consumption_pred = intercept + slope * income_range
    ax.plot(income_range, consumption_pred, 'r-', linewidth=2, label=display_arabic_text('دالة الاستهلاك المقدرة'))

    # إضافة معادلة الانحدار على الرسم
    equation = f"C = {intercept:.2f} + {slope:.2f}Y"
    ax.text(0.05, 0.95, display_arabic_text(equation), transform=ax.transAxes,
            fontsize=12, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    ax.set_title(display_arabic_text('دالة الاستهلاك المقدرة'), fontsize=16)
    ax.set_xlabel(display_arabic_text('الدخل المتاح (مليار دينار)'), fontsize=12)
    ax.set_ylabel(display_arabic_text('الاستهلاك (مليار دينار)'), fontsize=12)
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.7)

    st.pyplot(fig)

    # قياس جودة النموذج
    st.markdown('<h3 class="subsection-title">تقييم النموذج</h3>', unsafe_allow_html=True)

    # التنبؤات
    y_pred = model.predict(X)

    # حساب المعايير
    r2 = r2_score(y, y_pred)
    mse = mean_squared_error(y, y_pred)
    rmse = np.sqrt(mse)

    st.markdown(f"""
    - معامل التحديد (R²): {r2:.4f}
    - متوسط مربعات الخطأ (MSE): {mse:.2f}
    - الجذر التربيعي لمتوسط مربعات الخطأ (RMSE): {rmse:.2f}
    """)

    # اختبار إحصائي للنموذج
    X_sm = sm.add_constant(X)
    model_sm = sm.OLS(y, X_sm).fit()

    st.text(model_sm.summary().as_text())

    # تحليل البواقي
    st.markdown('<h3 class="subsection-title">تحليل البواقي</h3>', unsafe_allow_html=True)

    # البواقي
    residuals = y - y_pred

    # رسم البواقي
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # البواقي مقابل القيم المتوقعة
    axes[0].scatter(y_pred, residuals, color='#1976D2', alpha=0.7)
    axes[0].axhline(y=0, color='red', linestyle='-', alpha=0.3)
    axes[0].set_title(display_arabic_text('البواقي مقابل القيم المتوقعة'), fontsize=14)
    axes[0].set_xlabel(display_arabic_text('القيم المتوقعة'), fontsize=12)
    axes[0].set_ylabel(display_arabic_text('البواقي'), fontsize=12)
    axes[0].grid(True, linestyle='--', alpha=0.7)

    # المدرج التكراري للبواقي
    axes[1].hist(residuals, bins=8, color='#1976D2', alpha=0.7)
    axes[1].set_title(display_arabic_text('توزيع البواقي'), fontsize=14)
    axes[1].set_xlabel(display_arabic_text('البواقي'), fontsize=12)
    axes[1].set_ylabel(display_arabic_text('التكرار'), fontsize=12)
    axes[1].grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    st.pyplot(fig)

    # التنبؤ بالاستهلاك في المستقبل
    st.markdown('<h3 class="subsection-title">التنبؤ بالاستهلاك في المستقبل</h3>', unsafe_allow_html=True)

    # إدخال قيمة الدخل المتوقع
    expected_income = st.slider(display_arabic_text('قم بتحديد الدخل المتاح المتوقع (مليار دينار)'),
                                min_value=10000, max_value=20000, value=18000, step=500)

    # التنبؤ بالاستهلاك
    predicted_consumption = intercept + slope * expected_income

    st.markdown(f"""
    **النتيجة:** عند دخل متاح قدره {expected_income} مليار دينار، يتوقع أن يكون الاستهلاك {predicted_consumption:.2f} مليار دينار.
    """)

    # رسم التنبؤ
    fig, ax = plt.subplots(figsize=(10, 6))

    # البيانات الفعلية
    ax.scatter(income, consumption, color='#1976D2', s=80, alpha=0.7, label=display_arabic_text('البيانات التاريخية'))

    # خط الانحدار المقدر
    income_range = np.linspace(income.min() - 500, max(income.max(), expected_income) + 500, 100)
    consumption_pred = intercept + slope * income_range
    ax.plot(income_range, consumption_pred, 'r-', linewidth=2, label=display_arabic_text('دالة الاستهلاك المقدرة'))

    # نقطة التنبؤ
    ax.scatter(expected_income, predicted_consumption, color='green', s=100, marker='*',
               label=display_arabic_text('الاستهلاك المتوقع'))

    # خطوط توضيحية للتنبؤ
    ax.axvline(x=expected_income, color='green', linestyle='--', alpha=0.5)
    ax.axhline(y=predicted_consumption, color='green', linestyle='--', alpha=0.5)

    ax.set_title(display_arabic_text('التنبؤ بالاستهلاك بناءً على الدخل المتاح'), fontsize=16)
    ax.set_xlabel(display_arabic_text('الدخل المتاح (مليار دينار)'), fontsize=12)
    ax.set_ylabel(display_arabic_text('الاستهلاك (مليار دينار)'), fontsize=12)
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.7)

    st.pyplot(fig)

    st.markdown('<div class="tip-box content-text">', unsafe_allow_html=True)
    st.markdown("""
    ### خلاصة التطبيق العملي:

    1. **تقدير دالة الاستهلاك**: نجحنا في تقدير دالة الاستهلاك الكينزية للاقتصاد الجزائري، ووجدنا أن الميل الحدي للاستهلاك يبلغ حوالي 0.7-0.8، وهو ما يتوافق مع النظرية الاقتصادية التي تتوقع أن يكون الميل الحدي للاستهلاك بين 0 و 1

    2. **جودة النموذج**: النموذج يفسر أكثر من 99% من التغيرات في الاستهلاك، مما يشير إلى قوة العلاقة بين الدخل والاستهلاك

    3. **التنبؤ**: يمكننا استخدام النموذج للتنبؤ بمستويات الاستهلاك المستقبلية بناءً على توقعات الدخل

    4. **التطبيقات السياسية**: يمكن استخدام هذا النموذج في:
       - تقدير أثر سياسات إعادة توزيع الدخل على الاستهلاك
       - التنبؤ بأثر التغيرات الضريبية على الاستهلاك الكلي
       - تحليل أثر برامج التحفيز الاقتصادي

    5. **الحدود**: النموذج يفترض علاقة خطية بسيطة، في حين أن العلاقة الحقيقية قد تكون أكثر تعقيدًا وتتأثر بعوامل أخرى مثل سعر الفائدة، التوقعات، توزيع الدخل، وغيرها
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<style>
.footer {
    padding: 20px;
    text-align: center;
    color: #555;
    font-size: 16px;
    margin-top: 40px;
    border-top: 1px solid #ddd;
}
</style>
<div class="footer">
    تم إعداد هذا الدليل من طرف الدكتور رودان   للطلبة المبتدئين في القياس الاقتصادي في الجزائر
    <br>
    استخدم هذا التطبيق كمرجع تعليمي فقط، واستشر المصادر المتخصصة للتطبيقات الرسمية
</div>
""", unsafe_allow_html=True)