# Practical 06: RESTful API using Node.js and Express

## TaskGravity — CRUD REST Architecture, Persistent Data Storage, and Automated Postman Testing

### 1. Overview
Practical 06 develops a production-structured RESTful API adhering to REST principles (uniform interface, statelessness, appropriate HTTP verbs and response status codes) and connects to a persistent database store.

### 2. RESTful Resource Endpoints
| Method | Route | Description | Success Code |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/health` | Service uptime and heartbeat check | 200 OK |
| `GET` | `/api/tasks` | Retrieve all tasks (supports `?status=`, `?category=`, `?search=`) | 200 OK |
| `GET` | `/api/tasks/stats` | Aggregated metrics (total, completed, in-progress, velocity) | 200 OK |
| `GET` | `/api/tasks/:id` | Retrieve single task resource by ID | 200 OK (or 404) |
| `POST` | `/api/tasks` | Create new task resource with payload validation | 201 Created (or 400) |
| `PUT` | `/api/tasks/:id` | Full replacement/update of an existing task | 200 OK (or 400/404) |
| `PATCH`| `/api/tasks/:id/status`| Partial update modifying task lifecycle status | 200 OK (or 400/404) |
| `DELETE`| `/api/tasks/:id` | Permanently remove a task resource | 200 OK (or 404) |

### 3. Postman Test Suite
Import `TaskGravity_Practical_06.postman_collection.json` directly into Postman.
The collection includes 11 automated test scenarios with Chai assertions verifying:
- Status code contracts (200, 201, 400, 404).
- Automatic propagation of newly created `taskId` across subsequent update and delete requests.
- Response JSON schema validation.

### 4. Running Locally
```bash
cd Practical6
npm install
npm start
```
Interactive API console & inspector: `http://localhost:5000`.
