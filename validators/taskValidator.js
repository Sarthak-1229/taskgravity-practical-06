/**
 * REST API Payload Validator
 */

const VALID_CATEGORIES = ['Frontend', 'Backend', 'Database', 'DevOps', 'Testing', 'UI/UX'];
const VALID_PRIORITIES = ['Low', 'Medium', 'High', 'Urgent'];
const VALID_STATUSES = ['pending', 'in-progress', 'completed'];

function validateCreateTask(body) {
  const errors = {};

  if (!body.title || typeof body.title !== 'string' || body.title.trim().length < 3) {
    errors.title = 'Title must be at least 3 characters.';
  } else if (body.title.trim().length > 80) {
    errors.title = 'Title cannot exceed 80 characters.';
  }

  if (!body.category || !VALID_CATEGORIES.includes(body.category)) {
    errors.category = `Category must be one of: ${VALID_CATEGORIES.join(', ')}.`;
  }

  if (!body.priority || !VALID_PRIORITIES.includes(body.priority)) {
    errors.priority = `Priority must be one of: ${VALID_PRIORITIES.join(', ')}.`;
  }

  if (!body.dueDate || isNaN(new Date(body.dueDate).getTime())) {
    errors.dueDate = 'Valid ISO8601 deadline (YYYY-MM-DD) is required.';
  }

  const h = Number(body.estimatedHours);
  if (body.estimatedHours === undefined || isNaN(h) || h < 0.5 || h > 100) {
    errors.estimatedHours = 'Effort must be a numeric value between 0.5 and 100 hours.';
  }

  if (body.description && typeof body.description === 'string' && body.description.length > 300) {
    errors.description = 'Description cannot exceed 300 characters.';
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors
  };
}

function validateUpdateTask(body) {
  const errors = {};

  if (body.title !== undefined) {
    if (typeof body.title !== 'string' || body.title.trim().length < 3) {
      errors.title = 'Title must be at least 3 characters.';
    } else if (body.title.trim().length > 80) {
      errors.title = 'Title cannot exceed 80 characters.';
    }
  }

  if (body.category !== undefined && !VALID_CATEGORIES.includes(body.category)) {
    errors.category = `Category must be one of: ${VALID_CATEGORIES.join(', ')}.`;
  }

  if (body.priority !== undefined && !VALID_PRIORITIES.includes(body.priority)) {
    errors.priority = `Priority must be one of: ${VALID_PRIORITIES.join(', ')}.`;
  }

  if (body.status !== undefined && !VALID_STATUSES.includes(body.status)) {
    errors.status = `Status must be one of: ${VALID_STATUSES.join(', ')}.`;
  }

  if (body.estimatedHours !== undefined) {
    const h = Number(body.estimatedHours);
    if (isNaN(h) || h < 0.5 || h > 100) {
      errors.estimatedHours = 'Effort must be a numeric value between 0.5 and 100 hours.';
    }
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors
  };
}

module.exports = {
  VALID_CATEGORIES,
  VALID_PRIORITIES,
  VALID_STATUSES,
  validateCreateTask,
  validateUpdateTask
};
