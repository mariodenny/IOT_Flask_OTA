import os
import time
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, current_app, send_from_directory
from flask_login import login_required
from werkzeug.utils import secure_filename
from app.db import get_db

bp = Blueprint('firmware', __name__)

@bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    if request.method == 'POST':
        version = request.form.get('version')
        device_type = request.form.get('device_type', 'esp32')
        file = request.files.get('file')
        
        if not version or not file or file.filename == '':
            flash('No file selected or version missing.', 'danger')
            return redirect(request.url)
            
        if not file.filename.endswith('.bin'):
            flash('Only .bin files are allowed for firmware.', 'danger')
            return redirect(request.url)
            
        filename = secure_filename(f"{device_type}_{version}_{int(time.time())}.bin")
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        cursor.execute(
            "INSERT INTO firmware (version, filename, device_type) VALUES (%s, %s, %s)",
            (version, filename, device_type)
        )
        db.commit()
        flash('Firmware uploaded successfully!', 'success')
        return redirect(url_for('firmware.upload'))
        
    cursor.execute("SELECT * FROM firmware ORDER BY uploaded_at DESC")
    firmwares = cursor.fetchall()
    cursor.close()
    db.close()
    
    return render_template('upload.html', firmwares=firmwares)

@bp.route('/api/firmware/latest', methods=['GET'])
def get_latest_firmware():
    device_type = request.args.get('device', 'esp32')
    
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM firmware WHERE device_type = %s ORDER BY uploaded_at DESC LIMIT 1",
        (device_type,)
    )
    latest = cursor.fetchone()
    cursor.close()
    db.close()
    
    if not latest:
        return jsonify({"error": "No firmware found"}), 404
        
    # Build full URL for the binary - FIXED: removed /static and correct path
    download_url = request.host_url.rstrip('/') + f"/firmware/download/{latest['filename']}"
    
    return jsonify({
        "version": latest['version'],
        "url": download_url,
        "device_type": latest['device_type']
    })

# NEW: Route to serve firmware files (without 'static' in URL)
@bp.route('/firmware/download/<filename>')
def download_firmware(filename):
    """Serve firmware files from UPLOAD_FOLDER"""
    return send_from_directory(
        current_app.config['UPLOAD_FOLDER'], 
        filename, 
        as_attachment=True
    )

# Optional: If you also want a direct route without 'download' in path
@bp.route('/firmware/<filename>')
def serve_firmware(filename):
    """Alternative: serve firmware without /download/ in URL"""
    return send_from_directory(
        current_app.config['UPLOAD_FOLDER'], 
        filename, 
        as_attachment=True
    )