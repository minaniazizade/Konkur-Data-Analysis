import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="تحلیل داده‌های کنکور",
    layout="wide"
)

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Segoe UI', Tahoma, Arial, sans-serif;
}

.subtitle {
    text-align: center;
    font-size: 17px;
    color: #91899D;
    margin-bottom: 35px;
}

.metric-box {
    background: #FFFFFF;
    padding: 22px 15px;
    border-radius: 22px;
    border: 1px solid #EEE7F1;
    text-align: center;
    box-shadow: 0 7px 25px rgba(130, 110, 145, 0.08);
    transition: 0.2s;
}

.metric-box:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 30px rgba(130, 110, 145, 0.13);
}

.metric-title {
    font-size: 14px;
    color: #9A919F;
    margin-bottom: 8px;
}

.metric-value {
    font-size: 28px;
    font-weight: 800;
    color: #62586F;
}

[data-testid="stMetric"] {
    background: #FFFFFF;
    border-radius: 20px;
    padding: 15px;
}

.stButton > button {
    background: #DCCFEA;
    color: #574D64;
    border: none;
    border-radius: 14px;
    font-weight: 600;
}

.stButton > button:hover {
    background: #CFC0E2;
    color: #4F465B;
}

input {
    border-radius: 12px !important;
}

[data-testid="stDataFrame"] {
    border-radius: 18px;
    overflow: hidden;
}

.stAlert {
    border-radius: 15px;
}

hr {
    border: none;
    border-top: 1px solid #E9E1EA;
    margin: 35px 0;
}

h1 {
    color: #5E536C;
}

h2 {
    color: #685C76;
}

h3 {
    color: #756981;
}

</style>""", unsafe_allow_html=True)

@st.cache_data
def load_data():

    df = pd.read_csv(
        "final.csv",
        low_memory=False
    )

    numeric_columns = [
        "رتبه کشوری",
        "رتبه در منطقه",
        "سابقه کانونی",
        "میانگین تراز کانون",
        "تعداد آزمون",
        "سال"
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    return df


try:
    df = load_data()

except FileNotFoundError:
    st.error("error!")
    st.stop()

except Exception as e:
    st.error("error!")
    st.code(str(e))
    st.stop()


st.markdown(
    '<div class="title">داشبورد تحلیل داده‌های کنکور</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">  تحلیل رتبه | تراز | رشته | دانشگاه قبولی </div>',
    unsafe_allow_html=True
)


st.sidebar.title("فیلترها")

filtered = df.copy()


if "سال" in df.columns:

    years = sorted(
        df["سال"].dropna().unique().tolist()
    )

    selected_year = st.sidebar.multiselect(
        "سال",
        years,
        default=years
    )

    if selected_year:
        filtered = filtered[
            filtered["سال"].isin(selected_year)
        ]


if "رشته مدرسه" in df.columns:

    school_fields = sorted(
        df["رشته مدرسه"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_school = st.sidebar.multiselect(
        "رشته مدرسه",
        school_fields
    )

    if selected_school:
        filtered = filtered[
            filtered["رشته مدرسه"]
            .astype(str)
            .isin(selected_school)
        ]


if "منطقه" in df.columns:

    regions = sorted(
        df["منطقه"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_region = st.sidebar.multiselect(
        "منطقه",
        regions
    )

    if selected_region:
        filtered = filtered[
            filtered["منطقه"]
            .astype(str)
            .isin(selected_region)
        ]


if "شهر" in df.columns:

    cities = sorted(
        df["شهر"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_city = st.sidebar.multiselect(
        "شهر",
        cities
    )

    if selected_city:
        filtered = filtered[
            filtered["شهر"]
            .astype(str)
            .isin(selected_city)
        ]


if "رشته قبولی" in df.columns:

    fields = sorted(
        df["رشته قبولی"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_field = st.sidebar.multiselect(
        "رشته قبولی",
        fields
    )

    if selected_field:
        filtered = filtered[
            filtered["رشته قبولی"]
            .astype(str)
            .isin(selected_field)
        ]


if "دانشگاه قبولی" in df.columns:

    universities = sorted(
        df["دانشگاه قبولی"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_university = st.sidebar.multiselect(
        "دانشگاه قبولی",
        universities
    )

    if selected_university:
        filtered = filtered[
            filtered["دانشگاه قبولی"]
            .astype(str)
            .isin(selected_university)
        ]


st.sidebar.markdown("---")
st.sidebar.write(f"تعداد رکوردها: {len(filtered):,}")
st.header("نمای کلی")

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-title">
                تعداد رکورد
            </div>
            <div class="metric-value">
                {len(filtered):,}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with c2:

    if len(filtered) > 0:

        best_rank = filtered["رتبه کشوری"].min()

        value = (
            f"{best_rank:,.0f}"
            if pd.notna(best_rank)
            else "-"
        )

    else:
        value = "-"

    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-title">
                بهترین رتبه کشوری
            </div>
            <div class="metric-value">
                {value}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with c3:

    if len(filtered) > 0:

        avg_score = filtered[
            "میانگین تراز کانون"
        ].mean()

        value = (
            f"{avg_score:,.0f}"
            if pd.notna(avg_score)
            else "-"
        )

    else:
        value = "-"

    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-title">
                میانگین تراز
            </div>
            <div class="metric-value">
                {value}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with c4:

    if len(filtered) > 0:

        avg_tests = filtered[
            "تعداد آزمون"
        ].mean()

        value = (
            f"{avg_tests:,.1f}"
            if pd.notna(avg_tests)
            else "-"
        )

    else:
        value = "-"

    st.markdown(
        f"""
        <div class="metric-box">
            <div class="metric-title">
                میانگین تعداد آزمون
            </div>
            <div class="metric-value">
                {value}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "رتبه و تراز",
    "رشته قبولی",
    "دانشگاه",
    "شهر و منطقه",
    "داده‌ها"
])

