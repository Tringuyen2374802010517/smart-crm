# BT3 – API Reference (OpenAPI)

Source: FastAPI OpenAPI schema exported from the running backend.

The endpoint definitions below reflect declared OpenAPI metadata.
Authentication, authorization and runtime responses require separate verification.

## 1. GET `/`

**Purpose:** Home

**Parameters:**

- None declared

**Request body:**

None declared

**Declared responses:**

- HTTP `200`: Successful Response
```json
{
  "text/plain": {
    "schema": {
      "type": "string"
    }
  }
}
```

**Authentication / role:** Public endpoint; verify deployment-specific access restrictions separately.

**Runtime request/response evidence:** No endpoint-specific runtime evidence established in this audit.

---

## 2. GET `/appointments`

**Purpose:** List Appointments

**Parameters:**

- `authorization` (header), required=False; schema: `{"anyOf": [{"type": "string"}, {"type": "null"}], "title": "Authorization"}`

**Request body:**

None declared

**Declared responses:**

- HTTP `200`: Successful Response
```json
{
  "application/json": {
    "schema": {}
  }
}
```
- HTTP `422`: Validation Error
```json
{
  "application/json": {
    "schema": {
      "$ref": "#/components/schemas/HTTPValidationError"
    }
  }
}
```

**Authentication / role:** Authenticated user; based on router dependencies or authentication implementation.

**Runtime request/response evidence:** HTTP 200 verified with authenticated TECHNICIAN session in clean-room; HTTP 401 verified without authentication. Other scenarios not fully verified.

---

## 3. POST `/appointments`

**Purpose:** Create Appointment

**Parameters:**

- `authorization` (header), required=False; schema: `{"anyOf": [{"type": "string"}, {"type": "null"}], "title": "Authorization"}`

**Request body:**

```json
{
  "required": true,
  "content": {
    "application/json": {
      "schema": {
        "$ref": "#/components/schemas/AppointmentInput"
      }
    }
  }
}
```

**Declared responses:**

- HTTP `201`: Successful Response
```json
{
  "application/json": {
    "schema": {}
  }
}
```
- HTTP `422`: Validation Error
```json
{
  "application/json": {
    "schema": {
      "$ref": "#/components/schemas/HTTPValidationError"
    }
  }
}
```

**Authentication / role:** Authenticated user; based on router dependencies or authentication implementation.

**Runtime request/response evidence:** No endpoint-specific runtime evidence established in this audit.

---

## 4. POST `/appointments/check`

**Purpose:** Check Appointment

**Parameters:**

- `authorization` (header), required=False; schema: `{"anyOf": [{"type": "string"}, {"type": "null"}], "title": "Authorization"}`

**Request body:**

```json
{
  "required": true,
  "content": {
    "application/json": {
      "schema": {
        "$ref": "#/components/schemas/AppointmentInput"
      }
    }
  }
}
```

**Declared responses:**

- HTTP `200`: Successful Response
```json
{
  "application/json": {
    "schema": {}
  }
}
```
- HTTP `422`: Validation Error
```json
{
  "application/json": {
    "schema": {
      "$ref": "#/components/schemas/HTTPValidationError"
    }
  }
}
```

**Authentication / role:** Authenticated user; based on router dependencies or authentication implementation.

**Runtime request/response evidence:** No endpoint-specific runtime evidence established in this audit.

---

## 5. GET `/appointments/context/{ticket_id}`

**Purpose:** Appointment Context

**Parameters:**

- `ticket_id` (path), required=True; schema: `{"type": "integer", "title": "Ticket Id"}`
- `authorization` (header), required=False; schema: `{"anyOf": [{"type": "string"}, {"type": "null"}], "title": "Authorization"}`

**Request body:**

None declared

**Declared responses:**

- HTTP `200`: Successful Response
```json
{
  "application/json": {
    "schema": {}
  }
}
```
- HTTP `422`: Validation Error
```json
{
  "application/json": {
    "schema": {
      "$ref": "#/components/schemas/HTTPValidationError"
    }
  }
}
```

**Authentication / role:** Authenticated user; based on router dependencies or authentication implementation.

**Runtime request/response evidence:** HTTP 200 verified with authenticated TECHNICIAN session in clean-room; HTTP 401 verified without authentication. Other scenarios not fully verified.

---

## 6. GET `/appointments/ticket/{ticket_id}`

**Purpose:** Ticket Appointments

**Parameters:**

- `ticket_id` (path), required=True; schema: `{"type": "integer", "title": "Ticket Id"}`
- `authorization` (header), required=False; schema: `{"anyOf": [{"type": "string"}, {"type": "null"}], "title": "Authorization"}`

**Request body:**

None declared

**Declared responses:**

