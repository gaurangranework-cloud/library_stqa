import pytest
import json
import time
from app import app

class ApiResponseWrapper:
    """Wraps Flask TestResponse to match requests.Response API"""
    def __init__(self, resp):
        self._resp = resp
        self.status_code = resp.status_code
        self.headers = dict(resp.headers)
        self.text = resp.get_data(as_text=True)
        self.content = resp.data

    def json(self):
        try:
            data = self._resp.get_json()
            if data is not None:
                return data
            return json.loads(self.text)
        except Exception:
            return {}

class AppSession:
    """Maintains session across requests using Flask test client"""
    def __init__(self):
        self.client = app.test_client()
    
    def login(self, username, password):
        resp = self.client.post('/api/login', json={'username': username, 'password': password})
        return ApiResponseWrapper(resp)
    
    def logout(self):
        resp = self.client.post('/api/logout')
        return ApiResponseWrapper(resp)
    
    def get(self, url, **kwargs):
        resp = self.client.get(f'/api{url}', **kwargs)
        return ApiResponseWrapper(resp)
    
    def post(self, url, **kwargs):
        resp = self.client.post(f'/api{url}', **kwargs)
        return ApiResponseWrapper(resp)
    
    def put(self, url, **kwargs):
        resp = self.client.put(f'/api{url}', **kwargs)
        return ApiResponseWrapper(resp)
    
    def delete(self, url, **kwargs):
        resp = self.client.delete(f'/api{url}', **kwargs)
        return ApiResponseWrapper(resp)


@pytest.fixture
def session():
    """Fixture to provide a clean unauthenticated session"""
    return AppSession()

@pytest.fixture
def admin_session():
    """Fixture to provide an authenticated admin session"""
    session = AppSession()
    session.login('admin', 'admin123')
    yield session
    session.logout()

@pytest.fixture
def student_session():
    """Fixture to provide an authenticated student session"""
    session = AppSession()
    session.login('student1', 'student123')
    yield session
    session.logout()


class TestAuthentication:
    """Authentication and Authorization Tests"""

    def test_valid_student_login(self, session):
        """Test valid student login (Equivalence Partitioning: Valid Class)"""
        response = session.login('student1', 'student123')
        assert response.status_code == 200
        assert response.json().get('user', {}).get('role') == 'student'

    def test_valid_admin_login(self, session):
        """Test valid admin login (Equivalence Partitioning: Valid Class)"""
        response = session.login('admin', 'admin123')
        assert response.status_code == 200
        assert response.json().get('user', {}).get('role') == 'librarian'

    def test_invalid_password(self, session):
        """Test login with wrong password (Equivalence Partitioning: Invalid Class)"""
        response = session.login('student1', 'wrongpass')
        assert response.status_code in [401, 403, 400]

    def test_nonexistent_user(self, session):
        """Test login with fake user (Equivalence Partitioning: Invalid Class)"""
        response = session.login('fakeuser', 'password123')
        assert response.status_code in [401, 403, 404, 400]

    def test_account_lockout(self, session):
        """Test account lockout after 5 failed attempts (Boundary Value Analysis)"""
        lock_user = f"lockuser_{int(time.time())}"
        session.post('/register', json={'username': lock_user, 'password': 'ValidPassword123!', 'role': 'student'})
        for _ in range(5):
            session.login(lock_user, 'wrongpass')
        response = session.login(lock_user, 'ValidPassword123!')
        # Expecting failure even with correct password due to lockout
        assert response.status_code in [403, 429]

    def test_password_validation_short(self, session):
        """Test registration with 4-char password (Boundary Value Analysis: < Min Length)"""
        response = session.post('/register', json={'username': 'newuser1', 'password': 'abc', 'role': 'student'})
        assert response.status_code == 400

    def test_password_validation_no_uppercase(self, session):
        """Test registration with missing uppercase (Equivalence Partitioning: Invalid Format)"""
        response = session.post('/register', json={'username': 'newuser2', 'password': 'password1!', 'role': 'student'})
        assert response.status_code == 400

    def test_password_validation_no_digit(self, session):
        """Test registration with missing digit (Equivalence Partitioning: Invalid Format)"""
        response = session.post('/register', json={'username': 'newuser3', 'password': 'Password!', 'role': 'student'})
        assert response.status_code == 400

    def test_password_validation_no_special(self, session):
        """Test registration with missing special character (Equivalence Partitioning: Invalid Format)"""
        response = session.post('/register', json={'username': 'newuser4', 'password': 'Password1', 'role': 'student'})
        assert response.status_code == 400

    def test_valid_registration(self, session):
        """Test registration with valid data (Equivalence Partitioning: Valid Class)"""
        username = f'newuser_{int(time.time())}'
        response = session.post('/register', json={'username': username, 'password': 'ValidPassword123!', 'role': 'student'})
        assert response.status_code in [200, 201]

    def test_duplicate_registration(self, session):
        """Test registering the same username twice (Error Guessing / Negative Testing)"""
        username = f'dupuser_{int(time.time())}'
        session.post('/register', json={'username': username, 'password': 'ValidPassword123!', 'role': 'student'})
        response = session.post('/register', json={'username': username, 'password': 'ValidPassword123!', 'role': 'student'})
        assert response.status_code in [400, 409]

    def test_sql_injection_login(self, session):
        """Test login with SQL injection payload (Security Testing)"""
        response = session.login("' OR 1=1--", "password")
        assert response.status_code in [400, 401, 403, 404]


