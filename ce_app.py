import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import plotly.graph_objects as go


# Set page config
st.set_page_config(
    page_title="Circular Economy Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🌍 Circular Europe: Unpacking Progress Through Data")
st.markdown("A data-driven exploration of sustainability trends using Eurostat datasets.")
st.markdown("By Anusha Kogunde Vijaya")


tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["Overview","Top Waste generators", "Plastic Waste", "Municipal Waste","WEEE","Circular Material","Material Dependency", "Conclusions"])
with tab1:
    

    from PIL import Image

    # Title
    st.markdown("## ♻️ Understanding the Circular Economy")

    # Two-column layout
    col1, col2 = st.columns([1.2, 1])

    # Column 1: Textual explanation
    with col1:
        # Styled: What is Circular Economy?
        st.markdown("""
        <h2 style='font-size: 36px; color: #2e7d32; font-weight: 800; margin-bottom: 20px;'>
            🌍 What is the Circular Economy?
        </h2>
        <div style='font-size: 20px; line-height: 1.6;'>
            A <b>circular economy</b> is a <b>regenerative model</b> of production and consumption that involves:
            <ul>
                <li>🔁 Sharing</li>
                <li>♻️ Reusing</li>
                <li>🔧 Repairing</li>
                <li>🛠️ Refurbishing</li>
                <li>🔄 Recycling</li>
            </ul>
            Instead of the traditional <b>Take → Make → Dispose</b> model,  
            it promotes <b>Reduce → Reuse → Recycle → Regenerate</b>.
        </div>
        """, unsafe_allow_html=True)

        # Styled: Why Shift to a Circular Economy?
        st.markdown("""
        <h2 style='font-size: 36px; color: #2e7d32; font-weight: 800; margin-top: 40px; margin-bottom: 20px;'>
            🌱 Why Shift to a Circular Economy?
        </h2>
        <div style='font-size: 20px; line-height: 1.6;'>
            ✅ <b>Protects the environment</b>: Cuts waste, reduces raw material extraction, preserves biodiversity<br>
            ✅ <b>Boosts economic resilience</b>: Lowers raw material dependence, stabilizes costs<br>
            ✅ <b>Generates innovation and jobs</b>: EU estimates 700,000 new jobs by 2030<br>
            ✅ <b>Saves consumers money</b>: Durable, repairable products with longer lifespans
        </div>
        """, unsafe_allow_html=True)

    # Column 2: Visual icon/diagram
    with col2:
        image = Image.open("ce.png")  # Replace with your actual image path
        st.image(image, caption="Circular Economy Loop", use_container_width=True)

    # Divider
    st.markdown("---")

    # EU Action Section
    st.markdown("""
    **DATA SOURCES:** The EU is moving toward a more sustainable future through the  
    [European Circular Economy Action Plan](https://ec.europa.eu/eurostat/web/circular-economy).
    """)
    