- HTTP `200`: Successful Response
```json
{
  "application/json": {
    "schema": {}
  }
}
```
- HTTP `422`: Validation Error
```json
{
  "application/json": {
    "schema": {
      "$ref": "#/components/schemas/HTTPValidationError"
    }
  }
}
```

**Authentication / role:** Authenticated user; based on router dependencies or authentication implementation.

**Runtime request/response evidence:** HTTP 200 verified with authenticated TECHNICIAN session in clean-room; HTTP 401 verified without authentication. Other scenarios not fully verified.

---

## 7. POST `/assignments/`

**Purpose:** Create Assignment

**Parameters:**

- `authorization` (header), required=False; schema: `{"anyOf": [{"type": "string"}, {"type": "null"}], "title": "Authorization"}`

**Request body:**

```json
{
  "required": true,
  "content": {
    "application/json": {
      "schema": {
        "$ref": "#/components/schemas/AssignmentCreate"
      }
    }
  }
}
```

**Declared responses:**

- HTTP `201`: Successful Response
```json
{
  "application/json": {
    "schema": {}
  }
}
```
- HTTP `422`: Validation Error
```json
{
  "application/json": {
    "schema": {
      "$ref": "#/components/schemas/HTTPValidationError"
    }
  }
}
```

**Authentication / role:** MANAGER only; verified by source inspection and TECHNICIAN HTTP 403 tests.

**Runtime request/response evidence:** HTTP 403 verified with TECHNICIAN session. Other scenarios not fully verified.

---

## 8. GET `/assignments/eligible-technicians/{ticket_id}`

**Purpose:** Get Eligible Technicians

**Parameters:**

- `ticket_id` (path), required=True; schema: `{"type": "integer", "title": "Ticket Id"}`
- `authorization` (header), required=False; schema: `{"anyOf": [{"type": "string"}, {"type": "null"}], "title": "Authorization"}`

**Request body:**

None declared

**Declared responses:**

- HTTP `200`: Successful Response
```json
{
  "application/json": {
    "schema": {}
  }
}
```
- HTTP `422`: Validation Error
```json
{
  "application/json": {
    "schema": {
      "$ref": "#/components/schemas/HTTPValidationError"
    }
  }
}
```

**Authentication / role:** Authenticated user; based on router dependencies or authentication implementation.

**Runtime request/response evidence:** HTTP 200 verified with authenticated TECHNICIAN session in clean-room; HTTP 401 verified without authentication. Other scenarios not fully verified.

---

## 9. GET `/assignments/ticket/{ticket_id}/detail`

**Purpose:** Get Ticket Assignment Detail

**Parameters:**

- `ticket_id` (path), required=True; schema: `{"type": "integer", "title": "Ticket Id"}`
- `authorization` (header), required=False; schema: `{"anyOf": [{"type": "string"}, {"type": "null"}], "title": "Authorization"}`

**Request body:**

None declared

**Declared responses:**

- HTTP `200`: Successful Response
```json
{
  "application/json": {
    "schema": {}
  }
}
```
- HTTP `422`: Validation Error
```json
{
  "application/json": {
    "schema": {
      "$ref": "#/components/schemas/HTTPValidationError"
    }
  }
}
```

**Authentication / role:** Authenticated user; based on router dependencies or authentication implementation.

**Runtime request/response evidence:** HTTP 200 verified with authenticated TECHNICIAN session in clean-room; HTTP 401 verified without authentication. Other scenarios not fully verified.

---

## 10. GET `/assignments/ticket/{ticket_id}/history`

**Purpose:** Get Assignment History

**Parameters:**

- `ticket_id` (path), required=True; schema: `{"type": "integer", "title": "Ticket Id"}`
- `authorization` (header), required=False; schema: `{"anyOf": [{"type": "string"}, {"type": "null"}], "title": "Authorization"}`

**Request body:**

None declared

**Declared responses:**

- HTTP `200`: Successful Response
```json
{
  "application/json": {
    "schema": {}
  }
}
```
- HTTP `422`: Validation Error
```json
{
  "application/json": {
    "schema": {
      "$ref": "#/components/schemas/HTTPValidationError"
    }
  }
}
```

**Authentication / role:** MANAGER only; verified by source inspection and TECHNICIAN HTTP 403 tests.

**Runtime request/response evidence:** HTTP 401 verified without authentication; HTTP 403 verified with TECHNICIAN session. Other scenarios not fully verified.

---

## 11. PUT `/assignments/ticket/{ticket_id}/reassign`

**Purpose:** Reassign Assignment

**Parameters:**

- `ticket_id` (path), required=True; schema: `{"type": "integer", "title": "Ticket Id"}`
- `authorization` (header), required=False; schema: `{"anyOf": [{"type": "string"}, {"type": "null"}], "title": "Authorization"}`

**Request body:**

