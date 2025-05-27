import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import requests




#Streamlit part

st. set_page_config(layout= "wide")
st.title("PHONEPE TRANSACTION INSIGHT")

with st.sidebar:
    
    select=option_menu("Main menu",["Home", "Analysis"])

if select=="Home":
    

    st.markdown("""
    Welcome to **PhonePe Transaction Insight** – a data-driven dashboard designed to uncover meaningful insights from PhonePe's digital transaction ecosystem.

    This project leverages PhonePe Pulse data to provide a comprehensive view of transaction behaviors, user engagement, and market opportunities across India. It aims to support strategic business decisions through interactive visualizations and data analysis.

    ---

    ###  Project Objective

    To analyze and visualize PhonePe’s transaction data across various dimensions—state, time period, category, and user demographics—to derive actionable insights that can drive business growth, product improvements, and policy decisions.

    ---

    ###  Business Use Cases

    #### 1. **Decoding Transaction Dynamics on PhonePe**
    PhonePe observed significant variations in transaction behavior across states, quarters, and payment categories. This use case helps uncover patterns of growth, stagnation, or decline, enabling leadership to craft region-specific and category-specific strategies.

    #### 2. **Device Dominance and User Engagement Analysis**
    By analyzing registered users and app open data segmented by device brand and region, this use case highlights how user engagement varies across devices—informing UI optimization, device-specific campaigns, and tech enhancements.

    #### 3. **Insurance Penetration and Growth Potential**
    With increasing traction in its insurance offerings, PhonePe needs to identify states with high potential but low current adoption. This use case supports strategic marketing and partnership decisions in the insurance domain.

    #### 4. **Transaction Analysis for Market Expansion**
    In a competitive market, identifying emerging regions with high transaction growth is key. This use case explores transaction volumes at the state level to pinpoint areas ripe for market penetration and expansion""")