with tab2:
    st.header("♻️ Top 10 Waste Generators in Europe")
    df_waste = pd.read_csv("./Dataset_CE/Total_waste_generation_per_capita.csv")
    df_filtered = df_waste.copy()

    # Step 1: Filter the last 20 years
    recent_years = sorted(df_filtered['TIME_PERIOD'].unique())[-20:]
    df_20yrs = df_filtered[df_filtered['TIME_PERIOD'].isin(recent_years)]

    # Step 2: Rename for consistency
    df_20yrs = df_20yrs.rename(columns={'Geopolitical entity (reporting)': 'country', 'TIME_PERIOD': 'year'})

    # Step 3: Get top 10 countries per year
    top10_per_year = (
        df_20yrs.groupby('year', group_keys=False)
        .apply(lambda x: x.nlargest(10, 'OBS_VALUE'))
        .reset_index(drop=True)
    )

    # Step 4: Create animated bar chart
    fig = px.bar(
        top10_per_year,
        x='country',
        y='OBS_VALUE',
        color='country',
        animation_frame='year',
        title='Top 10 Waste-Generating Countries in Europe (Last 20 Years)',
        labels={'OBS_VALUE': 'Waste Generated (Kilograms percapita)', 'country': 'Country'},
        template='plotly_white'
    )

    # Step 5: Adjust animation speed and layout
    fig.update_layout(
        xaxis={'categoryorder': 'total descending'},
        yaxis_title='Waste Generated (in Kilograms per capita)',
        xaxis_title='Country',
        transition={'duration': 1000},  # 1 second per frame
        updatemenus=[{
            'buttons': [
                {'args': [None, {'frame': {'duration': 1000, 'redraw': True}, 'fromcurrent': True}],
                'label': 'Play',
                'method': 'animate'},
                {'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate'}],
                'label': 'Pause',
                'method': 'animate'}
            ],
            'direction': 'left',
            'pad': {'r': 10, 't': 87},
            'showactive': False,
            'type': 'buttons',
            'x': 0.1,
            'xanchor': 'right',
            'y': 0,
            'yanchor': 'top'
        }]
    )


    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("🛍️ Plastic Packaging Waste Generation vs Plastic Packaging Recycling Rate")

    st.markdown("""
    **Tracking Plastic Use and Recycling in the EU**  
    Plastics are integral to modern life — but managing their end-of-life is crucial. This section looks at:

    - **Plastic packaging waste generated per person (kg/year)**
    - **Recycling rate of plastic packaging (%)**

    📊 **Current figures (EU‑27, 2021):**
    - 🛒 **35.9 kg/person of plastic waste** generated annually  
    - ♻️ **41.3%** of plastic packaging was recycled  

    While recycling efforts are improving, **plastic waste generation continues to grow**, highlighting the need for **prevention**, **reuse**, and **innovation** in packaging design and materials.
    """)

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Plastic Waste per Person (2021)", value="35.9 kg")
    with col2:
        st.metric(label="Plastic Recycling Rate (2021)", value="41.3%")

  

    # Read datasets
    df_plastic_packaging_gen = pd.read_csv("./Dataset_CE/Generation_plastic_pkg_waste_per_capita.csv")
    df_packaging_recy = pd.read_csv("./Dataset_CE/Recycle_Plastic_pkging.csv")

    # --- Plastic Packaging Waste Chart ---
    st.subheader("Plastic Packaging Waste Generation (Top 10)")

    last_20_years = sorted(df_plastic_packaging_gen['TIME_PERIOD'].unique())[-20:]
    df_recent = df_plastic_packaging_gen[df_plastic_packaging_gen['TIME_PERIOD'].isin(last_20_years)]

    country_totals = df_recent.groupby('Geopolitical entity (reporting)')['OBS_VALUE'].sum().sort_values(ascending=False)
    top10_countries = country_totals.head(10).index.tolist()
    top3 = top10_countries[:3]
    rest = top10_countries[3:]

    germany_entry = [c for c in top10_countries if "Germany" in c]
    rest_except_germany = [c for c in rest if c != germany_entry[0]] if germany_entry else rest

    df_top10 = df_recent[df_recent['Geopolitical entity (reporting)'].isin(top10_countries)]

    fig = go.Figure()

    top3_colors = ['#1f77b4', '#2a9fd6', '#99ccff']
    for i, country in enumerate(top3):
        df_country = df_top10[df_top10['Geopolitical entity (reporting)'] == country]
        fig.add_trace(go.Scatter(
            x=df_country['TIME_PERIOD'],
            y=df_country['OBS_VALUE'],
            mode='lines+markers',
            name=country,
            line=dict(color=top3_colors[i], width=3),
            marker=dict(size=6)
        ))

    if germany_entry:
        df_germany = df_top10[df_top10['Geopolitical entity (reporting)'] == germany_entry[0]]
        fig.add_trace(go.Scatter(
            x=df_germany['TIME_PERIOD'],
            y=df_germany['OBS_VALUE'],
            mode='lines+markers',
            name='Germany',
            line=dict(color='crimson', width=3),
            marker=dict(size=6, symbol='circle')
        ))

    grey_shades = ['#cccccc', '#bbbbbb', '#aaaaaa', '#999999', '#888888', '#777777']
    for i, country in enumerate(rest_except_germany):
        df_country = df_top10[df_top10['Geopolitical entity (reporting)'] == country]
        fig.add_trace(go.Scatter(
            x=df_country['TIME_PERIOD'],
            y=df_country['OBS_VALUE'],
            mode='lines',
            name=country,
            line=dict(color=grey_shades[i % len(grey_shades)], width=1.5),
            showlegend=True
        ))

    fig.update_layout(
        
        xaxis_title='Year',
        yaxis_title='Plastic Waste (Kilograms)',
        yaxis=dict(rangemode='tozero'),
        template='plotly_white',
        legend_title='Country',
        hovermode='x unified'
    )

    st.plotly_chart(fig, use_container_width=True)

    # --- Plastic Packaging Recycling Rate Chart ---
    st.subheader("Plastic Packaging Recycling Rate (Top 10)")

    last_20_years = sorted(df_packaging_recy['TIME_PERIOD'].unique())[-20:]
    df_recent = df_packaging_recy[df_packaging_recy['TIME_PERIOD'].isin(last_20_years)]

    country_totals = df_recent.groupby('Geopolitical entity (reporting)')['OBS_VALUE'].sum().sort_values(ascending=False)
    top10_countries = country_totals.head(10).index.tolist()
    top3 = top10_countries[:3]
    rest = top10_countries[3:]

    germany_entry = [c for c in top10_countries if "Germany" in c]
    rest_except_germany = [c for c in rest if c != germany_entry[0]] if germany_entry else rest

    df_top10 = df_recent[df_recent['Geopolitical entity (reporting)'].isin(top10_countries)]

    fig = go.Figure()

    for i, country in enumerate(top3):
        df_country = df_top10[df_top10['Geopolitical entity (reporting)'] == country]
        fig.add_trace(go.Scatter(
            x=df_country['TIME_PERIOD'],
            y=df_country['OBS_VALUE'],
            mode='lines+markers',
            name=country,
            line=dict(color=top3_colors[i], width=3),
            marker=dict(size=6)
        ))

    if germany_entry:
        df_germany = df_top10[df_top10['Geopolitical entity (reporting)'] == germany_entry[0]]
        fig.add_trace(go.Scatter(
            x=df_germany['TIME_PERIOD'],
            y=df_germany['OBS_VALUE'],
            mode='lines+markers',
            name='Germany',
            line=dict(color='crimson', width=3),
            marker=dict(size=6, symbol='circle')
        ))

    for i, country in enumerate(rest_except_germany):
        df_country = df_top10[df_top10['Geopolitical entity (reporting)'] == country]
        fig.add_trace(go.Scatter(
            x=df_country['TIME_PERIOD'],
            y=df_country['OBS_VALUE'],
            mode='lines',
            name=country,
            line=dict(color=grey_shades[i % len(grey_shades)], width=1.5),
            showlegend=True
        ))

    fig.update_layout(
        
        xaxis_title='Year',
        yaxis_title='Plastic Recycling Rate (%)',
        yaxis=dict(rangemode='tozero'),
        template='plotly_white',
        legend_title='Country',
        hovermode='x unified'
    )

    st.plotly_chart(fig, use_container_width=True)