```json
{
  "required": true,
  "content": {
    "application/json": {
      "schema": {
        "$ref": "#/components/schemas/ReassignmentInput"
      }
    }
  }
}
```

**Declared responses:**

- HTTP `200`: Successful Response
```json
{
  "application/json": {
    "schema": {}
  }
}
```
- HTTP `422`: Validation Error
```json
{
  "application/json": {
    "schema": {
      "$ref": "#/components/schemas/HTTPValidationError"
    }
  }
}
```

**Authentication / role:** MANAGER only; verified by source inspection and TECHNICIAN HTTP 403 tests.

**Runtime request/response evidence:** HTTP 403 verified with TECHNICIAN session. Other scenarios not fully verified.

---

## 12. GET `/assignments/ticket/{ticket_id}/reassignment-candidates`

**Purpose:** Get Reassignment Candidates

**Parameters:**

- `ticket_id` (path), required=True; schema: `{"type": "integer", "title": "Ticket Id"}`
- `authorization` (header), required=False; schema: `{"anyOf": [{"type": "string"}, {"type": "null"}], "title": "Authorization"}`

**Request body:**

None declared

**Declared responses:**

- HTTP `200`: Successful Response
```json
{
  "application/json": {
    "schema": {}
  }
}
```
- HTTP `422`: Validation Error
```json
{
  "application/json": {
    "schema": {
      "$ref": "#/components/schemas/HTTPValidationError"
    }
  }
}
```

**Authentication / role:** MANAGER only; verified by source inspection and TECHNICIAN HTTP 403 tests.

**Runtime request/response evidence:** HTTP 401 verified without authentication; HTTP 403 verified with TECHNICIAN session. Other scenarios not fully verified.

---

## 13. POST `/auth/login`

**Purpose:** Login

**Parameters:**

- None declared

**Request body:**

```json
{
  "content": {
    "application/json": {
      "schema": {
        "$ref": "#/components/schemas/LoginInput"
      }
    }
  },
  "required": true
}
```

**Declared responses:**

- HTTP `200`: Successful Response
```json
{
  "application/json": {
    "schema": {}
  }
}
```
- HTTP `422`: Validation Error
```json
{
  "application/json": {
    "schema": {
      "$ref": "#/components/schemas/HTTPValidationError"
    }
  }
}
```

**Authentication / role:** Public endpoint; verify deployment-specific access restrictions separately.

**Runtime request/response evidence:** No endpoint-specific runtime evidence established in this audit.

---

## 14. POST `/auth/logout`

**Purpose:** Logout

**Parameters:**

- `authorization` (header), required=False; schema: `{"anyOf": [{"type": "string"}, {"type": "null"}], "title": "Authorization"}`

**Request body:**

None declared

**Declared responses:**

- HTTP `200`: Successful Response
```json
{
  "application/json": {
    "schema": {}
  }
}
```
- HTTP `422`: Validation Error
```json
{
  "application/json": {
    "schema": {
      "$ref": "#/components/schemas/HTTPValidationError"
    }
  }
}
```

**Authentication / role:** Authenticated user; based on router dependencies or authentication implementation.

**Runtime request/response evidence:** No endpoint-specific runtime evidence established in this audit.

---

## 15. GET `/auth/me`

**Purpose:** Me

**Parameters:**

- `authorization` (header), required=False; schema: `{"anyOf": [{"type": "string"}, {"type": "null"}], "title": "Authorization"}`

**Request body:**

None declared

**Declared responses:**

- HTTP `200`: Successful Response
```json
{
  "application/json": {
    "schema": {}
  }
}
```
- HTTP `422`: Validation Error
```json
{
  "application/json": {
    "schema": {
      "$ref": "#/components/schemas/HTTPValidationError"
    }
  }
}
```

**Authentication / role:** Authenticated user; based on router dependencies or authentication implementation.

**Runtime request/response evidence:** No endpoint-specific runtime evidence established in this audit.

---

## 16. GET `/db-check`

**Purpose:** Db Check

**Parameters:**

- None declared

**Request body:**

None declared

**Declared responses:**

- HTTP `200`: Successful Response
```json
{
  "application/json": {
    "schema": {}
  }
}
```

**Authentication / role:** Public endpoint; verify deployment-specific access restrictions separately.

**Runtime request/response evidence:** No endpoint-specific runtime evidence established in this audit.

---

## 17. GET `/health`

**Purpose:** Health Check

**Parameters:**

- None declared

**Request body:**

None declared

**Declared responses:**

- HTTP `200`: Successful Response
```json
{
  "application/json": {
    "schema": {}
  }
}
```

**Authentication / role:** Public endpoint; verify deployment-specific access restrictions separately.

**Runtime request/response evidence:** No endpoint-specific runtime evidence established in this audit.

---

## 18. GET `/technicians`

**Purpose:** List Technicians

