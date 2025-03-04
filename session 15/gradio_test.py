
from windrose import WindroseAxes
import numpy as np
import io
import base64
import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt


def read_data(file):
    if file.name.endswith('.csv'):
        data = pd.read_csv(file)
    elif file.name.endswith('.xlsx'):
        data = pd.read_excel(file)
    else:
        raise ValueError("Unsupported file format. Please upload a CSV or Excel file.")
    return data


def plot_wind_rose(data):
    fig = plt.figure(figsize=(8, 8))
    ax = WindroseAxes.from_ax(fig=fig)
    ax.bar(data['direction'], data['speed'], normed=True, opening=0.8, edgecolor='white')
    ax.set_legend(title='Wind Speed (m/s)')
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)

    return f'<img src="data:image/png;base64,{img_str}"/>'



def process_file(file):
    data = read_data(file)
    return plot_wind_rose(data)

# Gradio Interface
demo = gr.Interface(
    fn=process_file,
    inputs=gr.File(file_types=['.csv', '.xlsx']),
    outputs="html",
    title="Wind Rose Plotter",
    description="Upload a CSV or Excel file containing 'direction' and 'speed' columns to generate a wind rose plot."
)

demo.launch()