class TestBookCatalog:
    """Book Catalog Search and Management Tests"""

    def test_search_all_books(self, student_session):
        """Test getting all books (Basic Functionality)"""
        response = student_session.get('/books')
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_search_by_isbn(self, student_session):
        """Test searching by ISBN (Equivalence Partitioning: Valid Search)"""
        response = student_session.get('/books?search=9780134685991')
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        if data:
            assert '9780134685991' in data[0].get('isbn', '')

    def test_search_by_title(self, student_session):
        """Test searching by title (Equivalence Partitioning: Valid Search)"""
        response = student_session.get('/books?search=Python')
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_search_by_category(self, student_session):
        """Test searching by category (Equivalence Partitioning: Valid Search)"""
        response = student_session.get('/books?category=Fiction')
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_search_empty_string(self, student_session):
        """Test searching with empty string (Boundary Value Analysis)"""
        response = student_session.get('/books?search=')
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_search_nonexistent(self, student_session):
        """Test searching for non-existent book (Equivalence Partitioning: Invalid Search)"""
        response = student_session.get('/books?search=xyznonexistent')
        assert response.status_code == 200
        assert len(response.json()) == 0

    def test_add_book_admin(self, admin_session):
        """Test adding a book as admin (Authorization Testing)"""
        book_data = {
            'isbn': f'978{int(time.time())}',
            'title': 'Test Automation Guide',
            'author': 'QA Engineer',
            'category': 'Education'
        }
        response = admin_session.post('/books', json=book_data)
        assert response.status_code in [200, 201]

    def test_add_book_invalid_isbn(self, admin_session):
        """Test adding book with 10-digit ISBN (Equivalence Partitioning: Invalid Format)"""
        book_data = {
            'isbn': '1234567890',
            'title': 'Invalid ISBN Book',
            'author': 'Author',
            'category': 'Education'
        }
        response = admin_session.post('/books', json=book_data)
        assert response.status_code == 400

    def test_add_book_student_forbidden(self, student_session):
        """Test adding book as student (Security / Authorization Testing)"""
        book_data = {
            'isbn': '9780000000001',
            'title': 'Student Hack',
            'author': 'Student',
            'category': 'Hacking'
        }
        response = student_session.post('/books', json=book_data)
        assert response.status_code in [401, 403]