**Parameters:**

- `authorization` (header), required=False; schema: `{"anyOf": [{"type": "string"}, {"type": "null"}], "title": "Authorization"}`

**Request body:**

None declared

**Declared responses:**

- HTTP `200`: Successful Response
```json
{
  "application/json": {
    "schema": {}
  }
}
```
- HTTP `422`: Validation Error
```json
{
  "application/json": {
    "schema": {
      "$ref": "#/components/schemas/HTTPValidationError"
    }
  }
}
```

**Authentication / role:** Authenticated user; based on router dependencies or authentication implementation.

**Runtime request/response evidence:** HTTP 200 verified with authenticated TECHNICIAN session in clean-room; HTTP 401 verified without authentication. Other scenarios not fully verified.

---

## 19. POST `/technicians`

**Purpose:** Create Technician

**Parameters:**

- `authorization` (header), required=False; schema: `{"anyOf": [{"type": "string"}, {"type": "null"}], "title": "Authorization"}`

**Request body:**

```json
{
  "required": true,
  "content": {
    "application/json": {
      "schema": {
        "$ref": "#/components/schemas/TechnicianInput"
      }
    }
  }
}
```

**Declared responses:**

- HTTP `201`: Successful Response
```json
{
  "application/json": {
    "schema": {}
  }
}
```
- HTTP `422`: Validation Error
```json
{
  "application/json": {
    "schema": {
      "$ref": "#/components/schemas/HTTPValidationError"
    }
  }
}
```

**Authentication / role:** Authenticated user; based on router dependencies or authentication implementation.

**Runtime request/response evidence:** No endpoint-specific runtime evidence established in this audit.

---

## 20. GET `/technicians/{technician_id}`

**Purpose:** Get Technician

**Parameters:**

- `technician_id` (path), required=True; schema: `{"type": "integer", "title": "Technician Id"}`
- `authorization` (header), required=False; schema: `{"anyOf": [{"type": "string"}, {"type": "null"}], "title": "Authorization"}`

**Request body:**

None declared

**Declared responses:**

- HTTP `200`: Successful Response
```json
{
  "application/json": {
    "schema": {}
  }
}
```
- HTTP `422`: Validation Error
```json
{
  "application/json": {
    "schema": {
      "$ref": "#/components/schemas/HTTPValidationError"
    }
  }
}
```

**Authentication / role:** Authenticated user; based on router dependencies or authentication implementation.

**Runtime request/response evidence:** HTTP 200 verified with authenticated TECHNICIAN session in clean-room; HTTP 401 verified without authentication. Other scenarios not fully verified.

---

## 21. PUT `/technicians/{technician_id}`

**Purpose:** Update Technician

**Parameters:**

- `technician_id` (path), required=True; schema: `{"type": "integer", "title": "Technician Id"}`
- `authorization` (header), required=False; schema: `{"anyOf": [{"type": "string"}, {"type": "null"}], "title": "Authorization"}`

**Request body:**

```json
{
  "required": true,
  "content": {
    "application/json": {
      "schema": {
        "$ref": "#/components/schemas/TechnicianInput"
      }
    }
  }
}
```

**Declared responses:**

- HTTP `200`: Successful Response
```json
{
  "application/json": {
    "schema": {}
  }
}
```
- HTTP `422`: Validation Error
```json
{
  "application/json": {
    "schema": {
      "$ref": "#/components/schemas/HTTPValidationError"
    }
  }
}
```

**Authentication / role:** Authenticated user; based on router dependencies or authentication implementation.

**Runtime request/response evidence:** No endpoint-specific runtime evidence established in this audit.

---

## 22. DELETE `/technicians/{technician_id}`

**Purpose:** Delete Technician

**Parameters:**

- `technician_id` (path), required=True; schema: `{"type": "integer", "title": "Technician Id"}`
- `authorization` (header), required=False; schema: `{"anyOf": [{"type": "string"}, {"type": "null"}], "title": "Authorization"}`

**Request body:**

None declared

**Declared responses:**

- HTTP `200`: Successful Response
```json
{
  "application/json": {
    "schema": {}
  }
}
```
- HTTP `422`: Validation Error
```json
{
  "application/json": {
    "schema": {
      "$ref": "#/components/schemas/HTTPValidationError"
    }
  }
}
```

**Authentication / role:** Authenticated user; based on router dependencies or authentication implementation.

**Runtime request/response evidence:** No endpoint-specific runtime evidence established in this audit.

---

## 23. GET `/tickets`

**Purpose:** List Tickets

**Parameters:**

- `authorization` (header), required=False; schema: `{"anyOf": [{"type": "string"}, {"type": "null"}], "title": "Authorization"}`

**Request body:**

None declared

**Declared responses:**

