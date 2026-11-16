/**
 * Task Data Access Layer (DAL) for Practical 06
 * Implements persistent database operations with file synchronization.
 */

const fs = require('fs');
const path = require('path');

const DB_FILE = path.join(__dirname, '..', 'data', 'tasks.json');

// Ensure database file exists
function ensureDb() {
  if (!fs.existsSync(DB_FILE)) {
    fs.mkdirSync(path.dirname(DB_FILE), { recursive: true });
    fs.writeFileSync(DB_FILE, JSON.stringify([], null, 2), 'utf-8');
  }
}

function readAll() {
  ensureDb();
  try {
    const raw = fs.readFileSync(DB_FILE, 'utf-8');
    return JSON.parse(raw);
  } catch (err) {
    console.error('[DAL] Error reading database:', err);
    return [];
  }
}

function writeAll(data) {
  ensureDb();
  fs.writeFileSync(DB_FILE, JSON.stringify(data, null, 2), 'utf-8');
}

const TaskStore = {
  // Read all with filtering and pagination
  findAll({ status, category, priority, search, page = 1, limit = 50 } = {}) {
    let items = readAll();

    if (status && status !== 'all') {
      items = items.filter(t => t.status === status);
    }
    if (category && category !== 'all') {
      items = items.filter(t => t.category === category);
    }
    if (priority && priority !== 'all') {
      items = items.filter(t => t.priority === priority);
    }
    if (search) {
      const q = search.toLowerCase();
      items = items.filter(t => t.title.toLowerCase().includes(q) || (t.description || '').toLowerCase().includes(q));
    }

    const total = items.length;
    const startIndex = (page - 1) * limit;
    const paginated = items.slice(startIndex, startIndex + limit);

    return {
      total,
      page: Number(page),
      limit: Number(limit),
      totalPages: Math.ceil(total / limit),
      tasks: paginated
    };
  },

  // Read single by ID
  findById(id) {
    const items = readAll();
    return items.find(t => t.id === id) || null;
  },

  // Create new task
  create(payload) {
    const items = readAll();
    const newTask = {
      id: 'tg-api-' + Date.now().toString().slice(-4),
      title: payload.title.trim(),
      category: payload.category,
      priority: payload.priority,
      dueDate: payload.dueDate,
      estimatedHours: Number(payload.estimatedHours),
      description: (payload.description || '').trim(),
      status: payload.status || 'pending',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };

    items.unshift(newTask);
    writeAll(items);
    return newTask;
  },

  // Full Update
  update(id, payload) {
    const items = readAll();
    const index = items.findIndex(t => t.id === id);
    if (index === -1) return null;

    const existing = items[index];
    const updated = {
      ...existing,
      title: payload.title !== undefined ? payload.title.trim() : existing.title,
      category: payload.category || existing.category,
      priority: payload.priority || existing.priority,
      dueDate: payload.dueDate || existing.dueDate,
      estimatedHours: payload.estimatedHours !== undefined ? Number(payload.estimatedHours) : existing.estimatedHours,
      description: payload.description !== undefined ? payload.description.trim() : existing.description,
      status: payload.status || existing.status,
      updatedAt: new Date().toISOString()
    };

    items[index] = updated;
    writeAll(items);
    return updated;
  },

  // Partial status update
  updateStatus(id, newStatus) {
    const items = readAll();
    const task = items.find(t => t.id === id);
    if (!task) return null;

    task.status = newStatus;
    task.updatedAt = new Date().toISOString();
    writeAll(items);
    return task;
  },

  // Delete
  delete(id) {
    const items = readAll();
    const index = items.findIndex(t => t.id === id);
    if (index === -1) return null;

    const [removed] = items.splice(index, 1);
    writeAll(items);
    return removed;
  },

  // Aggregated Stats
  getStats() {
    const items = readAll();
    const total = items.length;
    const completed = items.filter(t => t.status === 'completed').length;
    const inProgress = items.filter(t => t.status === 'in-progress').length;
    const pending = items.filter(t => t.status === 'pending').length;

    return {
      total,
      completed,
      inProgress,
      pending,
      velocity: total > 0 ? Math.round((completed / total) * 100) : 0
    };
  }
};

module.exports = TaskStore;
