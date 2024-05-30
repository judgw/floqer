import openai
import pandas as pd
from flask import Flask, request, jsonify, render_template

# Initialize the Flask application
app = Flask(__name__)

# Load the spreadsheet data (ensure 'salaries.csv' exists)
df = pd.read_csv('salaries.csv')

# Set your OpenAI API key (replace with yours)
openai.api_key = 'sk-proj-QCr2IJAoqSz8R7WuQaOlT3BlbkFJfxZaZ0tapnW1jBHTbggE'  # Store securely

def query_llm(prompt, max_tokens=150):
  try:
    response = openai.completions.create(
        prompt=prompt,
        model="text-davinci-003",
        max_tokens=max_tokens
    )
    return response.choices[0].text.strip()
  except Exception as e:
    return f"An error occurred: {e}"

def generate_insight(query, df):
  # Include the first few rows of data in the prompt to give context
  data_preview = df.head().to_string()
  # Create a prompt that includes the user's query and the data preview
  prompt = f"Given the data:\n{data_preview}\n{query}"
  return query_llm(prompt)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
  user_input = request.json['user_input']
  response = generate_insight(user_input, df)
  return jsonify({'response': response})

if __name__ == '__main__':
  app.run(debug=True)