with tab4:
    st.header("🧹 Municipal Waste vs Recycling Rate of Municipal Waste")

    st.markdown("""
        **Managing Our Everyday Waste**  
        Municipal waste includes household and similar waste streams managed by public services. It's measured in:

        - **Generation per person (kg/year)**
        - **Recycling rate (%)** (material recycling + composting)

        📊 **Current trends (EU‑27, 2023):**
        - 💰 **511 kg/person generated** — slightly down from 515 kg in 2022  
        - ♻️ **48% recycled** – includes composting  

        EU aims to **reduce generation** and **increase recycling** to move up the Waste Hierarchy. Prevention and reuse rank highest in priority.
    """)

    st.divider()

    col3, col4 = st.columns(2)
    with col3:
        st.metric(label="Avg Generation (2023)", value="511 kg per person")
    with col4:
        st.metric(label="Recycling Rate (2023)", value="48%")

    st.markdown("### 📈 Trends in Waste Generation & Recycling Over Time")

    # --- Municipal Waste Generation Chart ---
    df_waste = pd.read_csv("./Dataset_CE/municipal_waste_per_capita.csv")
    recent_years = sorted(df_waste['TIME_PERIOD'].unique())[-20:]
    df_recent = df_waste[df_waste['TIME_PERIOD'].isin(recent_years)]

    top10 = df_recent.groupby('Geopolitical entity (reporting)')['OBS_VALUE'].sum().nlargest(10)
    top3 = top10.index[:3]
    rest = top10.index[3:]

    germany = [c for c in top10.index if "Germany" in c]
    if germany:
        rest = [c for c in rest if c != germany[0]]

    df_top10 = df_recent[df_recent['Geopolitical entity (reporting)'].isin(top10.index)]

    fig_waste = go.Figure()
    colors = ['#1f77b4', '#2a9fd6', '#99ccff']

    for i, country in enumerate(top3):
        df_c = df_top10[df_top10['Geopolitical entity (reporting)'] == country]
        fig_waste.add_trace(go.Scatter(
            x=df_c['TIME_PERIOD'],
            y=df_c['OBS_VALUE'],
            mode='lines+markers',
            name=country,
            line=dict(color=colors[i], width=3),
            marker=dict(size=6)
        ))

    if germany:
        df_g = df_top10[df_top10['Geopolitical entity (reporting)'] == germany[0]]
        fig_waste.add_trace(go.Scatter(
            x=df_g['TIME_PERIOD'],
            y=df_g['OBS_VALUE'],
            mode='lines+markers',
            name='Germany',
            line=dict(color='crimson', width=3),
            marker=dict(size=6, symbol='circle')
        ))

    grey = ['#cccccc', '#bbbbbb', '#aaaaaa', '#999999', '#888888', '#777777']
    for i, country in enumerate(rest):
        df_c = df_top10[df_top10['Geopolitical entity (reporting)'] == country]
        fig_waste.add_trace(go.Scatter(
            x=df_c['TIME_PERIOD'],
            y=df_c['OBS_VALUE'],
            mode='lines',
            name=country,
            line=dict(color=grey[i % len(grey)], width=1.5)
        ))

    fig_waste.update_layout(
        title='Top 10 Countries: Municipal Waste Generation (Last 20 Years)',
        xaxis_title='Year',
        yaxis_title='Waste per Capita (Kilograms)',
        yaxis=dict(rangemode='tozero'),
        template='plotly_white',
        legend_title='Country',
        hovermode='x unified'
    )

    st.plotly_chart(fig_waste, use_container_width=True)

    # --- Municipal Waste Recycling Rate Chart ---
    df_municipal_waste_recycle = pd.read_csv("./Dataset_CE/Recycling_rate_of_municipal_waste.csv")
    df_municipal_waste_recycle = df_municipal_waste_recycle[
        df_municipal_waste_recycle['Geopolitical entity (reporting)'] != 'European Union - 27 countries (from 2020)'
    ]
    last_10_years = sorted(df_municipal_waste_recycle['TIME_PERIOD'].unique())[-10:]
    df_recent = df_municipal_waste_recycle[df_municipal_waste_recycle['TIME_PERIOD'].isin(last_10_years)]

    country_totals = df_recent.groupby('Geopolitical entity (reporting)')['OBS_VALUE'].sum().sort_values(ascending=False)
    top10_countries = country_totals.head(10).index.tolist()

    germany_entry = [c for c in top10_countries if "Germany" in c]
    is_germany_in_top10 = bool(germany_entry)
    germany_name = germany_entry[0] if is_germany_in_top10 else None

    top10_excluding_germany = [c for c in top10_countries if c != germany_name]
    top2_others = top10_excluding_germany[:2]
    rest = top10_excluding_germany[2:]

    df_top10 = df_recent[df_recent['Geopolitical entity (reporting)'].isin(top10_countries)]

    fig_recycle = go.Figure()

    if is_germany_in_top10:
        df_germany = df_top10[df_top10['Geopolitical entity (reporting)'] == germany_name]
        fig_recycle.add_trace(go.Scatter(
            x=df_germany['TIME_PERIOD'],
            y=df_germany['OBS_VALUE'],
            mode='lines+markers',
            name='Germany',
            line=dict(color='crimson', width=3),
            marker=dict(size=6, symbol='circle')
        ))

    top2_colors = ['#1f77b4', '#2a9fd6']
    for i, country in enumerate(top2_others):
        df_country = df_top10[df_top10['Geopolitical entity (reporting)'] == country]
        fig_recycle.add_trace(go.Scatter(
            x=df_country['TIME_PERIOD'],
            y=df_country['OBS_VALUE'],
            mode='lines+markers',
            name=country,
            line=dict(color=top2_colors[i], width=3),
            marker=dict(size=6)
        ))

    grey_shades = ['#cccccc', '#bbbbbb', '#aaaaaa', '#999999']
    for i, country in enumerate(rest):
        df_country = df_top10[df_top10['Geopolitical entity (reporting)'] == country]
        fig_recycle.add_trace(go.Scatter(
            x=df_country['TIME_PERIOD'],
            y=df_country['OBS_VALUE'],
            mode='lines',
            name=country,
            line=dict(color=grey_shades[i % len(grey_shades)], width=1.5),
            showlegend=True
        ))

    fig_recycle.update_layout(
        title='Top 10 Countries: Municipal Waste Recycling Rate (Last 10 Years)',
        xaxis_title='Year',
        yaxis_title='Recycling Rate (%)',
        yaxis=dict(rangemode='tozero'),
        template='plotly_white',
        legend_title='Country',
        hovermode='x unified'
    )

    st.plotly_chart(fig_recycle, use_container_width=True)

