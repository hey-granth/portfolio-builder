# app.py
from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# Ensure the data directory exists
os.makedirs('data', exist_ok=True)

def save_portfolio_data(data):
    with open('data/portfolio.json', 'w') as f:
        json.dump(data, f)

def load_portfolio_data():
    try:
        with open('data/portfolio.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            'name': '',
            'title': '',
            'about': '',
            'skills': [],
            'projects': [],
            'contact': {'email': '', 'linkedin': '', 'github': ''}
        }

@app.route('/')
def index():
    portfolio_data = load_portfolio_data()
    return render_template('index.html', portfolio=portfolio_data)

@app.route('/edit')
def edit():
    portfolio_data = load_portfolio_data()
    return render_template('edit.html', portfolio=portfolio_data)

@app.route('/update', methods=['POST'])
def update():
    data = {
        'name': request.form['name'],
        'title': request.form['title'],
        'about': request.form['about'],
        'skills': request.form.getlist('skills'),
        'projects': [],
        'contact': {
            'email': request.form['email'],
            'linkedin': request.form['linkedin'],
            'github': request.form['github']
        }
    }

    # Handle projects
    project_titles = request.form.getlist('project_title')
    project_descriptions = request.form.getlist('project_description')
    project_links = request.form.getlist('project_link')

    for i in range(len(project_titles)):
        if project_titles[i]:  # Only add if title exists
            data['projects'].append({
                'title': project_titles[i],
                'description': project_descriptions[i],
                'link': project_links[i]
            })

    save_portfolio_data(data)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)