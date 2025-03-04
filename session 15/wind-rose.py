from windrose import WindroseAxes
import numpy as np
import io
import base64
import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
def save_wind_rose(data, filename='wind_rose', format='png', dpi=300):
    """
    Save wind rose plot to a file in the specified format.
    
    Args:
        data (pd.DataFrame): DataFrame containing wind data
        filename (str): Output filename (without extension)
        format (str): Output format - 'png', 'jpg', 'svg' (default: 'png')
        dpi (int): Resolution for raster formats (default: 300)
    """
    # Create figure and windrose axes
    fig = plt.figure(figsize=(8, 8))
    ax = WindroseAxes.from_ax(fig=fig)
    
    # Plot wind rose
    ax.bar(data['direction'], data['speed'], normed=True, opening=0.8, edgecolor='white')
    ax.set_legend(title='Wind Speed (m/s)')
    
    # Save figure
    output_file = f"{filename}.{format}"
    if format in ['png', 'jpg']:
        plt.savefig(output_file, format=format, dpi=dpi, bbox_inches='tight')
    elif format == 'svg':
        plt.savefig(output_file, format=format, bbox_inches='tight')
    else:
        raise ValueError("Unsupported format. Please use 'png', 'jpg', or 'svg'")
    
    plt.close(fig)
    return output_file



def read_data(file):
    if file.name.endswith('.csv'):
        data = pd.read_csv(file)
    elif file.name.endswith('.xlsx'):
        data = pd.read_excel(file)
    else:
        raise ValueError("Unsupported file format. Please upload a CSV or Excel file.")
    return data


def plot_wind_rose(data):
    # Create figure and windrose axes
    fig = plt.figure(figsize=(8, 8))
    ax = WindroseAxes.from_ax(fig=fig)
    
    # Plot wind rose
    ax.bar(data['direction'], data['speed'], normed=True, opening=0.8, edgecolor='white')
    ax.set_legend(title='Wind Speed (m/s)')
    
    # Convert plot to base64 string for Gradio HTML output
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)

    return f'<img src="data:image/png;base64,{img_str}"/>'

def process_file(file, format='png', dpi=300):
    data = read_data(file)
    image_path = save_wind_rose(data, format=format, dpi=dpi)
    return plot_wind_rose(data)




# Create Gradio interface
demo = gr.Interface(
    fn=process_file,
    inputs=gr.File(file_types=['.csv', '.xlsx']),
    outputs="html",
    title="Wind Rose Plot Generator",
    description="Upload a CSV or Excel file with 'date', 'speed', and 'direction' columns to generate a wind rose plot. The plot shows wind speed distribution across different directions."
)

# Launch the interface
demo.launch()
