const GET_TASKS_URL = '/api/get-task-list/';
const CREATE_TASK_URL = '/api/create-task/';
const UPDATE_TASK_URL = '/api/update-task/';
const DELETE_TASK_URL = '/api/delete-task/';

const taskForm = document.getElementById('task-form');
const taskListEl = document.getElementById('task-list');
const filterBtns = document.querySelectorAll('.filter-btn');

let currentFilter = '';

// ---------- Fetch & render ----------

async function fetchTasks() {
  const res = await fetch(GET_TASKS_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ status: currentFilter || null }),
  });
  const data = await res.json();

  if (data.status !== 'success') {
    taskListEl.innerHTML = `<p class="empty-msg">${escapeHtml(data.message || 'Something went wrong')}</p>`;
    return;
  }

  renderTasks(data.payload.tasks);
}

function renderTasks(tasks) {
  taskListEl.innerHTML = '';

  if (!tasks.length) {
    taskListEl.innerHTML = '<p class="empty-msg">No tasks here yet 🎉</p>';
    return;
  }

  tasks.forEach(task => {
    const item = document.createElement('div');
    item.className = `task-item ${task.status === 'completed' ? 'completed' : ''}`;

    item.innerHTML = `
      <div class="task-main">
        <div class="task-title">${escapeHtml(task.title)}</div>
        ${task.description ? `<div class="task-desc">${escapeHtml(task.description)}</div>` : ''}
        <div class="task-meta">
          <span class="badge badge-${task.priority}">${task.priority}</span>
          <span class="badge badge-${task.status}">${(task.status || '').replace('_', ' ')}</span>
          ${task.due_date ? `<span class="badge">Due: ${task.due_date}</span>` : ''}
        </div>
      </div>
      <div class="task-actions">
        <select data-id="${task.id}" class="status-select">
          <option value="pending" ${task.status === 'pending' ? 'selected' : ''}>Pending</option>
          <option value="in_progress" ${task.status === 'in_progress' ? 'selected' : ''}>In Progress</option>
          <option value="completed" ${task.status === 'completed' ? 'selected' : ''}>Completed</option>
        </select>
        <button class="delete-btn" data-id="${task.id}">Delete</button>
      </div>
    `;

    taskListEl.appendChild(item);
  });

  document.querySelectorAll('.status-select').forEach(sel => {
    sel.addEventListener('change', e => updateStatus(e.target.dataset.id, e.target.value));
  });
  document.querySelectorAll('.delete-btn').forEach(btn => {
    btn.addEventListener('click', e => deleteTask(e.target.dataset.id));
  });
}

function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str || '';
  return div.innerHTML;
}

// ---------- Create ----------

taskForm.addEventListener('submit', async (e) => {
  e.preventDefault();

  const payload = {
    title: document.getElementById('title').value.trim(),
    description: document.getElementById('description').value.trim(),
    priority: document.getElementById('priority').value,
    status: 'pending',
    due_date: document.getElementById('due_date').value || null,
  };

  if (!payload.title) return;

  const res = await fetch(CREATE_TASK_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  const data = await res.json();

  if (data.status !== 'success') {
    alert(data.message || 'Could not create task');
    return;
  }

  taskForm.reset();
  document.getElementById('priority').value = 'medium';
  fetchTasks();
});

// ---------- Update status ----------

async function updateStatus(id, status) {
  const res = await fetch(UPDATE_TASK_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ taskId: id, status }),
  });
  const data = await res.json();

  if (data.status !== 'success') {
    alert(data.message || 'Could not update task');
    return;
  }

  fetchTasks();
}

// ---------- Delete ----------

async function deleteTask(id) {
  if (!confirm('Delete this task?')) return;

  const res = await fetch(DELETE_TASK_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ taskId: id }),
  });
  const data = await res.json();

  if (data.status !== 'success') {
    alert(data.message || 'Could not delete task');
    return;
  }

  fetchTasks();
}

// ---------- Filters ----------

filterBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    filterBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    currentFilter = btn.dataset.status;
    fetchTasks();
  });
});

// ---------- Init ----------

fetchTasks();
