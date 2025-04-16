#!/usr/bin/env python3

import os
import json
import sys
from flask import Flask, render_template, abort, request, jsonify

# Add the project root to the path so we can import from scripts
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = Flask(__name__)

# Configure the app
app.config['SECRET_KEY'] = 'mtg-inventory-manager-secret'
app.config['DATA_DIR'] = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))

def load_secret_lairs():
    """Load Secret Lair data from JSON file"""
    try:
        with open(os.path.join(app.config['DATA_DIR'], 'secret_lairs.json'), 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        app.logger.error(f"Failed to load Secret Lair data: {e}")
        return []

@app.route('/')
def index():
    """Home page"""
    secret_lairs = load_secret_lairs()
    return render_template('index.html', secret_lairs=secret_lairs)

@app.route('/secret-lair/<drop_number>')
def secret_lair_detail(drop_number):
    """Detail page for a specific Secret Lair drop"""
    secret_lairs = load_secret_lairs()
    
    # Find the Secret Lair drop with the given drop number
    secret_lair = next((drop for drop in secret_lairs if drop['drop_number'] == drop_number), None)
    
    if not secret_lair:
        abort(404)
    
    return render_template('detail.html', secret_lair=secret_lair)

@app.route('/api/secret-lairs')
def api_secret_lairs():
    """API endpoint for Secret Lair data"""
    secret_lairs = load_secret_lairs()
    return jsonify(secret_lairs)

@app.route('/api/secret-lair/<drop_number>')
def api_secret_lair_detail(drop_number):
    """API endpoint for a specific Secret Lair drop"""
    secret_lairs = load_secret_lairs()
    
    # Find the Secret Lair drop with the given drop number
    secret_lair = next((drop for drop in secret_lairs if drop['drop_number'] == drop_number), None)
    
    if not secret_lair:
        abort(404)
    
    return jsonify(secret_lair)

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.context_processor
def utility_processor():
    """Add utility functions to templates"""
    def format_price(price):
        """Format a price as a string with two decimal places"""
        if price is None:
            return "N/A"
        try:
            return f"${float(price):.2f}"
        except (ValueError, TypeError):
            return "N/A"
    
    return dict(format_price=format_price)

if __name__ == '__main__':
    app.run(debug=True)