elif select=="Analysis":
    tab1, tab2, tab3, tab4, tab5=st.tabs(["Analysis 1", "Analysis 2", "Analysis 3", "Analysis 4", "Analysis 5"])
    with tab1:
       
        st.header("Analysis 1: Decoding Transaction Dynamics on PhonePe")
        top_states = pd.read_csv('C:/Users/rakes/Documents/sajinapython/phonepe/my_data.csv')
        st.subheader('Total Transaction Amount Trend by State')
        fig, ax = plt.subplots(figsize=(12, 9))
        sns.lineplot(data=top_states, x="Year", y="Total_Amount", hue="State", marker="o", palette='Set1', ax=ax)
        ax.set_title("Total Transaction Amount Trend by State")
        ax.set_xlabel("Year")
        ax.set_ylabel("Total Amount")
        ax.legend(title="State", bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(fig)

        geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        india_states = requests.get(geojson_url).json()
        st.subheader('Total Transaction Amount by States')
        fig = px.choropleth(
            top_states,
            geojson=india_states,
            featureidkey='properties.ST_NM',
            locations='State',
            color='Total_Amount',
            color_continuous_scale='Rainbow',  # or any other color scale
           
        )
        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig, use_container_width=True)


        Quarterly_by_state=pd.read_csv('C:/Users/rakes/Documents/sajinapython/phonepe/my_data1.csv')
        Quarterly_by_state.columns = Quarterly_by_state.columns.str.strip()
        Quarterly_by_state['time'] = Quarterly_by_state['Year'].astype(str) + '-Q' + Quarterly_by_state['Quarter'].astype(str)
        pivot_df = Quarterly_by_state.pivot(index='State', columns='time', values='Total_Amount').fillna(0)
        st.subheader('Quarterly Transaction by State')
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.heatmap(pivot_df, cmap='YlGnBu', ax=ax)
        ax.set_xlabel('Time (Year-Quarter)')
        ax.set_ylabel('State')
        st.pyplot(fig)


        Payment_category=pd.read_csv('C:/Users/rakes/Documents/sajinapython/phonepe/my_data2')
        st.subheader('Total Transaction trend by Transaction type')
        fig, ax = plt.subplots(figsize=(12, 9))
        sns.lineplot(data=Payment_category, x="Year", y="Total_Amount", hue="Transaction_type", marker="o", palette='Set1', ax=ax)
        ax.set_xlabel("Year")
        ax.set_ylabel("Total Amount")
        ax.legend(title="State", bbox_to_anchor=(1.05, 1), loc='upper left')
        st.pyplot(fig)


        Growth_rate_overstate=pd.read_csv('C:/Users/rakes/Documents/sajinapython/phonepe/my_data3')
        pivot_df = Growth_rate_overstate.pivot(index="State", columns="Year", values="YoY_Growth_Percentage")
        st.subheader('Year-over-Year Growth by State')
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.heatmap(pivot_df,annot=True, cmap='YlGnBu', ax=ax)
        ax.set_xlabel('Year')
        ax.set_ylabel('State')
        st.pyplot(fig)



    
    with tab2:
        st.header("Analysis 2: Device Dominance and User Engagement Analysis")

        Merged=pd.read_csv('C:/Users/rakes/Documents/sajinapython/phonepe/my_data4')
        top_brands = Merged.groupby('Brand')['Count'].sum().sort_values(ascending=False)
        st.subheader('Top Device Brands by Total Users')
        fig, ax = plt.subplots(figsize=(10, 6))
        top_brands.plot(kind='bar', color='skyblue', ax=ax)
        ax.set_xlabel('Device Brand')
        ax.set_ylabel('Total Users')
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)


        st.subheader(" Brand Engagement % Across States")
        engagement = Merged.groupby(['State', 'Brand'])['Brand_Engagement (%)'].mean().reset_index()
        heatmap_data = engagement.pivot(index='State', columns='Brand', values='Brand_Engagement (%)')
        fig, ax = plt.subplots(figsize=(16, 10))
        sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap='YlGnBu', cbar_kws={'label': 'Engagement %'}, ax=ax)
        ax.set_xlabel('Brand')
        ax.set_ylabel('State')
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)

        geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        india_states = requests.get(geojson_url).json()
        st.subheader('Brand Engagement (% ) by States')
        fig = px.choropleth(
            Merged,
            geojson=india_states,
            featureidkey='properties.ST_NM',
            locations='State',
            color='Brand_Engagement (%)',
            color_continuous_scale='Rainbow',  # or any other color scale
           
        )
        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig, use_container_width=True)


        engagement = Merged.groupby(['State', 'Brand'])['AppOpens_per_User'].mean().reset_index()
        heatmap_data = engagement.pivot(index='State', columns='Brand', values='AppOpens_per_User')
        st.subheader(' AppOpens_per_User Across States')
        fig, ax = plt.subplots(figsize=(16, 10))
        sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap='YlGnBu', cbar_kws={'label': 'AppOpens_per_User'}, ax=ax)
        ax.set_xlabel('Brand')
        ax.set_ylabel('State')
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)



    with tab3:
        st.header("Analysis 3: Insurance Penetration and Growth Potential")
        Agg_Insurance=pd.read_csv('C:/Users/rakes/Documents/sajinapython/phonepe/my_data6')
        state_summary = Agg_Insurance.groupby('State')[['Transaction_count', 'Transaction_amount']].sum().sort_values(by='Transaction_count', ascending=False)
        st.subheader("Quarterly Insurance Transaction Trend - Top 5 States ")
        top_states = state_summary.head(5).index.tolist()
        fig, ax = plt.subplots(figsize=(10, 6))
        for state in top_states:
            df = Agg_Insurance[Agg_Insurance['State'] == state]
            df_grouped = df.groupby(['Year', 'Quarter'])['Transaction_count'].sum().reset_index()
            df_grouped['Time'] = df_grouped['Year'].astype(str) + ' Q' + df_grouped['Quarter'].astype(str)
            ax.plot(df_grouped['Time'], df_grouped['Transaction_count'], label=state, marker='o')
        ax.set_xlabel("Quarter")
        ax.set_ylabel("Transaction Count")
        plt.xticks(rotation=45)
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)


        geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        india_states = requests.get(geojson_url).json()
        st.subheader('Insurance Transaction Amount by States')
        fig = px.choropleth(
            Agg_Insurance,
            geojson=india_states,
            featureidkey='properties.ST_NM',
            locations='State',
            color='Transaction_amount',
            color_continuous_scale='Rainbow',  # or any other color scale
        )
        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig, use_container_width=True)


        bottom_states = state_summary.tail(10).index.tolist()
        st.subheader("Quarterly Insurance Transaction Trends - Bottom 10 States")
        fig, ax = plt.subplots(figsize=(10, 6))
        for state in bottom_states:
            df = Agg_Insurance[Agg_Insurance['State'] == state]
            df_grouped = df.groupby(['Year', 'Quarter'])['Transaction_count'].sum().reset_index()
            df_grouped['Time'] = df_grouped['Year'].astype(str) + ' Q' + df_grouped['Quarter'].astype(str)
            ax.plot(df_grouped['Time'], df_grouped['Transaction_count'], label=state, marker='o')
        ax.set_xlabel("Quarter")
        ax.set_ylabel("Transaction Count")
        ax.legend()
        ax.grid(True)
        plt.xticks(rotation=45)
        st.pyplot(fig)


        growth_data = []
        for state in Agg_Insurance['State'].unique():
            df = Agg_Insurance[Agg_Insurance['State'] == state]
            df_grouped = df.groupby(['Year', 'Quarter'])['Transaction_count'].sum().reset_index()
            df_grouped = df_grouped.sort_values(by=['Year', 'Quarter'])

            if len(df_grouped) >= 2:
                start = df_grouped.iloc[0]['Transaction_count']
                end = df_grouped.iloc[-1]['Transaction_count']
                growth = ((end - start) / start * 100) if start > 0 else None
                growth_data.append((state, start, end, growth))

        growth_df = pd.DataFrame(growth_data, columns=['State', 'Start_Count', 'End_Count', 'Growth_Percent'])
        growth_df = growth_df.dropna().sort_values(by='Growth_Percent', ascending=False)
        top10_growth = growth_df.head(10)
        st.subheader("Top 10 Fastest Growing States in Insurance Transactions")
        fig, ax = plt.subplots(figsize=(7, 5))
        sns.barplot(x='Growth_Percent', y='State', data=top10_growth, palette='Greens_r', ax=ax)
        ax.set_xlabel("Growth Percentage (%)")
        ax.set_ylabel("State")
        plt.tight_layout()
        st.pyplot(fig)

        bottom10_growth = growth_df.tail(10)
        st.subheader("Bottom 10 States by Insurance Transaction Growth")
        fig2, ax2 = plt.subplots(figsize=(7, 5))
        sns.barplot(x='Growth_Percent', y='State', data=bottom10_growth, palette='Reds', ax=ax2)
        ax2.set_xlabel("Growth Percentage (%)")
        ax2.set_ylabel("State")
        plt.tight_layout()
        st.pyplot(fig2)

    
    with tab4:
        st.header("Analysis 4: Transaction Analysis for Market Expansion")

        Map_Trans=pd.read_csv('C:/Users/rakes/Documents/sajinapython/phonepe/my_data7')
        geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        india_states = requests.get(geojson_url).json()
        st.subheader(' Transaction Amount by States')
        fig = px.choropleth(
            Map_Trans,
            geojson=india_states,
            featureidkey='properties.ST_NM',
            locations='State',
            color='Transaction_amount',
            color_continuous_scale='Rainbow',  # or any other color scale
        )
        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig, use_container_width=True)
        
        
        
        state_summary = Map_Trans.groupby('State').agg({
            'Transaction_count': 'sum',
            'Transaction_amount': 'sum'
        }).reset_index()
        state_summary = state_summary.sort_values(by='Transaction_amount', ascending=False)
        st.subheader("Top 10 States by Total Transaction Amount")
        fig, ax = plt.subplots(figsize=(7, 5))
        sns.barplot(data=state_summary.head(10), x='Transaction_amount', y='State', palette='viridis', ax=ax)
        ax.set_xlabel('Transaction Amount (₹)')
        ax.set_ylabel('State')
        st.pyplot(fig)

        annual_summary = Map_Trans.groupby(['State', 'Year']).agg({
            'Transaction_count': 'sum',
            'Transaction_amount': 'sum'
        }).reset_index()

        annual_summary = annual_summary.sort_values(by=['State', 'Year'])

        annual_summary['Transaction_amount_YoY_growth'] = annual_summary.groupby('State')['Transaction_amount'].pct_change() * 100

        # Latest year growth
        latest_year = annual_summary['Year'].max()
        growth_latest_year = annual_summary[annual_summary['Year'] == latest_year]
        growth_latest_year = growth_latest_year.sort_values(by='Transaction_amount_YoY_growth', ascending=False)
        latest_year = annual_summary['Year'].max()
        growth_latest_year = annual_summary[annual_summary['Year'] == latest_year]
        growth_latest_year = growth_latest_year.sort_values(by='Transaction_amount_YoY_growth', ascending=False)
        st.subheader('Top 10 States by Transaction Amount YoY Growth in 2024')
        fig, ax = plt.subplots(figsize=(7, 5))
        sns.barplot(
            data=growth_latest_year.head(10),
            x='Transaction_amount_YoY_growth',
            y='State',
            palette='coolwarm',
            ax=ax
        )
        ax.set_xlabel('YoY Growth (%)')
        ax.set_ylabel('State')
        st.pyplot(fig)

        median_amount = growth_latest_year['Transaction_amount'].median()
        potential_states = growth_latest_year[
            (growth_latest_year['Transaction_amount'] < median_amount) &
            (growth_latest_year['Transaction_amount_YoY_growth'] > 10)
        ]
        st.subheader('Potential States for Market Expansion (Low Amount, High Growth)')
        fig, ax = plt.subplots(figsize=(7, 5))
        sns.barplot(data=potential_states, x='Transaction_amount_YoY_growth', y='State', palette='magma', ax=ax)
        ax.set_xlabel('YoY Growth (%)')
        ax.set_ylabel('State')

        st.pyplot(fig)


    with tab5:
        st.header("Analysis 5: User Engagement and Growth Strategy")
        Map_User=pd.read_csv('C:/Users/rakes/Documents/sajinapython/phonepe/mydata8')
        st.subheader('Total Registered Users by State')
        state_summary = Map_User.groupby('State')[['Registered_user', 'Appopen_count']].sum().sort_values(by='Registered_user', ascending=False)
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x=state_summary.index, y=state_summary['Registered_user'], ax=ax)
        ax.set_xlabel('State')
        ax.set_ylabel('Registered Users')
        plt.xticks(rotation=90)
        st.pyplot(fig)

            

        top_states = state_summary.head(10).index
        st.subheader('Quarterly Registered Users Trend - Top 10 States')
        fig, ax = plt.subplots(figsize=(10, 6))
        for state in top_states:
            df = Map_User[Map_User['State'] == state].groupby(['Year', 'Quarter'])[['Registered_user']].sum().reset_index()
            df['Time'] = df['Year'].astype(str) + ' Q' + df['Quarter'].astype(str)
            ax.plot(df['Time'], df['Registered_user'], label=state)
        ax.set_xlabel('Time')
        ax.set_ylabel('Registered Users')
        plt.xticks(rotation=45)
        ax.legend()
        st.pyplot(fig)


        Map_User['Engagement_Ratio'] = Map_User['Appopen_count'] / Map_User['Registered_user']
        Map_User.replace([float('inf'), -float('inf')], pd.NA, inplace=True)
        Map_User.dropna(subset=['Engagement_Ratio'], inplace=True)
        engagement_ratio = Map_User.groupby('State')['Engagement_Ratio'].mean().sort_values(ascending=False)
        st.subheader('Top 10 States by Average User Engagement Ratio')
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x=engagement_ratio.head(10).index, y=engagement_ratio.head(10).values, ax=ax)
        ax.set_ylabel('Engagement Ratio (App Opens / Registered Users)')
        ax.set_xlabel('State')
        plt.xticks(rotation=90)
        st.pyplot(fig)

        district_data = Map_User[Map_User['State'] == 'Maharashtra'].groupby('District')[['Registered_user', 'Appopen_count']].sum().sort_values(by='Registered_user', ascending=False)
        st.subheader('Districts in Maharashtra by Registered Users')
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x=district_data.index, y=district_data['Registered_user'], ax=ax)
        ax.set_ylabel('Registered Users')
        ax.set_xlabel('District')
        plt.xticks(rotation=90)
        st.pyplot(fig)


        
        

