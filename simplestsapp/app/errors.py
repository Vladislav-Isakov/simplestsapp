from app import app
from flask import render_template

@app.errorhandler(400)
def not_found_error_400(error):
    return render_template('error_400.html'), 400

@app.errorhandler(404)
def not_found_error_404(error):
    return render_template('error_404.html'), 404

@app.errorhandler(500)
def internal_error_500(error):
    return render_template('error_500.html'), 500