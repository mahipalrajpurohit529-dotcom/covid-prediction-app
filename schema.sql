-- =============================================
-- DATABASE SCHEMA FOR FLASK ML WEB APPLICATION
-- =============================================

-- Create and select the database
CREATE DATABASE IF NOT EXISTS ml_app;
USE ml_app;

-- -------------------------
-- TABLE 1: users
-- Stores registered user accounts
-- -------------------------
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL
);

-- -------------------------
-- TABLE 2: predictions
-- Stores ML prediction results linked to users
-- -------------------------
CREATE TABLE predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    age INT,
    gender VARCHAR(10),
    fever INT,
    cough VARCHAR(10),
    city VARCHAR(100),
    result VARCHAR(100),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- -------------------------
-- TABLE 3: services
-- Stores service booking requests
-- -------------------------
CREATE TABLE services (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    service VARCHAR(200),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- -------------------------
-- TABLE 4: messages
-- Stores contact form messages
-- -------------------------
CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    message TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
