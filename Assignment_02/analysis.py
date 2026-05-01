import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def load_and_clean_data(file_path):
    df = pd.read_csv(file_path)
    
    # Convert TotalCharges to numeric, handling empty strings
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df.dropna(subset=['TotalCharges'], inplace=True)
    
    # Convert SeniorCitizen to more readable format
    df['SeniorCitizen'] = df['SeniorCitizen'].map({1: 'Yes', 0: 'No'})
    return df

def get_churn_metrics(df):
    total_customers = len(df)
    churn_count = len(df[df['Churn'] == 'Yes'])
    churn_rate = (churn_count / total_customers) * 100
    return total_customers, churn_count, churn_rate

def plot_churn_by_contract(df):
    fig = px.histogram(df, x="Contract", color="Churn", barmode="group",
                       title="Churn Count by Contract Type",
                       color_discrete_map={'Yes': '#EF553B', 'No': '#636EFA'})
    return fig

def plot_tenure_vs_churn(df):
    fig = px.box(df, x="Churn", y="tenure", points="all",
                 title="Tenure Distribution by Churn Status",
                 color="Churn",
                 color_discrete_map={'Yes': '#EF553B', 'No': '#636EFA'})
    return fig

def plot_payment_method_churn(df):
    churn_df = df[df['Churn'] == 'Yes']
    fig = px.pie(churn_df, names='PaymentMethod', 
                 title='Churn Distribution by Payment Method',
                 hole=0.4)
    return fig
