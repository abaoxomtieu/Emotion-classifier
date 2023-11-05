from flask import Flask, render_template, request
from transformers import RobertaForSequenceClassification, AutoTokenizer
import torch
import plotly.express as px
from text_preprocessing import process_text
from markupsafe import Markup

app = Flask(__name__)

model_2 = RobertaForSequenceClassification.from_pretrained("save_weight_balance")
tokenizer = AutoTokenizer.from_pretrained("wonrax/phobert-base-vietnamese-sentiment", use_fast=False)

def predict_sentiment(text):
    inputs = tokenizer(text, padding=True, truncation=True, return_tensors='pt')
    outputs = model_2(**inputs)
    predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
    predictions = predictions.cpu().detach().numpy()
    return predictions[0]

def calculate_emotion_percentages(predictions):
    total_predictions = predictions.sum()
    percentages = (predictions / total_predictions) * 100
    return percentages

def map_position_to_label(position):
    label_mapping = {
        0: "Other",
        1: "Disgust🤮",
        2: "Enjoyment🥰",
        3: "Anger😡",
        4: "Surprise😮",
        5: "Sadness😔",
        6: "Fear🫣"
        # Add more mappings as needed
    }
    return label_mapping.get(position, "Unknown")

@app.route('/', methods=['GET', 'POST'])
def index():
    input_text = None
    preprocessed_text = None
    predicted_label = None
    formatted_percentages = None
    plotly_chart = None
    plotly_pie_chart = None
    selected_chart = 'bar'  # Thêm dòng này để mặc định là 'bar'

    if request.method == 'POST':
        input_text = request.form.get('text')
        if input_text:
            preprocessed_text = process_text(input_text)
            predictions = predict_sentiment(preprocessed_text)
            result_label = map_position_to_label(predictions.argmax())
            predicted_label = f"Predicted Emotion: {result_label}"
            
            # Calculate emotion percentages
            percentages = calculate_emotion_percentages(predictions)
            formatted_percentages = {label: percentage for label, percentage in zip(['Other', 
                                                                                     'Disgust🤮', 
                                                                                     'Enjoyment🥰', 
                                                                                     'Anger😡', 
                                                                                     'Surprise😮', 
                                                                                     'Sadness😔', 
                                                                                     'Fear🫣'], percentages)}
        
        # Handle chart selection
        if 'chart-select' in request.form:
            selected_chart = request.form['chart-type']  # Lưu giá trị của biểu đồ đã chọn
            if selected_chart == 'bar':
                bar_chart = px.bar(
                    x=list(formatted_percentages.values()),
                    y=list(formatted_percentages.keys()),
                    labels={'x': 'Probability'}
                )
                
                # Set the maximum range of x-axis to 100
                bar_chart.update_xaxes(range=[0, 100])
                
                # Update bar colors
                bar_chart.update_traces(marker=dict(color=['#1f77b4', 
                                                           '#ff7f0e', 
                                                           '#2ca02c', 
                                                           '#d62728', 
                                                           '#9467bd', 
                                                           '#8c564b', 
                                                           '#e377c2']))
                
                plotly_chart = Markup(bar_chart.to_html(full_html=False, include_plotlyjs='cdn'))
                plotly_pie_chart = None
            elif selected_chart == 'pie':
                pie_chart = px.pie(
                    names=list(formatted_percentages.keys()),
                    values=list(formatted_percentages.values()),
                    title='Emotion Percentages'
                )
                pie_chart.update_traces(textinfo='percent+label')
                plotly_pie_chart = Markup(pie_chart.to_html(full_html=False, include_plotlyjs='cdn'))
                plotly_chart = None

    return render_template(
        'index.html',
        input_text=input_text,
        preprocessed_text=preprocessed_text,
        predicted_label=predicted_label,
        plotly_chart=plotly_chart,
        plotly_pie_chart=plotly_pie_chart,
        selected_chart=selected_chart  # Truyền giá trị selected_chart để hiển thị lựa chọn biểu đồ
    )

if __name__ == '__main__':
    app.run(debug=True)
