/**
 * RESTful Routes for TaskGravity Tasks Resource
 */

const express = require('express');
const router = express.Router();
const TaskStore = require('../models/taskStore');
const { validateCreateTask, validateUpdateTask, VALID_STATUSES } = require('../validators/taskValidator');

// GET /api/tasks - Read all with filtering & pagination
router.get('/', (req, res) => {
  try {
    const { status, category, priority, search, page, limit } = req.query;
    const result = TaskStore.findAll({ status, category, priority, search, page, limit });
    res.status(200).json({
      success: true,
      count: result.tasks.length,
      pagination: {
        total: result.total,
        page: result.page,
        limit: result.limit,
        totalPages: result.totalPages
      },
      data: result.tasks
    });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Server error retrieving tasks', error: err.message });
  }
});

// GET /api/tasks/stats - Get aggregated metrics
router.get('/stats', (req, res) => {
  try {
    const stats = TaskStore.getStats();
    res.status(200).json({ success: true, stats });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Server error retrieving stats', error: err.message });
  }
});

// GET /api/tasks/:id - Read single task
router.get('/:id', (req, res) => {
  try {
    const task = TaskStore.findById(req.params.id);
    if (!task) {
      return res.status(404).json({
        success: false,
        message: `Task with id '${req.params.id}' was not found.`
      });
    }
    res.status(200).json({ success: true, data: task });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Server error retrieving task', error: err.message });
  }
});

// POST /api/tasks - Create new task
router.post('/', (req, res) => {
  try {
    const validation = validateCreateTask(req.body);
    if (!validation.isValid) {
      return res.status(400).json({
        success: false,
        message: 'Validation failed for new task resource.',
        errors: validation.errors
      });
    }

    const created = TaskStore.create(req.body);
    res.status(201).json({
      success: true,
      message: 'Task resource successfully created.',
      data: created
    });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Server error creating task', error: err.message });
  }
});

// PUT /api/tasks/:id - Full Update
router.put('/:id', (req, res) => {
  try {
    const existing = TaskStore.findById(req.params.id);
    if (!existing) {
      return res.status(404).json({
        success: false,
        message: `Task with id '${req.params.id}' not found for update.`
      });
    }

    const validation = validateUpdateTask(req.body);
    if (!validation.isValid) {
      return res.status(400).json({
        success: false,
        message: 'Validation failed for update payload.',
        errors: validation.errors
      });
    }

    const updated = TaskStore.update(req.params.id, req.body);
    res.status(200).json({
      success: true,
      message: `Task '${req.params.id}' updated successfully.`,
      data: updated
    });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Server error updating task', error: err.message });
  }
});

// PATCH /api/tasks/:id/status - Partial status update
router.patch('/:id/status', (req, res) => {
  try {
    const existing = TaskStore.findById(req.params.id);
    if (!existing) {
      return res.status(404).json({
        success: false,
        message: `Task with id '${req.params.id}' not found.`
      });
    }

    const { status } = req.body;
    let targetStatus = status;

    if (!targetStatus) {
      // Cycle automatically if no status body provided
      targetStatus = existing.status === 'pending'
        ? 'in-progress'
        : existing.status === 'in-progress'
          ? 'completed'
          : 'pending';
    } else if (!VALID_STATUSES.includes(targetStatus)) {
      return res.status(400).json({
        success: false,
        message: `Invalid status. Must be one of: ${VALID_STATUSES.join(', ')}.`
      });
    }

    const updated = TaskStore.updateStatus(req.params.id, targetStatus);
    res.status(200).json({
      success: true,
      message: `Task status updated to '${targetStatus}'.`,
      data: updated
    });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Server error updating status', error: err.message });
  }
});

// DELETE /api/tasks/:id - Delete task
router.delete('/:id', (req, res) => {
  try {
    const existing = TaskStore.findById(req.params.id);
    if (!existing) {
      return res.status(404).json({
        success: false,
        message: `Task with id '${req.params.id}' not found for deletion.`
      });
    }

    const deleted = TaskStore.delete(req.params.id);
    res.status(200).json({
      success: true,
      message: `Task '${deleted.title}' (${deleted.id}) successfully deleted.`,
      data: deleted
    });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Server error deleting task', error: err.message });
  }
});

module.exports = router;