- HTTP `200`: Successful Response
```json
{
  "application/json": {
    "schema": {}
  }
}
```
- HTTP `422`: Validation Error
```json
{
  "application/json": {
    "schema": {
      "$ref": "#/components/schemas/HTTPValidationError"
    }
  }
}
```

**Authentication / role:** Authenticated user; based on router dependencies or authentication implementation.

**Runtime request/response evidence:** HTTP 200 verified with authenticated TECHNICIAN session in clean-room; HTTP 401 verified without authentication. Other scenarios not fully verified.

---

## 24. POST `/tickets`

**Purpose:** Create Ticket

**Parameters:**

- `authorization` (header), required=False; schema: `{"anyOf": [{"type": "string"}, {"type": "null"}], "title": "Authorization"}`

**Request body:**

```json
{
  "required": true,
  "content": {
    "application/json": {
      "schema": {
        "$ref": "#/components/schemas/TicketInput"
      }
    }
  }
}
```

**Declared responses:**

- HTTP `201`: Successful Response
```json
{
  "application/json": {
    "schema": {}
  }
}
```
- HTTP `422`: Validation Error
```json
{
  "application/json": {
    "schema": {
      "$ref": "#/components/schemas/HTTPValidationError"
    }
  }
}
```

**Authentication / role:** Authenticated user; based on router dependencies or authentication implementation.

**Runtime request/response evidence:** No endpoint-specific runtime evidence established in this audit.

---

## 25. GET `/tickets/{ticket_id}`

**Purpose:** Get Ticket

**Parameters:**

- `ticket_id` (path), required=True; schema: `{"type": "integer", "title": "Ticket Id"}`
- `authorization` (header), required=False; schema: `{"anyOf": [{"type": "string"}, {"type": "null"}], "title": "Authorization"}`

**Request body:**

None declared

**Declared responses:**

- HTTP `200`: Successful Response
```json
{
  "application/json": {
    "schema": {}
  }
}
```
- HTTP `422`: Validation Error
```json
{
  "application/json": {
    "schema": {
      "$ref": "#/components/schemas/HTTPValidationError"
    }
  }
}
```

**Authentication / role:** Authenticated user; based on router dependencies or authentication implementation.

**Runtime request/response evidence:** HTTP 200 verified with authenticated TECHNICIAN session in clean-room; HTTP 401 verified without authentication. Other scenarios not fully verified.

---

## 26. PUT `/tickets/{ticket_id}`

**Purpose:** Update Ticket

**Parameters:**

- `ticket_id` (path), required=True; schema: `{"type": "integer", "title": "Ticket Id"}`
- `authorization` (header), required=False; schema: `{"anyOf": [{"type": "string"}, {"type": "null"}], "title": "Authorization"}`

**Request body:**

```json
{
  "required": true,
  "content": {
    "application/json": {
      "schema": {
        "$ref": "#/components/schemas/TicketInput"
      }
    }
  }
}
```

**Declared responses:**

- HTTP `200`: Successful Response
```json
{
  "application/json": {
    "schema": {}
  }
}
```
- HTTP `422`: Validation Error
```json
{
  "application/json": {
    "schema": {
      "$ref": "#/components/schemas/HTTPValidationError"
    }
  }
}
```

**Authentication / role:** Authenticated user; based on router dependencies or authentication implementation.

**Runtime request/response evidence:** No endpoint-specific runtime evidence established in this audit.

---

## 27. DELETE `/tickets/{ticket_id}`

**Purpose:** Delete Ticket

**Parameters:**

- `ticket_id` (path), required=True; schema: `{"type": "integer", "title": "Ticket Id"}`
- `authorization` (header), required=False; schema: `{"anyOf": [{"type": "string"}, {"type": "null"}], "title": "Authorization"}`

**Request body:**

None declared

**Declared responses:**

- HTTP `200`: Successful Response
```json
{
  "application/json": {
    "schema": {}
  }
}
```
- HTTP `422`: Validation Error
```json
{
  "application/json": {
    "schema": {
      "$ref": "#/components/schemas/HTTPValidationError"
    }
  }
}
```

**Authentication / role:** Authenticated user; based on router dependencies or authentication implementation.

**Runtime request/response evidence:** No endpoint-specific runtime evidence established in this audit.

---

## 28. PATCH `/tickets/{ticket_id}/complete`

**Purpose:** Complete Ticket

**Parameters:**

- `ticket_id` (path), required=True; schema: `{"type": "integer", "title": "Ticket Id"}`
- `authorization` (header), required=False; schema: `{"anyOf": [{"type": "string"}, {"type": "null"}], "title": "Authorization"}`

**Request body:**

None declared

**Declared responses:**

- HTTP `200`: Successful Response
```json
{
  "application/json": {
    "schema": {}
  }
}
```
- HTTP `422`: Validation Error
```json
{
  "application/json": {
    "schema": {
      "$ref": "#/components/schemas/HTTPValidationError"
    }
  }
}
```

