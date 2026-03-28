import os
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from sklearn.ensemble import IsolationForest

DATA_PATH = os.path.join('..', 'data', 'metrics.csv')

st.set_page_config(page_title='Cloud Cost Intelligence', layout='wide')
st.title('Cloud Cost Intelligence Console (Simulated)')

st.markdown('This dashboard demonstrates live telemetry + anomaly detection + action suggestions.\n'
            'No account credentials are required for local simulation, but the code includes integration hooks for AWS/GCP.')

if not os.path.exists(DATA_PATH):
    st.warning('No metrics CSV found at ' + DATA_PATH +
               '. Please run collector first or provide data.')
    st.stop()

# Read and normalize data
raw = pd.read_csv(DATA_PATH, header=None, names=['Timestamp', 'Value', 'Unit'])
raw['Timestamp'] = pd.to_datetime(raw['Timestamp'], errors='coerce')
raw = raw.dropna(subset=['Timestamp', 'Value']).sort_values(
    'Timestamp').reset_index(drop=True)

# Compute cost utility values (simulated)
COST_PER_CPU_UNIT = 0.0025  # USD per 5m aggregated point (example)
raw['EstimatedCost'] = raw['Value'] * COST_PER_CPU_UNIT

st.subheader('Live Usage / Billing Data')
col1, col2, col3 = st.columns(3)
col1.metric('Data points', len(raw))
col2.metric('Total estimated cost ($)', f"{raw['EstimatedCost'].sum():.4f}")
col3.metric('Latest Utilization (%)', f"{raw['Value'].iloc[-1]:.2f}")

fig = px.line(raw, x='Timestamp', y='Value',
              title='CPU Utilization (%) over Time', markers=True)
fig.update_layout(yaxis=dict(title='CPU Utilization (%)'),
                  xaxis=dict(title='Timestamp'))
st.plotly_chart(fig, use_container_width=True)

# Anomaly detection
n_anoms = st.slider('IsolationForest contamination (anomaly ratio)',
                    min_value=0.001, max_value=0.2, value=0.03, step=0.001)
model = IsolationForest(contamination=n_anoms, random_state=42)
raw['anomaly_flag'] = model.fit_predict(raw[['Value']])
raw['is_anomaly'] = raw['anomaly_flag'] == -1

anomaly_count = raw['is_anomaly'].sum()
st.subheader(f'Anomaly Detection (detected {anomaly_count} anomalies)')

anom_fig = px.scatter(raw, x='Timestamp', y='Value', color='is_anomaly',
                      title='Anomalous Resource Usage',
                      labels={'is_anomaly': 'Anomaly'})
st.plotly_chart(anom_fig, use_container_width=True)

st.subheader('Anomaly Events')
st.dataframe(raw[raw['is_anomaly']].head(20))

st.subheader('Optimization Actions')
optimize_ec2 = st.button('Simulate Scale-down EC2/Shrink Instance')
optimize_storage = st.button('Simulate Storage Cleanup / Lifecycle')
optimize_serverless = st.button('Simulate Serverless Idle Function Pause')


def log_action(action, details):
    os.makedirs('logs', exist_ok=True)
    with open('logs/actions.log', 'a', encoding='utf-8') as f:
        f.write(f"{pd.Timestamp.now()} - {action} - {details}\n")


if optimize_ec2:
    log_action('SCALE_DOWN_EC2',
               'Would call AWS SDK: ec2.modify_instance_attribute or autoscaling scale-in')
    st.success('EC2 scale-down optimization action logged (simulation).')
if optimize_storage:
    log_action('STORAGE_LIFECYCLE',
               'Would call AWS/GCP storage lifecycle policy API for old object cleanup')
    st.success('Storage optimization action logged (simulation).')
if optimize_serverless:
    log_action('SERVERLESS_IDLE',
               'Would call lambda/gcp cloud functions disable at low usage windows')
    st.success('Serverless optimization action logged (simulation).')

st.markdown('---')
st.write('Integration hooks (add your own keys):')
st.code('''
import boto3
from google.cloud import monitoring_v3

# AWS
aws_client = boto3.client('cloudwatch', region_name='us-west-2')
# GCP
# gcp_client = monitoring_v3.MetricServiceClient()
''')

st.info('For real provisioning, run this app in an environment with AWS/GCP credentials and implement the Cloud API calls as shown in the code comments.')
