# Lesson 4: Uploading Firmware from a Browser

How does the `.bin` file get onto our server in the first place? We upload it using a web browser!

## HTML Forms
We use HTML to create a form. The user types the version number and selects the file from their computer.

```html
<form action="/upload" method="POST" enctype="multipart/form-data">
    <input type="text" name="version" required>
    <input type="file" name="file" accept=".bin" required>
    <button type="submit">Upload</button>
</form>
```
*Note: `enctype="multipart/form-data"` is required when uploading files.*

## Handling the Upload in Python
When the user clicks "Upload", Flask receives the file.

```python
@bp.route('/upload', methods=['POST'])
def upload():
    # 1. Get data from the form
    version = request.form.get('version')
    file = request.files.get('file')
    
    # 2. Save the file to our folder
    filename = secure_filename(f"esp32_{version}.bin")
    file.save("static/firmware/" + filename)
    
    # 3. Save the record in MySQL
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO firmware (version, filename) VALUES (%s, %s)",
        (version, filename)
    )
    db.commit()
    
    return "Uploaded successfully!"
```

By saving the record in the database, our API from Lesson 3 knows there is a new file!
