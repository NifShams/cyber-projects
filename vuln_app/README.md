# Flask Security Vulnerabilities Demo

This project demonstrates common security vulnerabilities in a Flask-based web application. The repository contains two versions of the same application: a vulnerable version that intentionally includes security flaws, and a secure version that implements proper security measures. This serves as an educational resource for developers to understand and learn how to prevent common web application security risks.

## Project Structure

```
.
├── app.py              # Vulnerable version of the application
├── secure_app.py       # Secure version with implemented safeguards
├── init_db.py         # Database initialization script
└── README.md          # This documentation
```

## Security Vulnerabilities Demonstrated

The vulnerable version (`app.py`) includes the following security flaws:

1. **SQL Injection**: Unsanitized user input is directly concatenated into SQL queries
2. **Cross-Site Scripting (XSS)**: User input is rendered without proper escaping
3. **Cross-Site Request Forgery (CSRF)**: No CSRF tokens implemented for form submissions
4. **Insecure Direct Object Reference (IDOR)**: No authorization checks for accessing user profiles
5. **Broken Authentication**: Weak session management and password storage
6. **Open Redirect**: No validation of redirect URLs
7. **Insecure Session Management**: Hardcoded secret key and insufficient session handling
8. **Insufficient Authorization**: Weak admin panel access controls

## Security Improvements

The secure version (`secure_app.py`) implements the following security measures:

1. **SQL Injection Prevention**: 
   - Use of parameterized queries
   - Proper input validation

2. **XSS Prevention**:
   - Input sanitization using `markupsafe.escape()`
   - Content Security Policy headers

3. **CSRF Protection**:
   - Implementation of CSRF tokens
   - Secure form handling

4. **Authorization**:
   - Proper access control checks
   - Session-based authentication verification

5. **Secure Authentication**:
   - Password hashing using bcrypt
   - Secure session management
   - Strong secret key generation

6. **URL Redirection Security**:
   - Whitelist of allowed domains
   - URL validation

## Setup and Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install flask bcrypt markupsafe
```

3. Initialize the database:
```bash
python init_db.py
```

4. Run the application:
```bash
# For vulnerable version
python app.py

# For secure version
python secure_app.py
```

## Usage

The application will be available at `http://localhost:5000`. Both versions include the following endpoints:

- `/login` - User authentication
- `/comment` - Comment posting system
- `/profile` - User profile access
- `/transfer` - Money transfer simulation
- `/dashboard` - User dashboard
- `/admin` - Administrative panel
- `/redirect` - URL redirection

## Educational Purpose Only

 **WARNING**: The vulnerable version (`app.py`) contains intentional security flaws and should never be used in a production environment. It is provided solely for educational purposes to demonstrate security vulnerabilities and their remediation.

## Testing the Vulnerabilities

### SQL Injection Example
```
Username: admin' OR '1'='1
Password: anything
```

### XSS Example
```
Comment: <script>alert('XSS')</script>
```

### CSRF Example
Create an HTML file with a form that submits to the transfer endpoint without a CSRF token.

## Contributing

Feel free to submit pull requests to add more security vulnerabilities or improvements to the secure version. Please ensure all additions are properly documented and include both vulnerable and secure implementations.
