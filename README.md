# 📚 Book Review Web Application  

---

## 🚀 Overview

This project is a full-stack **Flask-based web application** that enables users to discover, review, and engage with a database of books. It features secure user authentication, comprehensive search capabilities, the ability to submit and read reviews, and administrative functionality for managing book entries.

The app uses a **MySQL database**, with structured schema defined in SQL and populated from a CSV dataset. It supports standard and advanced search queries, average rating calculations, and secure password handling using SHA-256.

> 🧠 This project is designed to showcase proficiency in **relational database design**, **complex SQL querying**, and **cloud deployment using Railway**.

---

## 🌟 Key Features

### 🔐 User Authentication
- Register and login using email and password
- Passwords are securely hashed using `hashlib` with SHA-256
- Flask session management handles login state

### 📖 Book Search & Filter
- Keyword-based book search across ISBN, title, author, genre
- Advanced filtering:
  - Publisher, year, page count, sort by rating, etc.
- Sort options (ascending/descending): title, author, genre, year, average rating

### ✍️ Reviews
- Authenticated users can:
  - Submit reviews with ratings (1 to 5)
  - View average ratings and prior reviews
- Rating data is aggregated and displayed in search results

### ⚙️ Admin Functions
- Add new books via a dedicated `add_book.html` page (form-based UI)
- Books include title, author, genre, publisher, year, and page count

---

## 🛠️ Technologies Used

### 👨‍💻 Backend
- **Python 3.8+**
- **Flask** — lightweight web framework for routing and templating
- **MySQL Connector** — interaction with MySQL database
- **hashlib + hmac** — secure password hashing and comparison

### 🗄️ Database
- **MySQL**
- Defined in `Book_Review_App_DB.sql`
  - Tables:
    - `Users`: id, username, email, password
    - `Books`: isbn, title, author, genre, publisher, publication_year, page_count
    - `Reviews`: id, user_id, book_id, rating, written_review, timestamp

### 🖼️ Frontend
- **Jinja2 HTML templates**
  - `register.html`, `login.html`, `search.html`, `advanced_search.html`, `add_review.html`, `add_book.html`, `write_review.html`
- **CSS** styling via `styles.css` (clean and responsive design)
- Form inputs, buttons, and tables styled for good UX

---

## ☁️ Cloud Deployment & SQL Emphasis

### 🚄 Railway-Powered Deployment
This app is fully deployed using [Railway](https://railway.app), a developer-first cloud platform. The following were configured in production:
- Hosted Flask app via GitHub integration
- Railway-managed **MySQL** database with persistent storage
- Environment variables used for secure DB connection in `app.py`
- External SQL client access via public host/port credentials

### 🧠 SQL-Focused Design
- **Schema-first** approach: all tables (`Users`, `Books`, `Reviews`, etc.) created via raw SQL in `Book_Review_App_DB.sql`
- Designed and optimized for:
  - `JOIN`s (user-to-review, book-to-review)
  - `GROUP BY` + `AVG()` for average rating calculations
  - Dynamic search queries with `LIKE`, `ORDER BY`, and filter chaining
- Book data imported via a custom Python → MySQL loader using `pandas` and `mysql.connector`
- Testing included raw `SHOW TABLES`, `INSERT`, `SELECT`, and query plan observation from MySQL CLI

This project was built intentionally as a **hands-on demonstration of SQL and cloud deployment proficiency**.

---

## 📁 Project Structure

```bash
.
├── app.py                    # Main Flask application with all routes
├── load_books_dataset.py     # Script to load CSV into MySQL database
├── books_dataset.csv         # CSV book dataset
├── Book_Review_App_DB.sql    # SQL schema file
├── static/
│   └── styles.css            # Application styling
├── templates/
│   ├── register.html         # Registration page
│   ├── login.html            # Login page
│   ├── search.html           # Basic search interface
│   ├── advanced_search.html  # Advanced filter-based search
│   ├── add_review.html       # Review submission form
│   ├── add_book.html         # Admin add-book form
│   └── write_review.html     # Alternative review form
├── requirements.txt          # Python package dependencies for the app
├── Procfile                  # Specifies the command to run the app on Railway
├── runtime.txt               # Specifies the Python version for deployment
└── README.md                 # Project documentation
```

## 🧪 Live Link

[Live App](https://web-production-0014.up.railway.app)  
_Deployed with Railway and powered by a cloud-hosted MySQL database._

## 🛠️ Future Improvements

- Implement review moderation and report system
- Add user profile pages and reading lists
- Build admin dashboard for book and user management
- Enable full-text search with indexing
