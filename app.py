import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sri Lanka Climate Dashboard",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .about-box {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 1px solid #2d6a4f;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_excel("sri_lanka_climate_cleaned.xlsx")
    df = df.dropna(subset=["Value"])
    return df

df = load_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/1/11/Flag_of_Sri_Lanka.svg", width=140)
st.sidebar.title("🌿 Dashboard Controls")
st.sidebar.markdown("---")

categories = {
    "🌱 Agriculture & Land": [i for i in df["Indicator Name"].unique() if any(k in i.lower() for k in ["agri", "land", "forest", "crop", "cereal", "fertilizer"])],
    "⚡ Energy": [i for i in df["Indicator Name"].unique() if any(k in i.lower() for k in ["energy", "electric", "fuel", "renewable"])],
    "🌡️ Climate": [i for i in df["Indicator Name"].unique() if any(k in i.lower() for k in ["co2", "emission", "temperature", "drought", "disaster", "flood"])],
    "👥 Population & Health": [i for i in df["Indicator Name"].unique() if any(k in i.lower() for k in ["population", "mortality", "health", "poverty", "urban"])],
    "💧 Water & Environment": [i for i in df["Indicator Name"].unique() if any(k in i.lower() for k in ["water", "marine", "protected", "terrestrial"])],
    "📊 All Indicators": list(df["Indicator Name"].unique())
}

selected_category = st.sidebar.selectbox("📂 Select Category", list(categories.keys()))
available_indicators = sorted(categories[selected_category])
selected_indicator = st.sidebar.selectbox("📈 Select Indicator", available_indicators)

st.sidebar.markdown("---")
year_min = int(df["Year"].min())
year_max = int(df["Year"].max())
year_range = st.sidebar.slider("📅 Year Range", year_min, year_max, (1990, year_max))

st.sidebar.markdown("---")
chart_theme = st.sidebar.selectbox("🎨 Chart Theme", ["Greens", "Blues", "Viridis", "Plasma", "Turbo"])

st.sidebar.markdown("---")
st.sidebar.markdown("**📌 About**")
st.sidebar.markdown("📊 Data: World Bank / HDX")
st.sidebar.markdown("🇱🇰 Country: Sri Lanka")
st.sidebar.markdown("📅 Period: 1960–2024")
st.sidebar.markdown("📚 Module: 5DATA004C")

# ── Filter data ───────────────────────────────────────────────────────────────
filtered = df[
    (df["Indicator Name"] == selected_indicator) &
    (df["Year"] >= year_range[0]) &
    (df["Year"] <= year_range[1])
].sort_values("Year")

# ── HEADER ────────────────────────────────────────────────────────────────────
col_title, col_logo = st.columns([4, 1])
with col_title:
    st.markdown("# 🌿 Sri Lanka Climate Change Dashboard")
    st.markdown("*Tracking environmental and climate indicators from 1960 to 2024*")
with col_logo:
    st.image("https://upload.wikimedia.org/wikipedia/commons/1/11/Flag_of_Sri_Lanka.svg", width=80)

st.markdown("---")

# ── ABOUT SECTION ─────────────────────────────────────────────────────────────
with st.expander("ℹ️ About This Dashboard", expanded=False):
    st.markdown("""
    **🌍 Purpose**  
    This interactive dashboard explores Sri Lanka's climate change indicators using World Bank data 
    sourced from the Humanitarian Data Exchange (HDX). It supports data-driven decision-making 
    at sustainability conferences and policy meetings.

    **📊 Dataset**  
    1,534 records | 48 climate indicators | 1960–2024

    **🔍 How to Use**  
    Use the sidebar to filter by category, indicator, and year range. 
    Explore trends, compare indicators, and download filtered data.
    """)

