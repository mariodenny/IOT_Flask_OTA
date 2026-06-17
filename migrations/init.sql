CREATE DATABASE IF NOT EXISTS ota_flask_iot;
USE ota_flask_iot;

CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL
);

-- Insert default admin user if not exists
INSERT IGNORE INTO users (id, username, password) VALUES (1, 'admin', 'admin123');

CREATE TABLE IF NOT EXISTS firmware (
  id INT AUTO_INCREMENT PRIMARY KEY,
  version VARCHAR(20) NOT NULL,
  filename VARCHAR(255) NOT NULL,
  device_type VARCHAR(50) DEFAULT 'esp32',
  uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
