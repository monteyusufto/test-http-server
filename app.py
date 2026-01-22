from flask import Flask, request, send_from_directory, redirect, url_for, abort
import html
import os
import time
from urllib.parse import quote
from werkzeug.utils import secure_filename, safe_join

app = Flask(__name__)

# Set the directory for file uploads
UPLOAD_FOLDER = '/app/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def format_size(num_bytes):
    size = float(num_bytes)
    units = ["B", "KB", "MB", "GB", "TB"]
    for unit in units:
        if size < 1024.0 or unit == units[-1]:
            if unit == "B":
                return f"{int(size)} {unit}"
            text = f"{size:.1f}".rstrip("0").rstrip(".")
            return f"{text} {unit}"
        size /= 1024.0

def format_mtime(epoch_seconds):
    return time.strftime("%Y-%m-%d %H:%M", time.localtime(epoch_seconds))

def extract_filename_from_disposition(value):
    if not value:
        return None
    parts = value.split(";")
    for part in parts:
        part = part.strip()
        if part.lower().startswith("filename="):
            name = part.split("=", 1)[1].strip().strip('"')
            return name or None
    return None

def choose_upload_filename(explicit_name=None):
    if explicit_name:
        return explicit_name

    for key in ("filename", "name", "file"):
        value = request.args.get(key)
        if value:
            return value

    for header_name in ("X-Filename", "X-File-Name"):
        value = request.headers.get(header_name)
        if value:
            return value

    disposition = request.headers.get("Content-Disposition")
    value = extract_filename_from_disposition(disposition)
    if value:
        return value

    if request.files:
        for item in request.files.values():
            if item and item.filename:
                return item.filename

    return f"upload_{int(time.time())}.bin"

def save_uploaded_content(filename):
    safe_name = secure_filename(filename) or f"upload_{int(time.time())}.bin"
    target_path = os.path.join(app.config["UPLOAD_FOLDER"], safe_name)

    if request.files:
        file_obj = request.files.get("file")
        if not file_obj:
            for item in request.files.values():
                file_obj = item
                break
        if file_obj:
            file_obj.save(target_path)
            return safe_name

    data = request.get_data()
    if not data:
        return None
    with open(target_path, "wb") as handle:
        handle.write(data)
    return safe_name

def list_uploaded_files():
    files = []
    for name in os.listdir(app.config['UPLOAD_FOLDER']):
        path = os.path.join(app.config['UPLOAD_FOLDER'], name)
        if os.path.isfile(path):
            stat = os.stat(path)
            files.append(
                {"name": name, "size": stat.st_size, "mtime": stat.st_mtime}
            )
    files.sort(key=lambda item: item["mtime"], reverse=True)
    return files

def render_page(files, message=None, error=None):
    if files:
        rows = []
        for item in files:
            name = item["name"]
            safe_name = html.escape(name)
            url_name = quote(name)
            size = format_size(item["size"])
            mtime = format_mtime(item["mtime"])
            rows.append(
                f'''
                <tr>
                  <td class="name"><a href="/uploads/{url_name}">{safe_name}</a></td>
                  <td>{size}</td>
                  <td>{mtime}</td>
                  <td class="actions">
                    <form method="post" action="/delete/{url_name}" onsubmit="return confirm('Delete {safe_name}?');">
                      <button type="submit">Delete</button>
                    </form>
                  </td>
                </tr>
                '''
            )
        file_rows = "\n".join(rows)
        table = f'''
        <table>
          <thead>
            <tr>
              <th>File</th>
              <th>Size</th>
              <th>Modified</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {file_rows}
          </tbody>
        </table>
        '''
    else:
        table = '<p class="empty">No files yet.</p>'

    notice = ""
    if message:
        notice = f'<div class="notice success">{html.escape(message)}</div>'
    if error:
        notice = f'<div class="notice error">{html.escape(error)}</div>'

    return f'''
    <!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>File Upload</title>
      <style>
        body {{
          font-family: Arial, sans-serif;
          margin: 24px;
          color: #222;
          background: #f7f7f7;
        }}
        main {{
          max-width: 900px;
          margin: 0 auto;
          background: #fff;
          padding: 20px;
          border: 1px solid #ddd;
          border-radius: 8px;
        }}
        h1 {{
          margin: 0 0 12px;
          font-size: 22px;
        }}
        form.upload {{
          display: flex;
          gap: 12px;
          align-items: center;
          margin-bottom: 16px;
        }}
        input[type="file"] {{
          flex: 1;
        }}
        button {{
          padding: 6px 12px;
          cursor: pointer;
        }}
        .notice {{
          padding: 8px 12px;
          border-radius: 6px;
          margin: 12px 0;
        }}
        .notice.success {{
          background: #e6f4ea;
          border: 1px solid #b6e0c2;
          color: #1f6d3a;
        }}
        .notice.error {{
          background: #fde8e7;
          border: 1px solid #f2c4c0;
          color: #8c2c26;
        }}
        table {{
          width: 100%;
          border-collapse: collapse;
        }}
        th, td {{
          text-align: left;
          padding: 8px;
          border-bottom: 1px solid #eee;
        }}
        th {{
          font-weight: 600;
          background: #fafafa;
        }}
        td.actions {{
          width: 1%;
          white-space: nowrap;
        }}
        .empty {{
          color: #666;
          margin-top: 12px;
        }}
        a {{
          color: #0b5bd3;
          text-decoration: none;
        }}
        a:hover {{
          text-decoration: underline;
        }}
      </style>
    </head>
    <body>
      <main>
        <h1>File Upload</h1>
        <form class="upload" method="post" enctype="multipart/form-data">
          <input type="file" name="file" required>
          <button type="submit">Upload</button>
        </form>
        {notice}
        <h2>Files ({len(files)})</h2>
        {table}
        <p class="empty">Direct list: /uploads/</p>
      </main>
    </body>
    </html>
    '''

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(url_for('upload_file', error='No file part'))
        file = request.files['file']
        if file.filename == '':
            return redirect(url_for('upload_file', error='No selected file'))
        if file:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            return redirect(url_for('upload_file', message=f'Uploaded {file.filename}'))
    files = list_uploaded_files()
    message = request.args.get('message')
    error = request.args.get('error')
    return render_page(files, message=message, error=error)

@app.route('/uploads', methods=['GET', 'POST', 'PUT'])
@app.route('/uploads/', methods=['GET', 'POST', 'PUT'])
def list_or_upload():
    if request.method in ('POST', 'PUT'):
        filename = choose_upload_filename()
        saved = save_uploaded_content(filename)
        if not saved:
            abort(400, description="No upload content received")
        return f'File {saved} uploaded successfully'
    files = list_uploaded_files()
    return render_page(files)

@app.route('/uploads/<filename>', methods=['GET', 'POST', 'PUT'])
def download_or_upload_file(filename):
    if request.method in ('POST', 'PUT'):
        saved = save_uploaded_content(filename)
        if not saved:
            abort(400, description="No upload content received")
        return f'File {saved} uploaded successfully'
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/delete/<filename>', methods=['POST', 'DELETE'])
def delete_file(filename):
    path = safe_join(app.config['UPLOAD_FOLDER'], filename)
    if not path:
        abort(400, description="Invalid filename")
    if not os.path.isfile(path):
        abort(404, description="File not found")
    os.remove(path)
    if request.method == 'DELETE':
        return f'File {filename} deleted'
    return redirect(url_for('upload_file', message=f'Deleted {filename}'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
