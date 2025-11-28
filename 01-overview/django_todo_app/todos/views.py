from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import TodoItem


class TodoListView(ListView):
    model = TodoItem
    template_name = 'todos/home.html'
    context_object_name = 'todos'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')
        if status == 'resolved':
            return queryset.filter(is_resolved=True)
        elif status == 'active':
            return queryset.filter(is_resolved=False)
        return queryset


class TodoCreateView(CreateView):
    model = TodoItem
    template_name = 'todos/todo_form.html'
    fields = ['title', 'description', 'due_date']
    success_url = reverse_lazy('todo-list')


class TodoUpdateView(UpdateView):
    model = TodoItem
    template_name = 'todos/todo_form.html'
    fields = ['title', 'description', 'due_date', 'is_resolved']
    success_url = reverse_lazy('todo-list')


class TodoDeleteView(DeleteView):
    model = TodoItem
    template_name = 'todos/todo_confirm_delete.html'
    success_url = reverse_lazy('todo-list')
