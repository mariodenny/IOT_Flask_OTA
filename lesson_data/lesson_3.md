# Lesson 3: Building the Flask API

Our Flask server needs to respond to the ESP32 when it asks for the latest firmware.

We use **raw SQL** with `mysql-connector-python` to talk to our database.

## The Database
We have a table called `firmware`:
- `id`: Unique number
- `version`: Like "1.0.1"
- `filename`: Like "esp32_1.0.1.bin"
- `device_type`: Like "esp32"
- `uploaded_at`: The time it was uploaded

## The API Route
When the ESP32 goes to `http://OUR_IP:5000/api/firmware/latest`, this Python code runs:

```python
@bp.route('/api/firmware/latest', methods=['GET'])
def get_latest_firmware():
    # 1. Connect to MySQL
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    # 2. Ask MySQL for the newest firmware for esp32
    cursor.execute(
        "SELECT * FROM firmware WHERE device_type = 'esp32' ORDER BY uploaded_at DESC LIMIT 1"
    )
    latest = cursor.fetchone()
    
    # 3. Clean up
    cursor.close()
    db.close()
    
    if not latest:
        return jsonify({"error": "No firmware found"}), 404
        
    # 4. Reply with JSON
    return jsonify({
        "version": latest['version'],
        "url": "http://OUR_IP:5000/static/firmware/" + latest['filename']
    })
```

The ESP32 reads this JSON reply to decide what to do!
