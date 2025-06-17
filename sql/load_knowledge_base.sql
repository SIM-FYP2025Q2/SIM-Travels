DROP DATABASE IF EXISTS `knowledge_base`;
CREATE DATABASE IF NOT EXISTS `knowledge_base`;
USE `knowledge_base`;

-- Users Table
CREATE TABLE `Users` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `username` VARCHAR(50) NOT NULL UNIQUE,
    `email` VARCHAR(100) NOT NULL UNIQUE,
    `password` VARCHAR(255) NOT NULL,
    `is_admin` BOOLEAN NOT NULL DEFAULT FALSE,
    `is_active` BOOLEAN NOT NULL DEFAULT FALSE
);

-- Category table with UNIQUE category name
CREATE TABLE `Category` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `category` VARCHAR(100) NOT NULL UNIQUE
);

-- FAQ table with a foreign key to Category
CREATE TABLE `FAQ` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `question` TEXT NOT NULL,
    `answer` TEXT NOT NULL,
    `category_id` INT NOT NULL,
    `link` TEXT NULL,
    `is_synced` BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (`category_id`) REFERENCES `Category` (`id`)
);

-- Insert into Users table
INSERT INTO `Users` (`username`, `email`, `password`, `is_admin`, `is_active`) VALUES
('admin', 'admin@email.com', '$2y$10$RU7.5wQr.743eFntHokafOCtSZQ1pnf2G.ioHatEOPdmY3bjk7lwi', TRUE, TRUE),
('jake', 'jake@email.com', '$2y$10$RU7.5wQr.743eFntHokafOCtSZQ1pnf2G.ioHatEOPdmY3bjk7lwi', FALSE, TRUE);

-- Insert into Category table
INSERT INTO `Category` (`category`) VALUES
('Account'),
('Billing'),
('Technical Support'),
('Security'),
('General');

-- Insert into FAQ table
INSERT INTO `FAQ` (`question`, `answer`, `link`, `category_id`) VALUES
('How do I reset my password?',
 'Click on "Forgot Password" on the login screen and follow the instructions.',
 'https://example.com/account/reset-password',
 1),

('How can I update my account information?',
 'Navigate to your account settings and click "Update".',
 'https://example.com/account',
 1),

('How do I check in for my flight online?',
 'You can check in online via the airline''s website or app, usually 24–48 hours before departure.',
 'https://example.com/faq/1',
 5),

('What is the baggage policy for AirAsia?',
 'For AirAsia, cabin baggage is limited to 7kg. Weight limit for one checked baggage is 32kg. Each passenger is entitled to purchase one checked baggage per booking, per flight.',
 'https://www.airasia.com/aa/inflight-comforts/en/gb/baggage.html',
 5),

('What payment methods are accepted?',
 'We accept credit/debit cards, PayPal, and selected e-wallets like GrabPay.',
 'https://example.com/faq/billing-support',
 2);

