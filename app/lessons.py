from flask import Blueprint, render_template, abort, current_app
import markdown
import os

bp = Blueprint('lessons', __name__)

def get_lesson_content(lesson_id):
    filepath = os.path.join(current_app.root_path, '../lesson_data', f'lesson_{lesson_id}.md')
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    return markdown.markdown(text, extensions=['fenced_code', 'codehilite'])

@bp.route('/')
def index():
    # Show list of lessons
    lessons = [
        {'id': 1, 'title': 'What is OTA?'},
        {'id': 2, 'title': 'ESP32 Wi-Fi & HTTP Basics'},
        {'id': 3, 'title': 'Building the Flask API'},
        {'id': 4, 'title': 'Uploading Firmware from a Browser'},
        {'id': 5, 'title': 'ESP32 OTA Update'},
        {'id': 6, 'title': 'Adding Login / Auth'},
        {'id': 7, 'title': 'Extending the System'},
        {'id': 8, 'title': 'Real-World OTA Examples'}
    ]
    return render_template('index.html', lessons=lessons)

@bp.route('/lesson/<int:lesson_id>')
def view_lesson(lesson_id):
    html_content = get_lesson_content(lesson_id)
    if not html_content:
        abort(404)
    return render_template('lesson.html', lesson_id=lesson_id, content=html_content)

@bp.route('/lesson/<int:lesson_id>/pdf')
def download_pdf(lesson_id):
    html_content = get_lesson_content(lesson_id)
    if not html_content:
        abort(404)
    
    # We replaced WeasyPrint with a simpler browser-based Print-to-PDF
    full_html = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Lesson {lesson_id}</title>
        <style>
            body {{ font-family: sans-serif; line-height: 1.6; color: #333; margin: 2rem; }}
            pre {{ background-color: #f4f4f4; color: #333; padding: 15px; border-radius: 5px; border: 1px solid #ddd; overflow-x: auto; }}
            code {{ font-family: monospace; background-color: #f4f4f4; padding: 2px 4px; border-radius: 3px; }}
            pre code {{ padding: 0; border: none; background: transparent; }}
            h1, h2, h3 {{ color: #2c3e50; }}
            /* Basic pygments style for code blocks */
            .c {{ color: #75715e }} /* Comment */
            .k {{ color: #007bff }} /* Keyword */
            .s {{ color: #d14 }} /* String */
            .nf {{ color: #900 }} /* Name.Function */
        </style>
        <script>
            window.onload = function() {{
                window.print();
            }};
        </script>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    '''
    
    return full_html