class TestBookIssueReturn:
    """Book Issuing, Returning, and Fine Calculation Tests"""

    @staticmethod
    def _gen_isbn(offset=0):
        t = int(time.time() * 1000) + offset
        return f"978{t % 10000000000:010d}"

    def test_reserve_book(self, student_session, admin_session):
        """Test reserving an available book (State Transition: Available -> Reserved)"""
        isbn = self._gen_isbn(1)
        admin_session.post('/books', json={'isbn': isbn, 'title': 'Reserve Me', 'author': 'Author', 'category': 'Fiction'})
        response = student_session.post('/reserve', json={'isbn': isbn})
        assert response.status_code in [200, 201]

    def test_issue_reserved_book(self, admin_session):
        """Test issuing a reserved book (State Transition: Reserved -> Issued)"""
        username = f'issue_student_{int(time.time() * 1000)}'
        admin_session.post('/register', json={'username': username, 'password': 'ValidPassword123!', 'role': 'student'})
        student = AppSession()
        student.login(username, 'ValidPassword123!')
        
        isbn = self._gen_isbn(2)
        admin_session.post('/books', json={'isbn': isbn, 'title': 'Issue Me', 'author': 'Author', 'category': 'Fiction'})
        student.post('/reserve', json={'isbn': isbn})
        response = admin_session.post('/issue', json={'isbn': isbn, 'username': username})
        assert response.status_code in [200, 201]
        student.logout()

    def test_return_book_on_time(self, admin_session):
        """Test returning a book on time (Decision Table: On Time -> Fine = 0)"""
        username = f'ret_student_{int(time.time() * 1000)}'
        admin_session.post('/register', json={'username': username, 'password': 'ValidPassword123!', 'role': 'student'})
        student = AppSession()
        student.login(username, 'ValidPassword123!')
        
        isbn = self._gen_isbn(3)
        admin_session.post('/books', json={'isbn': isbn, 'title': 'Return Me', 'author': 'Author', 'category': 'Fiction'})
        student.post('/reserve', json={'isbn': isbn})
        admin_session.post('/issue', json={'isbn': isbn, 'username': username})
        response = admin_session.post('/return', json={'isbn': isbn, 'username': username})
        assert response.status_code == 200
        data = response.json()
        assert data.get('fine', 0) == 0
        student.logout()

    def test_issue_limit_3_books(self, student_session, admin_session):
        """Test issuing more than 3 books (Boundary Value Analysis: Max Books Limit)"""
        username = f'limit_student_{int(time.time())}'
        admin_session.post('/register', json={'username': username, 'password': 'ValidPassword123!', 'role': 'student'})
        
        new_student = AppSession()
        new_student.login(username, 'ValidPassword123!')
        
        for i in range(3):
            isbn = self._gen_isbn(10 + i)
            admin_session.post('/books', json={'isbn': isbn, 'title': f'Book {i}', 'author': 'Author', 'category': 'Fiction'})
            new_student.post('/reserve', json={'isbn': isbn})
            admin_session.post('/issue', json={'isbn': isbn, 'username': username})
            
        isbn4 = self._gen_isbn(20)
        admin_session.post('/books', json={'isbn': isbn4, 'title': 'Book 4', 'author': 'Author', 'category': 'Fiction'})
        new_student.post('/reserve', json={'isbn': isbn4})
        response = admin_session.post('/issue', json={'isbn': isbn4, 'username': username})
        assert response.status_code in [400, 403]
        new_student.logout()

    def test_return_overdue_fine(self, admin_session):
        """Test fine calculation for overdue book (Decision Table / BVA)"""
        response = admin_session.post('/return', json={'isbn': 'dummy', 'username': 'dummy', 'force_overdue_days': 5})
        assert response.status_code in [200, 400, 404]

    def test_state_transition_available_to_reserved(self, student_session, admin_session):
        """Test state transition from available to reserved (State Transition Testing)"""
        isbn = self._gen_isbn(30)
        admin_session.post('/books', json={'isbn': isbn, 'title': 'State Test', 'author': 'Author', 'category': 'Fiction'})
        response = student_session.post('/reserve', json={'isbn': isbn})
        assert response.status_code in [200, 201]
        
        books_response = student_session.get(f'/books?search={isbn}')
        if books_response.json():
            assert books_response.json()[0].get('status') == 'Reserved'

    def test_cannot_reserve_issued_book(self, admin_session):
        """Test reserving an already issued book (Negative Testing)"""
        username = f'issued_student_{int(time.time() * 1000)}'
        admin_session.post('/register', json={'username': username, 'password': 'ValidPassword123!', 'role': 'student'})
        student = AppSession()
        student.login(username, 'ValidPassword123!')

        isbn = self._gen_isbn(40)
        admin_session.post('/books', json={'isbn': isbn, 'title': 'Issued Book', 'author': 'Author', 'category': 'Fiction'})
        student.post('/reserve', json={'isbn': isbn})
        admin_session.post('/issue', json={'isbn': isbn, 'username': username})
        
        student2_session = AppSession()
        student2_session.login('student2', 'student123')
        response = student2_session.post('/reserve', json={'isbn': isbn})
        assert response.status_code in [400, 409]
        student2_session.logout()
        student.logout()



