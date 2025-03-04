import gradio as gr
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def process_file(file):
    # Read the uploaded file
    if file.name.endswith('.csv'):
        df = pd.read_csv(file.name)
    elif file.name.endswith(('.xlsx', '.xls')):
        df = pd.read_excel(file.name)
    else:
        return None

    # Convert datetime column to datetime type
    df['date'] = pd.to_datetime(df['date'])

    # Calculate daily mean speed
    daily_mean = df.groupby(df['date'].dt.date)['speed'].mean().reset_index()
    daily_mean['date'] = pd.to_datetime(daily_mean['date'])
    
    # Create a line plot using seaborn
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.lineplot(data=daily_mean, x='date', y='speed', ax=ax)
    ax.set_title("Daily Mean Speed Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Speed")
    plt.xticks(rotation=45)
    
    return fig

# Create Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("## Daily Mean Speed Plot")
    gr.Markdown("Upload a CSV or Excel file with 'date' and 'speed' columns")
    
    file_input = gr.File(label="Upload File", file_types=[".csv", ".xlsx", ".xls"])
    plot_output = gr.Plot()
    
    file_input.change(fn=process_file, inputs=file_input, outputs=plot_output)

# Launch the interface
demo.launch()
