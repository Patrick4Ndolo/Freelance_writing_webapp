from flask import render_template
from myapp import app, db

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404-error-page.html'), 404

@app.errorhandler
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500