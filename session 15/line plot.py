import gradio as gr
import pandas as pd

def load_data(file):
    if file.name.endswith('.csv'):
        df = pd.read_csv(file.name)
    elif file.name.endswith('.xlsx'):
        df = pd.read_excel(file.name)
    else:
        raise ValueError("Unsupported file format")
    return df

def plot_data(file):
    df = load_data(file)
    return gr.LinePlot(df, x="date", y="speed")

with gr.Blocks() as demo:
    file_input = gr.File(label="Upload CSV or Excel file")
    plot_output = gr.Plot()
    
    file_input.change(fn=plot_data, inputs=file_input, outputs=plot_output)

demo.launch()