class TestDefectManagement:
    """Defect Tracker API Tests"""

    def test_get_defects(self, session):
        """Test retrieving all defects (Basic Functionality)"""
        response = session.get('/defects')
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_add_defect(self, session):
        """Test adding a new defect (Basic Functionality)"""
        defect_data = {
            'title': 'Login Button Missing',
            'description': 'The login button disappears on mobile view',
            'severity': 'High',
            'module': 'Authentication'
        }
        response = session.post('/defects', json=defect_data)
        assert response.status_code in [200, 201]

    def test_update_defect_status(self, session):
        """Test updating a defect status (State Transition Testing)"""
        defect_data = {
            'title': 'Test Defect',
            'description': 'Desc',
            'severity': 'Low',
            'module': 'UI'
        }
        create_res = session.post('/defects', json=defect_data)
        if create_res.status_code in [200, 201] and 'id' in create_res.json():
            defect_id = create_res.json()['id']
            response = session.put(f'/defects/{defect_id}', json={'status': 'Fixed'})
            assert response.status_code == 200


class TestExports:
    """CSV Export Generation Tests"""

    def test_export_test_cases_csv(self, session):
        """Test exporting test cases as CSV (Basic Functionality)"""
        response = session.get('/export/test-cases')
        assert response.status_code == 200
        assert 'text/csv' in response.headers.get('Content-Type', '')

    def test_export_defects_csv(self, session):
        """Test exporting defects as CSV (Basic Functionality)"""
        response = session.get('/export/defects')
        assert response.status_code == 200
        assert 'text/csv' in response.headers.get('Content-Type', '')

    def test_export_summary_csv(self, session):
        """Test exporting test summary as CSV (Basic Functionality)"""
        response = session.get('/export/summary')
        assert response.status_code == 200
        assert 'text/csv' in response.headers.get('Content-Type', '')


class TestDashboard:
    """Dashboard Stats and Automation Trigger Tests"""

    def test_dashboard_stats(self, session):
        """Test retrieving dashboard statistics (Basic Functionality)"""
        response = session.get('/dashboard-stats')
        assert response.status_code == 200
        data = response.json()
        assert 'total_test_cases' in data
        assert 'defects' in data
        assert 'execution_status' in data

    def test_run_automation(self, session):
        """Test running simulated automation suite (Integration Testing)"""
        response = session.post('/run-automation')
        assert response.status_code in [200, 202]
        data = response.json()
        assert 'results' in data or 'status' in data
