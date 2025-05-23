import hashlib
import hmac
import os

from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'CS480_FINAL_PROJECT_SECRET_KEY'  # Replace with a strong secret key

#mySQLpassword = input("Enter Your MySQL Password: ")

# Database configuration
db_config = {
    'host': os.getenv('MYSQLHOST', 'localhost'),
    'user': os.getenv('MYSQLUSER', 'root'),
    'password': os.getenv('MYSQLPASSWORD', ''),
    'database': os.getenv('MYSQLDATABASE', 'book_reviews'),
    'port': int(os.getenv('MYSQLPORT', 3306))
}

# Connect to MySQL
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Hash password using hashlib
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Verify password
def verify_password(stored_password, provided_password):
    return hmac.compare_digest(stored_password, hash_password(provided_password))


@app.route('/')
def home():
    return redirect(url_for('login'))

# User registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        hashed_password = hash_password(password)
        print(f"Attempting to register: {username}, {email}, {hashed_password}")

        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO Users (username, email_address, password) VALUES (%s, %s, %s)",
                (username, email, hashed_password)
            )
            connection.commit()
            print("User successfully inserted into the database.")
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))

        except mysql.connector.Error as err:
            print(f"[REGISTER ERROR] {err}")
            flash(f'Registration failed: {err}', 'danger')

        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'connection' in locals() and connection:
                connection.close()

    return render_template('register.html')




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Users WHERE email_address = %s", (email,))
            user = cursor.fetchone()

            if user and verify_password(user['password'], password):
                session['user_id'] = user['id']
                session['username'] = user['username']
                flash('Login successful!', 'success')
                return redirect(url_for('search_data'))
            else:
                flash('Invalid credentials. Please try again.', 'danger')
        except Exception as e:
            print(f"[ERROR] Failed DB connection or query: {e}")
            flash("Database error occurred.", "danger")
            return render_template("login.html")
        finally:
            # Close resources if they exist
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'connection' in locals() and connection:
                connection.close()

    return render_template('login.html')



# User logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))



# Search books with sorting
@app.route('/search', methods=['GET', 'POST'])
def search_data():
    search_query = None
    rows = []

    search_query = request.form.get('search_query', '').strip()
    sort_by = request.form.get('sort_by', 'title').strip()
    sort_order = request.form.get('sort_order', 'ASC').strip()

    connection = get_db_connection()
    cursor = connection.cursor()


    if request.method == 'POST':

        query = """
            SELECT Books.isbn, Books.title, Books.author, Books.genre, 
                Books.publisher, Books.publication_year, Books.page_count,
                AVG(Reviews.rating) AS average_rating
            FROM Books
            LEFT JOIN Reviews ON Books.isbn = Reviews.book_id
            WHERE (%s = '' OR LOWER(Books.isbn) LIKE LOWER(%s))
            or (%s = '' OR LOWER(Books.title) LIKE LOWER(%s))
            or (%s = '' OR LOWER(Books.author) LIKE LOWER(%s))
            or (%s = '' OR LOWER(Books.genre) LIKE LOWER(%s))
            GROUP BY Books.isbn, Books.title, Books.author, Books.genre, Books.publisher, Books.publication_year, Books.page_count
        """

        valid_sort_columns = ['title', 'author', 'genre', 'publication_year', 'average_rating']
        if sort_by in valid_sort_columns and sort_order in ['ASC', 'DESC']:
            query += f" ORDER BY {sort_by} {sort_order}"
        

        like_query = f"%{search_query}%"
        print(search_query)
        print(like_query)
        params = [search_query, like_query, 
                  search_query, like_query,
                  search_query, like_query, 
                  search_query, like_query]
        
        cursor.execute(query, params)
        rows = cursor.fetchall()

        cursor.close()
        connection.close()

    return render_template('search.html', search_query=search_query, rows=rows, sort_by=sort_by, sort_order=sort_order)

