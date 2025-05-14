-- Drop existing tables if needed
DROP TABLE IF EXISTS Book_Requests;
DROP TABLE IF EXISTS Book_Saves;
DROP TABLE IF EXISTS Reviews;
DROP TABLE IF EXISTS Books;
DROP TABLE IF EXISTS Users;

-- 1. Users Table
CREATE TABLE Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email_address VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- 2. Books Table
CREATE TABLE Books (
    isbn VARCHAR(13) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    genre VARCHAR(100),
    publisher VARCHAR(255),
    publication_year INT,
    page_count INT
);

-- 3. Reviews Table
CREATE TABLE Reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_id VARCHAR(13),
    user_id INT,
    rating INT,
    written_review TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES Books(isbn) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
);

-- 4. Book_Saves Table
CREATE TABLE Book_Saves (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    book_id VARCHAR(13),
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES Books(isbn) ON DELETE CASCADE
);

-- 5. Book_Requests Table
CREATE TABLE Book_Requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    isbn VARCHAR(13),
    request_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'Pending',
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
);

-- Sample Data for Users
-- user1@example.com : password123
-- user2@example.com : password123
-- admin1@example.com : adminpass

INSERT INTO Users (username, email_address, password) VALUES
('user1', 'user1@example.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f'),
('user2', 'user2@example.com', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f'),
('admin1', 'admin1@example.com', '3793e0a4380c836a4d1372c21f6cbad9574141c45893011c916459b9d28a7e38');


-- Sample Data for Books
INSERT INTO Books (isbn, title, author, genre, publisher, publication_year, page_count) VALUES
('1234567890123', 'Book A', 'Author A', 'Fiction', 'Publisher A', 2020, 300),
('9876543210987', 'Book B', 'Author B', 'Mystery', 'Publisher B', 2018, 250),
('4567891234567', 'Book C', 'Author C', 'Sci-Fi', 'Publisher C', 2022, 400);

-- Sample Data for Reviews
INSERT INTO Reviews (book_id, user_id, rating, written_review) VALUES
('1234567890123', 1, 5, 'An amazing book, highly recommend!'),
('9876543210987', 2, 4, 'Very interesting, but a bit slow in the middle.'),
('4567891234567', 1, 3, 'Decent read, but could be better.');

-- Sample Data for Book_Saves
INSERT INTO Book_Saves (user_id, book_id) VALUES
(1, '1234567890123'),
(1, '9876543210987'),
(2, '4567891234567');

-- Sample Data for Book_Requests
INSERT INTO Book_Requests (user_id, isbn) VALUES
(1, '1234567890123'),
(2, '9876543210987');
