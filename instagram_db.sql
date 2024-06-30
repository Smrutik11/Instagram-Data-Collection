CREATE DATABASE instagram_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE instagram_db;

CREATE TABLE IF NOT EXISTS instagram_posts (
    post_id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255),
    timestamp DATETIME,
    content TEXT,
    likes INT,
    shares INT
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