**Authentication / role:** Authenticated user; based on router dependencies or authentication implementation.

**Runtime request/response evidence:** No endpoint-specific runtime evidence established in this audit.

---

---

## BT3 – Unauthenticated GET Verification (11/11)

Test environment: local FastAPI backend, port 8000.

Test method: HTTP GET without Authorization header.

| Endpoint | Expected | Actual | Result |
|---|---|---|---|
| GET /appointments | 401 | 401 | PASS |
| GET /appointments/context/{ticket_id} | 401 | 401 | PASS |
| GET /appointments/ticket/{ticket_id} | 401 | 401 | PASS |
| GET /assignments/eligible-technicians/{ticket_id} | 401 | 401 | PASS |
| GET /assignments/ticket/{ticket_id}/detail | 401 | 401 | PASS |
| GET /assignments/ticket/{ticket_id}/history | 401 | 401 | PASS |
| GET /assignments/ticket/{ticket_id}/reassignment-candidates | 401 | 401 | PASS |
| GET /technicians | 401 | 401 | PASS |
| GET /technicians/{technician_id} | 401 | 401 | PASS |
| GET /tickets | 401 | 401 | PASS |
| GET /tickets/{ticket_id} | 401 | 401 | PASS |

**Result: 11/11 PASS.**

Scope: verifies unauthenticated GET access only. Write operations, invalid or expired tokens, and role-based authorization are not covered by this test.

---

## BT3 – Assignment Authorization Matrix

Source: `src/backend/api/assignment_api.py` and `src/backend/main.py`.

| Method | Endpoint | Required role |
|---|---|---|
| GET | `/assignments/eligible-technicians/{ticket_id}` | Authenticated user |
| POST | `/assignments/` | MANAGER |
| GET | `/assignments/ticket/{ticket_id}/reassignment-candidates` | MANAGER |
| PUT | `/assignments/ticket/{ticket_id}/reassign` | MANAGER |
| GET | `/assignments/ticket/{ticket_id}/detail` | Authenticated user |
| GET | `/assignments/ticket/{ticket_id}/history` | MANAGER |

All six endpoints require authentication through the shared router dependency.

Four endpoints additionally use `Depends(require_manager)`.

Evidence: source-code inspection and isolated Docker clean-room RBAC tests. All four MANAGER-only endpoints returned HTTP 403 for an authenticated TECHNICIAN account (4/4 PASS). See the BT3 MANAGER RBAC Verification section below.

---

## BT3 – MANAGER RBAC Verification (4/4)

Environment: isolated Docker clean-room backend.

Test account: `bt3_rbac_test` (TECHNICIAN).

| Method | Endpoint | Expected | Actual | Result |
|---|---|---|---|---|
| POST | `/assignments/` | 403 | 403 | PASS |
| GET | `/assignments/ticket/1/reassignment-candidates` | 403 | 403 | PASS |
| PUT | `/assignments/ticket/1/reassign` | 403 | 403 | PASS |
| GET | `/assignments/ticket/1/history` | 403 | 403 | PASS |

**Result: 4/4 PASS.**

A temporary session was created and revoked after testing.

Scope: verifies that a TECHNICIAN account is denied access to four MANAGER-only endpoints. It does not verify successful MANAGER operations or all business response payloads.

---

## BT3 – Authenticated GET Response Verification (9/9)

Environment: isolated Docker clean-room backend.
Authentication: valid temporary TECHNICIAN session.

| Endpoint | HTTP status | JSON type | Result |
|---|---|---|---|
| GET `/tickets` | 200 | `list` | PASS |
| GET `/tickets/1` | 200 | `dict` | PASS |
| GET `/technicians` | 200 | `list` | PASS |
| GET `/technicians/1` | 200 | `dict` | PASS |
| GET `/appointments` | 200 | `list` | PASS |
| GET `/appointments/ticket/1` | 200 | `list` | PASS |
| GET `/appointments/context/1` | 200 | `dict` | PASS |
| GET `/assignments/eligible-technicians/1` | 200 | `list` | PASS |
| GET `/assignments/ticket/1/detail` | 200 | `dict` | PASS |

**Result: 9/9 PASS.**

The temporary authentication session was revoked.

Scope: HTTP status and top-level JSON type only.
Individual response fields, write operations and other error cases remain outside this test.

---

## BT3 – Verified GET Response Fields

Environment: isolated Docker clean-room backend.
Authentication: temporary TECHNICIAN session, revoked after testing.