with tab1:

    st.header("تحلیل رتبه و تراز")


    col1, col2 = st.columns(2)


    with col1:

        rank_data = filtered[
            "رتبه کشوری"
        ].dropna()

        fig = px.histogram(
            rank_data,
            x="رتبه کشوری",
            nbins=50,
            title="توزیع رتبه کشوری"
        )

        fig.update_layout(
            template="plotly_white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    with col2:

        score_data = filtered[
            "میانگین تراز کانون"
        ].dropna()

        fig = px.histogram(
            score_data,
            x="میانگین تراز کانون",
            nbins=50,
            title="توزیع میانگین تراز"
        )

        fig.update_layout(
            template="plotly_white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    scatter_data = filtered[
        [
            "رتبه کشوری",
            "رتبه در منطقه",
            "منطقه"
        ]
    ].dropna()


    fig = px.scatter(
        scatter_data,
        x="رتبه کشوری",
        y="رتبه در منطقه",
        color="منطقه",
        title="رابطه رتبه کشوری و رتبه منطقه"
    )

    fig.update_layout(
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with tab2:

    st.header("رشته‌های قبولی")


    field_count = (
        filtered["رشته قبولی"]
        .value_counts()
        .head(20)
        .sort_values()
    )


    fig = px.bar(
        x=field_count.values,
        y=field_count.index,
        orientation="h",
        title="رشته با بیشترین تعداد قبولی"
    )

    fig.update_layout(
        template="plotly_white",
        xaxis_title="تعداد",
        yaxis_title="رشته"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    if "رشته مدرسه" in filtered.columns:

        cross = pd.crosstab(
            filtered["رشته مدرسه"],
            filtered["رشته قبولی"]
        )

        top_fields = (
            filtered["رشته قبولی"]
            .value_counts()
            .head(10)
            .index
        )

        cross = cross[
            [
                x for x in top_fields
                if x in cross.columns
            ]
        ]


        fig = px.bar(
            cross,
            barmode="group",
            title="رشته قبولی بر اساس رشته مدرسه"
        )

        fig.update_layout(
            template="plotly_white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

with tab3:

    st.header("تحلیل دانشگاه‌ها")


    university_count = (
        filtered["دانشگاه قبولی"]
        .value_counts()
        .head(20)
        .sort_values()
    )


    fig = px.bar(
        x=university_count.values,
        y=university_count.index,
        orientation="h",
        title="دانشگاه با بیشترین تعداد قبولی"
    )

    fig.update_layout(
        template="plotly_white",
        xaxis_title="تعداد قبولی",
        yaxis_title="دانشگاه"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    top_universities = (
        filtered["دانشگاه قبولی"]
        .value_counts()
        .head(10)
        .index
    )


    uni_data = filtered[
        filtered["دانشگاه قبولی"]
        .isin(top_universities)
    ]


    if len(uni_data) > 0:

        fig = px.sunburst(
            uni_data,
            path=[
                "دانشگاه قبولی",
                "رشته قبولی"
            ],
            title="دانشگاه و رشته قبولی"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

with tab4:
    st.header("شهر و منطقه")
    col1, col2 = st.columns(2)
    with col1:

        region_count = (
            filtered["منطقه"]
            .value_counts()
        )

        fig = px.pie(
            values=region_count.values,
            names=region_count.index,
            title="توزیع مناطق"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:
        city_count = (
            filtered["شهر"]
            .value_counts()
            .head(20)
            .sort_values()
        )


        fig = px.bar(
            x=city_count.values,
            y=city_count.index,
            orientation="h",
            title="شهر با بیشترین تعداد"
        )

        fig.update_layout(
            template="plotly_white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


with tab5:
    st.header("📋 داده‌های فیلترشده")
    st.write(
        f"تعداد رکورد:{len(filtered):,}"
    )
    st.dataframe(
        filtered,
        use_container_width=True,
        height=600
    )

st.markdown("---")
st.caption("داشبورد تحلیل داده‌های کنکور")