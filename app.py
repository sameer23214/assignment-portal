from flask import Flask, render_template, request, redirect, url_for, flash  # type: ignore
import re

app = Flask(__name__)
app.secret_key = 'devops-lab-secret'

# In-memory storage for submissions
submissions = []

def is_valid_url(url):
    regex = re.compile(
        r'^(https?://)?'  # http:// or https://
        r'([^\s$.?#].[^\s]*)$', re.IGNORECASE)
    return re.match(regex, url) is not None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        reg_number = request.form.get('reg_number', '').strip()
        title = request.form.get('title', '').strip()
        url = request.form.get('url', '').strip()

        # Validation rules
        if not name or not reg_number or not title or not url:
            flash('All fields are required.', 'danger')
            return redirect(url_for('index'))
        
        if not is_valid_url(url):
            flash('Invalid submission URL format.', 'danger')
            return redirect(url_for('index'))

        # Save valid submission
        submissions.append({
            'name': name,
            'reg_number': reg_number,
            'title': title,
            'url': url
        })
        flash('Assignment submitted successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('index.html', submissions=submissions)

if __name__ == '__main__':
    app.run(debug=True, port=5000)