with tab5:
    st.header("🖥️ Waste Electrical and Electronic Equipment (WEEE)")

    st.markdown("""
    **Turning E-waste into Value!**  
                    
    **WEEE** includes **discarded electronics** such as mobile phones, fridges, laptops, and TVs —  
    and is one of the **fastest-growing waste streams** in the EU.

    - 📈 Measured by the **WEEE collection & recycling rate (%)**  
    - 🚛 Progress driven by strong **EU directives** and recycling infrastructure  
    - 🚨 Challenges remain: **illegal flows** and untracked devices

    ⚡ *Every recycled device brings us closer to a circular electronics future.*
    """)

    st.divider()

    col3, col4 = st.columns(2)

    with col3:
        st.metric(label="EU Average (2022)", value="48.7%")

    with col4:
        st.metric(label="Progress Highlight", value="Steady growth since 2010 🚀")

    st.markdown("### 🔁 Tracking WEEE Collection & Recycling Over Time")

    df_weee_recycle = pd.read_csv("./Dataset_CE/Recycling rate of WEEE separately collected.csv")

    # Filter the last 10 years
    last_20_years = sorted(df_weee_recycle['TIME_PERIOD'].unique())[-20:]
    df_recent = df_weee_recycle[df_weee_recycle['TIME_PERIOD'].isin(last_20_years)]

    # Group by country and sum WEEE recycled over last 10 years
    country_totals = df_recent.groupby('Geopolitical entity (reporting)')['OBS_VALUE'].sum().sort_values(ascending=False)

    # Get top 10 countries
    top10_countries = country_totals.head(10).index.tolist()
    top3 = top10_countries[:3]
    rest = top10_countries[3:]

    # Check if Germany is in top 10
    germany_entry = [c for c in top10_countries if "Germany" in c]
    rest_except_germany = [c for c in rest if c != germany_entry[0]] if germany_entry else rest

    # Filter data only for top 10 countries
    df_top10 = df_recent[df_recent['Geopolitical entity (reporting)'].isin(top10_countries)]

    # Create figure
    fig_weee = go.Figure()

    # Add top 3 countries with shades of blue
    top3_colors = ['#1f77b4', '#2a9fd6', '#99ccff']
    for i, country in enumerate(top3):
        df_country = df_top10[df_top10['Geopolitical entity (reporting)'] == country]
        fig_weee.add_trace(go.Scatter(
            x=df_country['TIME_PERIOD'],
            y=df_country['OBS_VALUE'],
            mode='lines+markers',
            name=country,
            line=dict(color=top3_colors[i], width=3),
            marker=dict(size=6)
        ))

    # Add Germany with a distinct color (red)
    if germany_entry:
        df_germany = df_top10[df_top10['Geopolitical entity (reporting)'] == germany_entry[0]]
        fig_weee.add_trace(go.Scatter(
            x=df_germany['TIME_PERIOD'],
            y=df_germany['OBS_VALUE'],
            mode='lines+markers',
            name='Germany',
            line=dict(color='crimson', width=3),
            marker=dict(size=6, symbol='circle')
        ))

    # Add remaining countries with subtle grey gradient
    grey_shades = ['#cccccc', '#bbbbbb', '#aaaaaa', '#999999', '#888888', '#777777']
    for i, country in enumerate(rest_except_germany):
        df_country = df_top10[df_top10['Geopolitical entity (reporting)'] == country]
        fig_weee.add_trace(go.Scatter(
            x=df_country['TIME_PERIOD'],
            y=df_country['OBS_VALUE'],
            mode='lines',
            name=country,
            line=dict(color=grey_shades[i % len(grey_shades)], width=1.5),
            showlegend=True
        ))

    # Layout customization
    fig_weee.update_layout(
        title='Top 10 Countries: WEEE Recycling Rate',
        xaxis_title='Year',
        yaxis_title='WEEE Recycling Rate (%)',
        yaxis=dict(range=[60, 100]),
        template='plotly_white',
        legend_title='Country',
        hovermode='x unified'
    )

    st.plotly_chart(fig_weee, use_container_width=True)

