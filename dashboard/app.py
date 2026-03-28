import os
import matplotlib.pyplot as plt
from flask import Flask, render_template
import pandas as pd
import matplotlib
matplotlib.use('Agg')

app = Flask(__name__)


@app.route("/")
def index():
    file_path = "../data/metrics.csv"
    if not os.path.exists(file_path):
        return "No data available yet. Please wait for data collection."
    df = pd.read_csv(file_path)
    df.columns = ['Timestamp', 'Value', 'Unit']
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    # Compute statistics
    stats = {
        'mean': df['Value'].mean(),
        'min': df['Value'].min(),
        'max': df['Value'].max(),
        'count': len(df)
    }

    # Plot
    plt.figure(figsize=(10, 5))
    plt.plot(df['Timestamp'], df['Value'], marker='o')
    plt.title('CPU Utilization Over Time')
    plt.xlabel('Time')
    plt.ylabel('CPU Utilization (%)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    os.makedirs("static", exist_ok=True)
    plt.savefig("static/graph.png")
    plt.close()

    return render_template("index.html", table=df.tail(10).to_html(index=False), graph="static/graph.png", stats=stats)


app.run(debug=True)
