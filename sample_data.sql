-- Sample data for RoomieMatch app
-- This file contains SQL INSERT statements for sample users and profiles

-- Insert sample users (6 core profiles)
INSERT INTO users (username, email, password_hash) VALUES 
('alex_smith', 'alex@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J8Qz8K8K2'),
('maya_johnson', 'maya@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J8Qz8K8K2'),
('sam_wilson', 'sam@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J8Qz8K8K2'),
('jessica_brown', 'jessica@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J8Qz8K8K2'),
('mike_davis', 'mike@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J8Qz8K8K2'),
('sarah_miller', 'sarah@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J8Qz8K8K2');

-- Insert sample profiles (6 core profiles)
INSERT INTO user_profiles (user_id, name, age, budget, location, bio, interests, lifestyle_preferences) VALUES 
(2, 'Alex Smith', 22, 600, 'Downtown', 'Love music, gaming, and cooking! Looking for someone who enjoys late-night conversations and weekend adventures.', '["Music", "Gaming", "Cooking", "Movies"]', '["Night Owl", "Very Social", "Moderately Clean", "Love Pets"]'),
(3, 'Maya Johnson', 25, 750, 'Midtown', 'Fitness enthusiast and nature lover. Prefer quiet evenings with good books and early morning workouts.', '["Fitness", "Nature", "Reading", "Photography"]', '["Early Bird", "Quiet", "Very Clean", "Neutral"]'),
(4, 'Sam Wilson', 23, 650, 'Uptown', 'Artist and photographer. Love exploring the city and trying new restaurants. Need a creative space!', '["Art", "Photography", "Travel", "Cooking"]', '["Flexible", "Moderately Social", "Moderately Clean", "Love Pets"]'),
(5, 'Jessica Brown', 24, 700, 'Downtown', 'Tech professional who loves coding and gaming. Looking for someone who understands the developer lifestyle.', '["Technology", "Gaming", "Movies", "Music"]', '["Night Owl", "Moderately Social", "Moderately Clean", "Neutral"]'),
(6, 'Mike Davis', 26, 800, 'Midtown', 'Sports fanatic and outdoor enthusiast. Love hiking, basketball, and watching games with friends.', '["Sports", "Fitness", "Nature", "Travel"]', '["Early Bird", "Very Social", "Very Clean", "No Pets"]'),
(7, 'Sarah Miller', 21, 550, 'Uptown', 'Student studying art history. Love museums, galleries, and quiet study sessions. Prefer a peaceful environment.', '["Art", "Reading", "Movies", "Nature"]', '["Flexible", "Quiet", "Very Clean", "Neutral"]');