with tab6:
    st.header("♻️ Circular Material Use Rate")

    st.markdown("""
    **Recycling the Loop!**  
    The **CMU rate** tells us how much of the materials we use are **recycled back into the economy**.
    
    - 📊 **Higher rate = less waste, less raw material extraction**  
    - 🌍 **Supports EU’s climate and sustainability goals**  
    - 🎯 Core metric in the EU Circular Economy Action Plan

    🧩 *The more we loop, the less we lose.*
    """)

    st.divider()

    col3, col4 = st.columns(2)
    with col3:
        st.metric(label="EU Average (2022)", value="11.7%")

    with col4:
        st.metric(label="EU Target (2030)", value="Increase significantly 🚀")

    # Load and clean the dataset
    df_circular_mtl_use = pd.read_csv("./Dataset_CE/Circular_material_use_rate.csv")
    df_circular_mtl_use = df_circular_mtl_use[['Geopolitical entity (reporting)', 'TIME_PERIOD', 'OBS_VALUE']].dropna()

    # Keep only the latest year
    latest_year = df_circular_mtl_use['TIME_PERIOD'].max()
    df_latest = df_circular_mtl_use[df_circular_mtl_use['TIME_PERIOD'] == latest_year].copy()

    # Rename and map country names
    df_latest.rename(columns={
        'Geopolitical entity (reporting)': 'Country',
        'OBS_VALUE': 'Circular Material Use Rate (%)'
    }, inplace=True)

    country_name_map = {
        "Czechia": "Czech Republic",
        "EU27_2020": "European Union"
    }
    df_latest['Country'] = df_latest['Country'].replace(country_name_map)

    # Choropleth map
    fig_choropleth = px.choropleth(
        df_latest,
        locations="Country",
        locationmode="country names",
        color="Circular Material Use Rate (%)",
        hover_name="Country",
        color_continuous_scale="Viridis",
        title=f"Circular Material Use Rate by Country ({latest_year})",
        template="plotly_white"
    )

    fig_choropleth.update_geos(
        showcoastlines=True,
        showland=True,
        showcountries=True,
        fitbounds=False,
        projection_type="natural earth"
    )

    fig_choropleth.update_layout(
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        geo=dict(bgcolor="rgba(0,0,0,0)")
    )

    st.plotly_chart(fig_choropleth, use_container_width=True)

    # Animated bar chart: Top 10 countries over last 20 years
    df = df_circular_mtl_use.copy()
    df = df[df["Geopolitical entity (reporting)"] != "European Union - 27 countries (from 2020)"]

    df["TIME_PERIOD"] = pd.to_numeric(df["TIME_PERIOD"], errors='coerce')
    df["OBS_VALUE"] = pd.to_numeric(df["OBS_VALUE"], errors='coerce')

    recent_years = sorted(df["TIME_PERIOD"].dropna().unique())[-20:]
    df = df[df["TIME_PERIOD"].isin(recent_years)]

    df_top10 = df.groupby("TIME_PERIOD").apply(lambda x: x.nlargest(10, "OBS_VALUE")).reset_index(drop=True)

    fig_bar_animated = px.bar(
        df_top10,
        x="OBS_VALUE",
        y="Geopolitical entity (reporting)",
        color="Geopolitical entity (reporting)",
        orientation='h',
        animation_frame="TIME_PERIOD",
        range_x=[0, df_top10["OBS_VALUE"].max() * 1.1],
        title="Top 10 Countries: Circular Material Use Rate",
        labels={
            "OBS_VALUE": "Circular Use Rate (%)",
            "Geopolitical entity (reporting)": "Country"
        },
        template="plotly_white"
    )
    fig_bar_animated.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        xaxis_title="Circular Use Rate (%)",
        yaxis_title="Country",
        legend_title="Country",
        transition={'duration': 500},
        hovermode="closest"
    )

    st.plotly_chart(fig_bar_animated, use_container_width=True)