@app.route('/advanced_search', methods=['GET', 'POST'])
def advanced_search():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))

    search_query = None
    rows = []

    # If the form is submitted
    if request.method == 'POST':
        search_query = request.form.get('search_query', '').strip()
        sort_by = request.form.get('sort_by', 'title').strip()
        sort_order = request.form.get('sort_order', 'ASC').strip()

        isbn = request.form.get('isbn', '').strip()
        title = request.form.get('title', '').strip()
        author = request.form.get('author', '').strip()
        genre = request.form.get('genre', '').strip()
        publisher = request.form.get('publisher', '').strip()
        publication_year = request.form.get('publication_year', '').strip()
        min_page_count = request.form.get('min_page_count', '').strip()
        max_page_count = request.form.get('max_page_count', '').strip()
    
        # Connect to the database
        connection = get_db_connection()
        cursor = connection.cursor()

        # SQL query with wildcard search
        query = """
          SELECT Books.isbn, Books.title, Books.author, Books.genre, 
          Books.publisher, Books.publication_year, Books.page_count,
          AVG(Reviews.rating) AS average_rating
          FROM Books
          LEFT JOIN Reviews ON Books.isbn = Reviews.book_id
          WHERE (%s = '' OR LOWER(Books.isbn) LIKE LOWER(%s))
          AND (%s = '' OR LOWER(Books.title) LIKE LOWER(%s))
          AND (%s = '' OR LOWER(Books.author) LIKE LOWER(%s))
          AND (%s = '' OR LOWER(Books.genre) LIKE LOWER(%s))
          AND (%s = '' OR LOWER(publisher) LIKE LOWER(%s))
          AND (%s = '' OR publication_year = %s)
          AND (%s = '' OR page_count >= %s)
          AND (%s = '' OR page_count <= %s)
          GROUP BY Books.isbn
        """
        valid_sort_columns = ['title', 'author', 'genre', 'publication_year', 'average_rating']
        if sort_by in valid_sort_columns and sort_order in ['ASC', 'DESC']:
            query += f" ORDER BY {sort_by} {sort_order}"

        params = [
            isbn, f"%{isbn}%",
            title, f"%{title}%",
            author, f"%{author}%",
            genre, f"%{genre}%",
            publisher, f"%{publisher}%",
            publication_year, publication_year,
            min_page_count, min_page_count,
            max_page_count, max_page_count
        ]
        cursor.execute(query, params)

        # Fetch the results
        rows = cursor.fetchall()

        # Close the connection
        cursor.close()
        connection.close()

    # Render the HTML template
    return render_template('advanced_search.html', search_query=search_query, rows=rows)

@app.route('/add_review/<isbn>', methods=['GET', 'POST'])
def add_review(isbn):
    if 'user_id' not in session:
        flash('Please log in to leave a review.', 'warning')
        return redirect(url_for('login'))
    
    search_query = request.args.get('search_query', '')
    sort_by = request.args.get('sort_by', 'title')
    sort_order = request.args.get('sort_order', 'ASC')


    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Books WHERE isbn = %s", (isbn,))
    book = cursor.fetchone()

    if not book:
        flash('Sorry, we could not fetch the book for some reason.', 'danger')
        return redirect(url_for('search_data'))
    
    if request.method == 'POST':
        rating = request.form.get('rating')
        written_review = request.form.get('written_review')

        if not rating or not rating.isdigit() or not (1 <= int(rating) <= 5):
            flash('Rating must be a number between 1 and 5.', 'danger')
        else:
            try:
                cursor.execute(
                    """
                    INSERT INTO Reviews (book_id, user_id, rating, written_review)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (isbn, session['user_id'], int(rating), written_review)
                )
                connection.commit()  
                flash('Review submitted successfully!', 'success')
                return redirect(url_for('search_data'))  # Redirect to search page
            except mysql.connector.Error as err:
                flash(f'Error submitting review: {err}', 'danger')

    cursor.close()
    return render_template('add_review.html', book=book, search_query=search_query, sort_by=sort_by, sort_order=sort_order)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
