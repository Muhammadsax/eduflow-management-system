import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from eduflow_app import create_app

app = create_app()

@app.route('/')
def home():
    return "🎉 EduFlow يعمل بنجاح!"

if __name__ == '__main__':
    app.run(debug=True)