with tab7:
    st.header("📦 Material Import Dependency-How much do we rely on foreign materials?")

    st.markdown("""
   
    The **Material Import Dependency** indicator shows what share of a country’s material consumption comes from imports.

    - 🏭 **High dependency = more exposure to external supply shocks**
    - 🌐 **Lower dependency = more self-reliant economy**
    - 🔑 Important for the **EU's resilience and circular economy strategies**

    🧲 *The more we extract or recycle locally, the less we depend on global chains.*
    """)

    st.divider()

    col3, col4 = st.columns(2)

    with col3:
        st.metric(label="EU Average (2022)", value="23.0%")

    with col4:
        st.metric(label="Key Insight", value="Some countries > 40% 📈")

    st.markdown("### 🔄 Top 10 Material Import Dependent Countries Over Time")

    # Load and clean data
    df_mtl_dep = pd.read_csv("./Dataset_CE/Material import dependency.csv")
    df_mtl_dep = df_mtl_dep[~df_mtl_dep['Geopolitical entity (reporting)'].str.contains("European Union", na=False)]
    df_mtl_dep = df_mtl_dep.dropna(subset=['OBS_VALUE'])
    df_mtl_dep = df_mtl_dep[df_mtl_dep['TIME_PERIOD'] >= 2003]

    # Compute top 10 countries for each year independently
    df_top10_dynamic = df_mtl_dep.groupby('TIME_PERIOD', group_keys=False).apply(
        lambda g: g.nlargest(10, 'OBS_VALUE')
    ).reset_index(drop=True)

    # Animated bubble chart
    fig = px.scatter(
        df_top10_dynamic,
        x='Geopolitical entity (reporting)',
        y='OBS_VALUE',
        size='OBS_VALUE',
        color='Geopolitical entity (reporting)',
        animation_frame='TIME_PERIOD',
        animation_group='Geopolitical entity (reporting)',
        size_max=60,
        range_y=[0, df_top10_dynamic['OBS_VALUE'].max() + 10],
        title='🔄 Material Import Dependency — Top 10 Countries (Dynamic by Year)',
        labels={
            'OBS_VALUE': 'Material Import Dependency (%)',
            'Geopolitical entity (reporting)': 'Country'
        },
        template='plotly_white'
    )

    # Smooth transition settings
    fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 700  # Animation speed
    fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 500

    fig.update_layout(
        xaxis_title='Country',
        yaxis_title='Import Dependency (%)',
        showlegend=False,
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

with tab8:
    st.header("🔑 Key Takeaways from the Project")

    # Main column layout
    col1, col2 = st.columns([1.3, 1])

    with col1:
        st.markdown("### ♻️ Circular Economy Insights")

        st.markdown("""
        - 📈 **Municipal Waste**: Germany ranks among top waste producers per capita but shows steady improvement in recycling rate.
        - 🧴 **Plastic Packaging Waste**: Rising trend observed, but recycling still lags behind generation rates across the EU.
        - 💻 **WEEE (E-Waste)**: Recycling rate improvements, but gaps persist especially in less-developed EU economies.
        - 🔄 **Circular Material Use Rate (CMUR)**:
            - EU average ~11.5% (2022)
            - Netherlands, Belgium, France lead; Germany improving steadily.
        - 🌍 **Material Import Dependency**:
            - Critical for raw materials security
            - Countries like Belgium, Netherlands show high dependency over time.
        """)

        st.markdown("### 🇪🇺 EU Policy Push")

        st.markdown("""
        - The **European Green Deal** and **Circular Economy Action Plan** aim for climate neutrality and sustainable growth by 2050.
        - Strong legislative moves: Ecodesign, Green Claims Directive, Right to Repair, WEEE directive, and Plastic Packaging rules.
        - Estimated creation of **700,000 circular economy jobs** by 2030.
        """)

        st.markdown("""
        #### 🔗 Further Resources

        - [EU Circular Economy Action Plan](https://ec.europa.eu/environment/circular-economy/)
        - [Eurostat CMU Data](https://ec.europa.eu/eurostat/databrowser/view/cei_srm030/)
        - [WEEE Statistics – Eurostat](https://ec.europa.eu/eurostat/databrowser/view/env_waselee/)
        - [United Nations – Circularity Gap Report](https://www.circularity-gap.world/)

        ---
        """)

        st.markdown("""
        > 🌟 *"Closing the loop isn't just good for the planet — it's a smarter, more sustainable way to grow economies and empower future generations."*
        """)
