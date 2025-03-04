from windrose import WindroseAxes
import numpy as np
import io
import base64
import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt

def save_wind_rose(data, format='png', dpi=300):
    """
    Save wind rose plot and return the file path.
    
    Args:
        data (pd.DataFrame): DataFrame containing wind data.
        format (str): Output format - 'png', 'jpg', 'svg' (default: 'png').
        dpi (int): Resolution for raster formats (default: 300).
        
    Returns:
        str: Path to the saved wind rose image.
    """
    filename = f"wind_rose.{format}"
    
    # Create figure and windrose axes
    fig = plt.figure(figsize=(8, 8))
    ax = WindroseAxes.from_ax(fig=fig)
    
    # Plot wind rose
    ax.bar(data['direction'], data['speed'], normed=True, opening=0.8, edgecolor='white')
    ax.set_legend(title='Wind Speed (m/s)')
    
    # Save figure
    if format in ['png', 'jpg']:
        plt.savefig(filename, format=format, dpi=dpi, bbox_inches='tight')
    elif format == 'svg':
        plt.savefig(filename, format=format, bbox_inches='tight')
    else:
        raise ValueError("Unsupported format. Please use 'png', 'jpg', or 'svg'")
    
    plt.close(fig)
    return filename

def read_data(file):
    if file.name.endswith('.csv'):
        data = pd.read_csv(file)
    elif file.name.endswith('.xlsx'):
        data = pd.read_excel(file)
    else:
        raise ValueError("Unsupported file format. Please upload a CSV or Excel file.")
    return data

def process_file(file, format):
    data = read_data(file)
    image_path = save_wind_rose(data, format)
    return image_path

# Create Gradio interface
demo = gr.Interface(
    fn=process_file,
    inputs=[
        gr.File(file_types=['.csv', '.xlsx']),
        gr.Radio(["png", "jpg", "svg"], label="Select Output Format", value="png")
    ],
    outputs=gr.File(label="Download Wind Rose"),
    title="Wind Rose Plot Generator",
    description="Upload a CSV or Excel file with 'speed' and 'direction' columns to generate and download a wind rose plot."
)

# Launch the interface
demo.launch()
