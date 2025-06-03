import unittest
import json
from simple_task_manager.src.app import create_app
from simple_task_manager.src.models import db, Task
from datetime import datetime, timezone

# SAARTHI-20250603131546: LOW | LINTING
# ISSUE: Class name does not follow the recommended naming convention for test classes.
# POLICY: N/A
# FIX: Rename the class to TaskApiTests.
# EFFORT: [5m]
class TaskApiTestCase(unittest.TestCase):
    """This class represents the task API test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app('test')  # Use testing configuration
        self.client = self.app.test_client()
        self.task_payload = {'title': 'Test Task Title', 'description': 'My test description'}

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Executed after each test"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_health_check(self):
        """Test API health check."""
        res = self.client.get('/health')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['status'], 'healthy')

# SAARTHI-20250603131546: HIGH | COMPLETENESS
# ISSUE: Test coverage is very low.
# POLICY: Policy 4.1: Core business logic and utility functions must have unit tests. Policy 4.2: API endpoints should have integration tests covering common success and failure scenarios.
# FIX: Add more test cases to cover all the task API endpoints.
# EFFORT: [1d]
# SAARTHI-202506031556: LOW | LINTING
# ISSUE: Class name does not follow the recommended naming convention for test classes.
# POLICY: N/A
# FIX: Rename the class to TaskApiTests.
if __name__ == "__main__":
    unittest.main()
