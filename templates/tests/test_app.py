import unittest
from app import app, submissions

class TestApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        submissions.clear()
        self.client = app.test_client()

    def test_valid_submission(self):
        """Complete details and a valid submission URL"""
        response = self.client.post('/', data={
            'name': 'Sameer Ahmad',
            'reg_number': 'FA23-BSE-011',
            'title': 'DevOps Midterm',
            'url': 'https://github.com/sameer12354we5/assignment-portal'
        }, follow_redirects=True)
    
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Assignment submitted successfully!', response.data)
        self.assertIn(b'FA23-BSE-011', response.data)

    def test_missing_registration_number(self):
        """Missing registration number"""
        response = self.client.post('/', data={
            'name': 'Sameer Ahmad',
            'reg_number': '',
            'title': 'DevOps Midterm',
            'url': 'https://github.com/sameer12354we5/assignment-portal'
        }, follow_redirects=True)
    
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'All fields are required.', response.data)

    def test_invalid_submission_url(self):
        """Invalid submission URL"""
        response = self.client.post('/', data={
            'name': 'Sameer Ahmad',
            'reg_number': 'FA23-BSE-011',
            'title': 'DevOps Midterm',
            'url': 'not-a-valid-url'
        }, follow_redirects=True)
    
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid submission URL format.', response.data)