# ── KPI CARDS ─────────────────────────────────────────────────────────────────
if not filtered.empty:
    latest = filtered.iloc[-1]
    earliest = filtered.iloc[0]
    max_val = filtered["Value"].max()
    min_val = filtered["Value"].min()
    avg_val = filtered["Value"].mean()

    if earliest["Value"] != 0:
        change_pct = ((latest["Value"] - earliest["Value"]) / abs(earliest["Value"])) * 100
    else:
        change_pct = 0

    st.markdown("### 📊 Key Statistics")
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.metric(f"Latest ({int(latest['Year'])})", f"{latest['Value']:,.2f}", delta=f"{change_pct:+.1f}%")
    with c2:
        st.metric(f"Earliest ({int(earliest['Year'])})", f"{earliest['Value']:,.2f}")
    with c3:
        st.metric("Peak Value", f"{max_val:,.2f}")
    with c4:
        st.metric("Lowest Value", f"{min_val:,.2f}")
    with c5:
        st.metric("Average", f"{avg_val:,.2f}")

    st.markdown("---")

    # ── TABS ──────────────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Trend Analysis",
        "📊 Year Breakdown",
        "🔍 Compare Indicators",
        "🕐 Decade Overview",
        "📋 Data Explorer"
    ])

    # ── TAB 1: TREND ANALYSIS ─────────────────────────────────────────────────
    with tab1:
        st.subheader(f"📈 Trend Over Time: {selected_indicator}")
        show_ma = st.checkbox("Show 5-Year Moving Average", value=True)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=filtered["Year"], y=filtered["Value"],
            mode="lines+markers", name=selected_indicator,
            line=dict(color="#2d9e6b", width=3),
            marker=dict(size=7, color="#90EE90"),
            hovertemplate="<b>Year:</b> %{x}<br><b>Value:</b> %{y:,.2f}<extra></extra>"
        ))

        if show_ma and len(filtered) >= 5:
            filtered_ma = filtered.copy()
            filtered_ma["MA"] = filtered_ma["Value"].rolling(window=5, center=True).mean()
            fig.add_trace(go.Scatter(
                x=filtered_ma["Year"], y=filtered_ma["MA"],
                mode="lines", name="5-Year Moving Avg",
                line=dict(color="#FFD700", width=2, dash="dash"),
                hovertemplate="<b>Moving Avg:</b> %{y:,.2f}<extra></extra>"
            ))

        fig.update_layout(
            title=f"{selected_indicator} ({year_range[0]}–{year_range[1]})",
            xaxis_title="Year", yaxis_title="Value",
            hovermode="x unified",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0.1)",
            font=dict(color="white"),
            legend=dict(bgcolor="rgba(0,0,0,0.3)"), height=450
        )
        fig.update_xaxes(showgrid=True, gridcolor="rgba(255,255,255,0.1)")
        fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.1)")
        st.plotly_chart(fig, use_container_width=True)

        direction = "increased 📈" if change_pct > 0 else "decreased 📉"
        st.info(f"💡 **Insight:** {selected_indicator} has {direction} by **{abs(change_pct):.1f}%** from {int(earliest['Year'])} to {int(latest['Year'])}.")

    # ── TAB 2: BAR CHART ──────────────────────────────────────────────────────
    with tab2:
        st.subheader(f"📊 Value by Year: {selected_indicator}")
        fig_bar = px.bar(
            filtered, x="Year", y="Value",
            color="Value", color_continuous_scale=chart_theme,
            title=f"{selected_indicator} — Annual Values",
            hover_data={"Year": True, "Value": ":.2f"}
        )
        fig_bar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0.1)",
            font=dict(color="white"), height=450
        )
        fig_bar.update_xaxes(showgrid=False)
        fig_bar.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.1)")
        st.plotly_chart(fig_bar, use_container_width=True)

    # ── TAB 3: COMPARE ────────────────────────────────────────────────────────
    with tab3:
        st.subheader("🔍 Compare Multiple Indicators Over Time")
        all_indicators = sorted(df["Indicator Name"].unique())
        compare_indicators = st.multiselect(
            "Select indicators to compare",
            all_indicators, default=all_indicators[:3]
        )

        if compare_indicators:
            compare_df = df[
                (df["Indicator Name"].isin(compare_indicators)) &
                (df["Year"] >= year_range[0]) &
                (df["Year"] <= year_range[1])
            ]
            normalize = st.checkbox("Normalize values (0–100 scale) for fair comparison", value=False)

            if normalize:
                def normalize_series(s):
                    mn, mx = s.min(), s.max()
                    return (s - mn) / (mx - mn) * 100 if mx != mn else s * 0
                compare_df = compare_df.copy()
                compare_df["Value"] = compare_df.groupby("Indicator Name")["Value"].transform(normalize_series)

            fig_comp = px.line(
                compare_df, x="Year", y="Value", color="Indicator Name",
                markers=True,
                title="Indicator Comparison" + (" (Normalized)" if normalize else ""),
                labels={"Value": "Normalized (0–100)" if normalize else "Value"}
            )
            fig_comp.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0.1)",
                font=dict(color="white"),
                legend=dict(bgcolor="rgba(0,0,0,0.3)", orientation="h", yanchor="bottom", y=-0.4),
                height=500
            )
            fig_comp.update_xaxes(showgrid=True, gridcolor="rgba(255,255,255,0.1)")
            fig_comp.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.1)")
            st.plotly_chart(fig_comp, use_container_width=True)

    # ── TAB 4: DECADE OVERVIEW ────────────────────────────────────────────────
    with tab4:
        st.subheader("🕐 Decade-by-Decade Overview")

        decade_df = filtered.copy()
        decade_df["Decade"] = (decade_df["Year"] // 10 * 10).astype(str) + "s"
        decade_avg = decade_df.groupby("Decade")["Value"].mean().reset_index()
        decade_avg.columns = ["Decade", "Average Value"]

        col_d1, col_d2 = st.columns(2)
        with col_d1:
            fig_decade = px.bar(
                decade_avg, x="Decade", y="Average Value",
                color="Average Value", color_continuous_scale=chart_theme,
                title=f"Average by Decade", text="Average Value"
            )
            fig_decade.update_traces(texttemplate="%{text:,.1f}", textposition="outside")
            fig_decade.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0.1)",
                font=dict(color="white"), height=400
            )
            st.plotly_chart(fig_decade, use_container_width=True)

        with col_d2:
            fig_pie = px.pie(
                decade_avg, names="Decade", values="Average Value",
                title="Decade Distribution",
                color_discrete_sequence=px.colors.sequential.Greens_r,
                hole=0.4
            )
            fig_pie.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white"), height=400
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        st.subheader("🌡️ All Indicators Heatmap by Decade")
        heat_df = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])].copy()
        heat_df["Decade"] = (heat_df["Year"] // 10 * 10).astype(str) + "s"
        heat_pivot = heat_df.groupby(["Indicator Name", "Decade"])["Value"].mean().reset_index()
        heat_pivot = heat_pivot.pivot(index="Indicator Name", columns="Decade", values="Value")
        heat_norm = heat_pivot.apply(
            lambda x: (x - x.min()) / (x.max() - x.min()) if x.max() != x.min() else x, axis=1
        )
        fig_heat = px.imshow(
            heat_norm, color_continuous_scale="RdYlGn",
            title="Normalized Indicator Performance by Decade",
            aspect="auto", height=600
        )
        fig_heat.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white", size=10)
        )
        st.plotly_chart(fig_heat, use_container_width=True)

    # ── TAB 5: DATA EXPLORER ──────────────────────────────────────────────────
    with tab5:
        st.subheader("📋 Data Explorer")

        col_f1, col_f2 = st.columns(2)
        with col_f1:
            show_all = st.checkbox("Show all indicators", value=False)
        with col_f2:
            sort_by = st.selectbox("Sort by", ["Year", "Value", "Indicator Name"])

        display_df = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])].sort_values(sort_by) if show_all else filtered.sort_values(sort_by)

        st.dataframe(display_df.reset_index(drop=True), use_container_width=True, height=400)

        col_dl1, col_dl2 = st.columns(2)
        with col_dl1:
            st.download_button(
                "⬇️ Download as CSV",
                data=display_df.to_csv(index=False),
                file_name="sri_lanka_climate_data.csv",
                mime="text/csv",
                use_container_width=True
            )
        with col_dl2:
            st.metric("Total Rows", len(display_df))

else:
    st.warning("⚠️ No data available. Please adjust your filters.")

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("---")
col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    st.markdown("**🌿 Sri Lanka Climate Dashboard**")
with col_f2:
    st.markdown("**📚 Module:** 5DATA004C")
with col_f3:
    st.markdown("**📊 Data:** World Bank via HDX | 1960–2024")