| Endpoint | JSON type | Observed fields |
|---|---|---|
| GET `/tickets` | list | center_id, incident_group, is_assigned, priority, status, ticket_id, title |
| GET `/tickets/1` | object | center_id, incident_group, priority, status, ticket_id, title |
| GET `/technicians` | list | area, availability_status, center_id, name, technician_id |
| GET `/technicians/1` | object | area, availability_status, center_id, name, technician_id |
| GET `/appointments` | list | Empty list; item fields not verified |
| GET `/appointments/ticket/1` | list | Empty list; item fields not verified |
| GET `/appointments/context/1` | object | technician_id, technician_name, ticket_id, ticket_status, title |
| GET `/assignments/eligible-technicians/1` | list | area, availability_status, center_id, current_workload, incident_group, name, proficiency, technician_id |
| GET `/assignments/ticket/1/detail` | object | assignment, ticket_id, ticket_status |

**Result: 9/9 response structures inspected successfully.**

These are observed field names, not complete JSON response examples.
Nested assignment fields and empty appointment item schemas remain unverified.

---

## BT3 – Verified OpenAPI Schema Definitions

Source: exported FastAPI OpenAPI schema.
These definitions are declarations, not runtime payload examples.

### AppointmentInput

| Field | Type / schema | Required | Constraints |
|---|---|---|---|
| `ticket_id` | `integer` | Yes | `{}` |
| `appointment_type` | `string` | Yes | `{}` |
| `start_time` | `string` | Yes | `{}` |

### AssignmentCreate

| Field | Type / schema | Required | Constraints |
|---|---|---|---|
| `ticket_id` | `integer` | Yes | `{}` |
| `technician_id` | `integer` | Yes | `{}` |

### HTTPValidationError

| Field | Type / schema | Required | Constraints |
|---|---|---|---|
| `detail` | `array` | No | `{}` |

### LoginInput

| Field | Type / schema | Required | Constraints |
|---|---|---|---|
| `username` | `string` | Yes | `{"minLength": 1, "maxLength": 100}` |
| `password` | `string` | Yes | `{"minLength": 1}` |

### ReassignmentInput

| Field | Type / schema | Required | Constraints |
|---|---|---|---|
| `technician_id` | `integer` | Yes | `{}` |
| `reason` | `string` | Yes | `{"minLength": 1, "maxLength": 255}` |

### TechnicianInput

| Field | Type / schema | Required | Constraints |
|---|---|---|---|
| `name` | `string` | Yes | `{}` |
| `center_id` | `integer` | Yes | `{}` |
| `area` | `[{"type": "string"}, {"type": "null"}]` | No | `{}` |
| `availability_status` | `string` | Yes | `{}` |

### TicketInput

| Field | Type / schema | Required | Constraints |
|---|---|---|---|
| `title` | `string` | Yes | `{}` |
| `incident_group` | `string` | Yes | `{}` |
| `priority` | `string` | Yes | `{}` |
| `center_id` | `integer` | Yes | `{}` |

### ValidationError

| Field | Type / schema | Required | Constraints |
|---|---|---|---|
| `loc` | `array` | Yes | `{}` |
| `msg` | `string` | Yes | `{}` |
| `type` | `string` | Yes | `{}` |
| `input` | `other` | No | `{}` |
| `ctx` | `object` | No | `{}` |

---

## BT3 – Backend HTTP Error Audit

Source: static inspection of Python HTTPException calls in `src/backend`.

| HTTP status | Meaning | Source |
|---|---|---|
| 400 | Invalid appointment type, missing technician assignment, or appointment time not in the future | `appointment_api.py` |
| 401 | Authentication required, invalid/expired session, or invalid login credentials | `auth_api.py` |
| 403 | Insufficient permission for a manager-only assignment operation | `assignment_api.py` |
| 404 | Referenced ticket not found | `appointment_api.py`, `assignment_api.py` |
| 409 | Technician appointment time conflict | `appointment_api.py` |
| 503 | Database unavailable | `main.py` |
| 422 | Request validation error declared by FastAPI | OpenAPI schema |

**Static audit result:** 13 explicit `HTTPException` call sites identified.

This table documents observed source-code declarations. It does not establish that every error path has been exercised at runtime, nor does it exhaust errors raised by service-layer code.

Previously verified runtime evidence:
- Unauthenticated business GET requests: 11/11 returned HTTP 401.
- TECHNICIAN access to manager-only assignment operations: 4/4 returned HTTP 403.

---

## BT3 – Illustrative JSON Request Bodies

The following payloads are illustrative examples generated from declared OpenAPI fields.
They are NOT captured runtime requests and are NOT guaranteed to satisfy all business rules.

### POST /appointments

Schema: `AppointmentInput`

```json
{
  "ticket_id": 1,
  "appointment_type": "DELIVERY",
  "start_time": "2030-01-01T09:00:00"
}
```

### POST /appointments/check

Schema: `AppointmentInput`

```json
{
  "ticket_id": 1,
  "appointment_type": "DELIVERY",
  "start_time": "2030-01-01T09:00:00"
}
```

