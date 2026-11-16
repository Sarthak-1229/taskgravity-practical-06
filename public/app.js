/**
 * Practical 06: RESTful API Console Client
 */

const createForm = document.getElementById('createForm');
const taskListContainer = document.getElementById('taskList');
const jsonViewer = document.getElementById('jsonViewer');
const responseStatusBadge = document.getElementById('responseStatusBadge');

const statTotal = document.getElementById('statTotal');
const statInProgress = document.getElementById('statInProgress');
const statPending = document.getElementById('statPending');
const statVelocity = document.getElementById('statVelocity');

document.addEventListener('DOMContentLoaded', () => {
  fetchTasks();
  fetchStats();
});

function logResponse(status, data) {
  responseStatusBadge.textContent = `Status: ${status} | Timestamp: ${new Date().toLocaleTimeString()}`;
  jsonViewer.textContent = JSON.stringify(data, null, 2);
}

async function fetchTasks() {
  try {
    const res = await fetch('/api/tasks');
    const json = await res.json();
    logResponse(res.status, json);
    if (json.success) renderTasks(json.data);
  } catch (err) {
    console.error('Error fetching tasks:', err);
  }
}

async function fetchStats() {
  try {
    const res = await fetch('/api/tasks/stats');
    const json = await res.json();
    if (json.success && json.stats) {
      statTotal.textContent = json.stats.total;
      statInProgress.textContent = json.stats.inProgress;
      statPending.textContent = json.stats.pending;
      statVelocity.textContent = `${json.stats.velocity}%`;
    }
  } catch (err) {}
}

createForm.addEventListener('submit', async (e) => {
  e.preventDefault();

  const payload = {
    title: document.getElementById('taskTitle').value,
    category: document.getElementById('taskCategory').value,
    priority: document.getElementById('taskPriority').value,
    dueDate: document.getElementById('taskDueDate').value,
    estimatedHours: document.getElementById('taskHours').value,
    description: document.getElementById('taskDesc').value
  };

  try {
    const res = await fetch('/api/tasks', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const result = await res.json();
    logResponse(res.status, result);

    if (res.status === 201) {
      createForm.reset();
      fetchTasks();
      fetchStats();
    }
  } catch (err) {
    logResponse(500, { error: err.message });
  }
});

async function cycleStatus(id) {
  try {
    const res = await fetch(`/api/tasks/${id}/status`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({})
    });
    const result = await res.json();
    logResponse(res.status, result);
    fetchTasks();
    fetchStats();
  } catch (err) {
    logResponse(500, { error: err.message });
  }
}

async function deleteTask(id) {
  if (!confirm(`Execute DELETE /api/tasks/${id}?`)) return;
  try {
    const res = await fetch(`/api/tasks/${id}`, { method: 'DELETE' });
    const result = await res.json();
    logResponse(res.status, result);
    fetchTasks();
    fetchStats();
  } catch (err) {
    logResponse(500, { error: err.message });
  }
}

function renderTasks(tasks) {
  if (!tasks || tasks.length === 0) {
    taskListContainer.innerHTML = `
      <div style="text-align: center; padding: 2rem; background: #fff; border: 1px dashed #e2e8f0; border-radius: 6px; color: #64748b;">
        Database collection is currently empty.
      </div>
    `;
    return;
  }

  taskListContainer.innerHTML = tasks.map(t => {
    const priorityClass = `badge-${t.priority.toLowerCase()}`;
    const statusClass = `badge-${t.status}`;
    return `
      <article class="task-card">
        <div class="task-header">
          <span class="task-title">${escapeHTML(t.title)}</span>
          <div style="display: flex; gap: 4px;">
            <span class="badge ${priorityClass}">${t.priority}</span>
            <span class="badge ${statusClass}">${t.status}</span>
          </div>
        </div>
        ${t.description ? `<p class="task-desc">${escapeHTML(t.description)}</p>` : ''}
        <div class="task-meta">
          <div>
            <span class="badge badge-category">${t.category}</span>
            <span style="margin-left: 8px;">Due: <strong>${t.dueDate}</strong></span>
            <span style="margin-left: 8px;">Est: <strong>${t.estimatedHours}h</strong></span>
          </div>
          <div style="display: flex; gap: 4px; align-items: center;">
            <code style="font-size: 0.7rem; color: #64748b;">${t.id}</code>
            <button class="btn btn-secondary btn-sm" onclick="cycleStatus('${t.id}')">PATCH Status</button>
            <button class="btn btn-sm" style="background: transparent; color: #dc2626;" onclick="deleteTask('${t.id}')">DELETE</button>
          </div>
        </div>
      </article>
    `;
  }).join('');
}

function escapeHTML(str) {
  if (!str) return '';
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}
