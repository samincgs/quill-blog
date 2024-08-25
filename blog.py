from flask import Flask, render_template

app = Flask(__name__)

# dummy data
posts = [
    {
        'author': 'John Done',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'August 25, 2024',
    },
    {
        'author': 'Jane Smith',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 12, 2024',
    },
    {
        'author': 'Mary Jones',
        'title': 'Blog Post 3',
        'content': 'Third post content',
        'date_posted': 'December 3, 2023',
    },
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)