### POST /assignments/

Schema: `AssignmentCreate`

```json
{
  "ticket_id": 1,
  "technician_id": 1
}
```

### PUT /assignments/ticket/{ticket_id}/reassign

Schema: `ReassignmentInput`

```json
{
  "technician_id": 1,
  "reason": "Workload balancing"
}
```

### POST /auth/login

Schema: `LoginInput`

```json
{
  "username": "<REPLACE_WITH_USERNAME>",
  "password": "<REPLACE_WITH_PASSWORD>"
}
```

### POST /technicians

Schema: `TechnicianInput`

```json
{
  "name": "Example Technician",
  "center_id": 1,
  "area": "Example Area",
  "availability_status": "AVAILABLE"
}
```

### PUT /technicians/{technician_id}

Schema: `TechnicianInput`

```json
{
  "name": "Example Technician",
  "center_id": 1,
  "area": "Example Area",
  "availability_status": "AVAILABLE"
}
```

### POST /tickets

Schema: `TicketInput`

```json
{
  "title": "Example repair ticket",
  "incident_group": "HARDWARE",
  "priority": "CAO",
  "center_id": 1
}
```

### PUT /tickets/{ticket_id}

Schema: `TicketInput`

```json
{
  "title": "Example repair ticket",
  "incident_group": "HARDWARE",
  "priority": "CAO",
  "center_id": 1
}
```

---

## BT3 – Verified Request Business Rules

Source: static inspection of backend services and API validation.

| Field | Verified rule |
|---|---|
| `priority` | Must be `CAO`, `TRUNG_BINH`, or `THAP` |
| `incident_group` | Must be a non-empty string; no fixed enumeration found in ticket validation |
| `availability_status` | Must be `AVAILABLE`, `BUSY`, or `UNAVAILABLE` |
| `appointment_type` | Must be `DELIVERY` or `PICKUP` |
| `reason` | Required string, 1–255 characters according to OpenAPI |

**Important:** Assignment eligibility additionally depends on technician skills, availability, center, and workload rules. An illustrative JSON payload is not proof of a successful business operation.

---

## BT3 – Redacted GET Response Examples

The examples below preserve observed top-level field names and JSON container types.
The following are schema-shaped response illustrations, not captured JSON responses. Angle-bracket values describe expected types rather than literal values.
Nested objects and field value types have not all been independently verified.

### GET /tickets

```text
[
  {
    "ticket_id": "<integer>",
    "title": "<string>",
    "incident_group": "<string>",
    "priority": "<string>",
    "status": "<string>",
    "center_id": "<integer>",
    "is_assigned": "<boolean>"
  }
]
```

### GET /tickets/{ticket_id}

```text
{
  "ticket_id": "<integer>",
  "title": "<string>",
  "incident_group": "<string>",
  "priority": "<string>",
  "status": "<string>",
  "center_id": "<integer>"
}
```

### GET /technicians

```text
[
  {
    "technician_id": "<integer>",
    "name": "<string>",
    "center_id": "<integer>",
    "area": "<string or null>",
    "availability_status": "<string>"
  }
]
```

### GET /technicians/{technician_id}

```text
{
  "technician_id": "<integer>",
  "name": "<string>",
  "center_id": "<integer>",
  "area": "<string or null>",
  "availability_status": "<string>"
}
```

### GET /appointments

```text
[]
```

### GET /appointments/ticket/{ticket_id}

```text
[]
```

### GET /appointments/context/{ticket_id}

```text
{
  "ticket_id": "<integer>",
  "title": "<string>",
  "ticket_status": "<string>",
  "technician_id": "<integer or null>",
  "technician_name": "<string or null>"
}
```

### GET /assignments/eligible-technicians/{ticket_id}

```text
[
  {
    "technician_id": "<integer>",
    "name": "<string>",
    "center_id": "<integer>",
    "area": "<string or null>",
    "availability_status": "<string>",
    "incident_group": "<string>",
    "proficiency": "<integer>",
    "current_workload": "<integer>"
  }
]
```

### GET /assignments/ticket/{ticket_id}/detail

```text
{
  "ticket_id": "<integer>",
  "ticket_status": "<string>",
  "assignment": "<object or null>"
}
```

## BT3 – Verified Authentication API Contract

Source: src/backend/api/auth_api.py (lines 130–198).

| Endpoint | Authentication | Evidence |
|---|---|---|
| POST /auth/login | Public | Validates username and password |
| GET /auth/me | Required | Calls require_user(authorization) |
| POST /auth/logout | Required | Calls require_user(authorization) and revokes session |

Login success returns access_token, token_type, expires_at and user (user_id, username, role). Logout success returns a message confirming logout. These structures are derived from source code; runtime responses have not been verified here.
