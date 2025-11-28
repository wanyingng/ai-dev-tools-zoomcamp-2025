from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import TodoItem


class TodoItemModelTests(TestCase):
    """Tests for the TodoItem model."""
    
    def test_create_todo_item(self):
        """Test creating a todo item with required fields."""
        todo = TodoItem.objects.create(
            title="Test Todo",
            description="Test Description"
        )
        self.assertEqual(todo.title, "Test Todo")
        self.assertEqual(todo.description, "Test Description")
        self.assertIsNotNone(todo.created_at)
    
    def test_default_is_resolved_false(self):
        """Test that is_resolved defaults to False."""
        todo = TodoItem.objects.create(title="Test Todo")
        self.assertFalse(todo.is_resolved)
    
    def test_str_representation(self):
        """Test the string representation returns the title."""
        todo = TodoItem.objects.create(title="My Task")
        self.assertEqual(str(todo), "My Task")
    
    def test_ordering_by_due_date(self):
        """Test that todos are ordered by due_date, then by created_at."""
        now = timezone.now()
        
        # Create todos with different due dates
        todo1 = TodoItem.objects.create(
            title="Later Task",
            due_date=now + timedelta(days=2)
        )
        todo2 = TodoItem.objects.create(
            title="Earlier Task",
            due_date=now + timedelta(days=1)
        )
        todo3 = TodoItem.objects.create(
            title="No Due Date"
        )
        
        todos = list(TodoItem.objects.all())
        # In SQLite, NULL values sort FIRST in ascending order
        # So items without due_date come first, then items with due_date (sorted by date)
        self.assertEqual(todos[0].title, "No Due Date")
        self.assertEqual(todos[1].title, "Earlier Task")
        self.assertEqual(todos[2].title, "Later Task")


class TodoListViewTests(TestCase):
    """Tests for the TodoListView."""
    
    def setUp(self):
        self.client = Client()
        self.url = reverse('todo-list')
    
    def test_list_view_displays_todos(self):
        """Test that list view displays all todos."""
        TodoItem.objects.create(title="Task 1")
        TodoItem.objects.create(title="Task 2")
        
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Task 1")
        self.assertContains(response, "Task 2")
    
    def test_list_view_empty_state(self):
        """Test empty state when no todos exist."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No tasks found")
    
    def test_filter_active_todos(self):
        """Test filtering for active (unresolved) todos."""
        active = TodoItem.objects.create(title="Active Task", is_resolved=False)
        resolved = TodoItem.objects.create(title="Resolved Task", is_resolved=True)
        
        response = self.client.get(self.url + '?status=active')
        self.assertEqual(response.status_code, 200)
        
        # Check that only active todo is in the context
        todos = response.context['todos']
        self.assertEqual(len(todos), 1)
        self.assertEqual(todos[0].title, "Active Task")
        self.assertFalse(todos[0].is_resolved)
    
    def test_filter_resolved_todos(self):
        """Test filtering for resolved todos."""
        active = TodoItem.objects.create(title="Active Task", is_resolved=False)
        resolved = TodoItem.objects.create(title="Resolved Task", is_resolved=True)
        
        response = self.client.get(self.url + '?status=resolved')
        self.assertEqual(response.status_code, 200)
        
        # Check that only resolved todo is in the context
        todos = response.context['todos']
        self.assertEqual(len(todos), 1)
        self.assertEqual(todos[0].title, "Resolved Task")
        self.assertTrue(todos[0].is_resolved)


class TodoCreateViewTests(TestCase):
    """Tests for the TodoCreateView."""
    
    def setUp(self):
        self.client = Client()
        self.url = reverse('todo-create')
    
    def test_create_view_get(self):
        """Test GET request shows the form."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "New Task")
    
    def test_create_todo_with_valid_data(self):
        """Test creating a todo with valid POST data."""
        data = {
            'title': 'New Task',
            'description': 'Task description',
        }
        response = self.client.post(self.url, data)
        
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertEqual(TodoItem.objects.count(), 1)
        
        todo = TodoItem.objects.first()
        self.assertEqual(todo.title, 'New Task')
        self.assertEqual(todo.description, 'Task description')
    
    def test_create_redirects_to_list(self):
        """Test that successful creation redirects to list view."""
        data = {'title': 'New Task'}
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('todo-list'))


class TodoUpdateViewTests(TestCase):
    """Tests for the TodoUpdateView."""
    
    def setUp(self):
        self.client = Client()
        self.todo = TodoItem.objects.create(
            title="Original Title",
            description="Original Description"
        )
        self.url = reverse('todo-update', kwargs={'pk': self.todo.pk})
    
    def test_update_view_get(self):
        """Test GET request shows form with existing data."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Original Title")
        self.assertContains(response, "Edit Task")
    
    def test_update_todo_with_valid_data(self):
        """Test updating a todo with valid POST data."""
        data = {
            'title': 'Updated Title',
            'description': 'Updated Description',
            'is_resolved': True
        }
        response = self.client.post(self.url, data)
        
        self.assertEqual(response.status_code, 302)  # Redirect
        
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, 'Updated Title')
        self.assertEqual(self.todo.description, 'Updated Description')
        self.assertTrue(self.todo.is_resolved)
    
    def test_mark_todo_as_resolved(self):
        """Test marking a todo as resolved."""
        data = {
            'title': self.todo.title,
            'description': self.todo.description,
            'is_resolved': True
        }
        self.client.post(self.url, data)
        
        self.todo.refresh_from_db()
        self.assertTrue(self.todo.is_resolved)
    
    def test_update_redirects_to_list(self):
        """Test that successful update redirects to list view."""
        data = {'title': 'Updated', 'is_resolved': False}
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('todo-list'))


class TodoDeleteViewTests(TestCase):
    """Tests for the TodoDeleteView."""
    
    def setUp(self):
        self.client = Client()
        self.todo = TodoItem.objects.create(title="Task to Delete")
        self.url = reverse('todo-delete', kwargs={'pk': self.todo.pk})
    
    def test_delete_view_get(self):
        """Test GET request shows confirmation page."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Delete Task")
        self.assertContains(response, "Task to Delete")
    
    def test_delete_todo(self):
        """Test POST request deletes the todo."""
        self.assertEqual(TodoItem.objects.count(), 1)
        
        response = self.client.post(self.url)
        
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertEqual(TodoItem.objects.count(), 0)
    
    def test_delete_redirects_to_list(self):
        """Test that successful deletion redirects to list view."""
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('todo-list'))


class URLTests(TestCase):
    """Tests for URL routing."""
    
    def test_list_url_resolves(self):
        """Test that list URL resolves correctly."""
        url = reverse('todo-list')
        self.assertEqual(url, '/')
    
    def test_create_url_resolves(self):
        """Test that create URL resolves correctly."""
        url = reverse('todo-create')
        self.assertEqual(url, '/create/')
    
    def test_update_url_resolves(self):
        """Test that update URL resolves correctly."""
        url = reverse('todo-update', kwargs={'pk': 1})
        self.assertEqual(url, '/1/update/')
    
    def test_delete_url_resolves(self):
        """Test that delete URL resolves correctly."""
        url = reverse('todo-delete', kwargs={'pk': 1})
        self.assertEqual(url, '/1/delete/')
