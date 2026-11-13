# Smart CRM – Security Checklist

**Project:** Smart CRM – Mekong Mobile (L4)
**Assessment date:** November 10, 2026
**Scope:** FastAPI backend, SQLite, Docker deployment and authentication

## Security Assessment

| No. | Security Criterion | Status | Evidence and Assessment |
|---|---|---|---|
| 1 | Secrets and environment configuration | CHƯA LÀM | `.env` is excluded by `.gitignore` and `.dockerignore`. The current `.env.example` uses a password placeholder. A private strong password must be configured before deployment. Historical Git revisions and complete secret exposure have not yet been fully audited. |
| 2 | Input validation and SQL injection prevention | CHƯA LÀM | Pydantic models validate API inputs. Parameterized SQLite queries are used in the authentication module and repository code. Complete validation and SQL query coverage have not been independently verified. |
| 3 | Authentication and authorization | CHƯA LÀM | Protected API routes require authentication. Four unauthenticated GET requests returned HTTP 401. Manager-only checks exist for assignment operations. Complete role-based and resource-level authorization has not been verified. |
| 4 | Password hashing and session security | ĐÃ LÀM | Passwords use PBKDF2-HMAC-SHA256 with 600,000 iterations and random salts. Session tokens are generated using `secrets.token_urlsafe(32)`, stored as SHA-256 hashes, expire after 8 hours, and support revocation on logout. |
| 5 | Safe error handling | CHƯA LÀM | HTTP 401, 403 and 404 responses are implemented. The healthcheck handles SQLite errors. A complete review of exception messages and internal error exposure remains pending. |
| 6 | Safe logging | CHƯA LÀM | No comprehensive logging security review has been completed. Sensitive values, passwords and authentication tokens must not be written to application logs. |
| 7 | Dependency security | CHƯA LÀM | Python dependencies are pinned to exact versions in `requirements.txt`. A dependency vulnerability audit and frontend dependency review have not yet been completed. |

## Authentication Test Evidence

**Test date:** November 10, 2026

The following API endpoints were requested without an authentication token:

| Endpoint | Expected | Actual | Result |
|---|---|---|---|
| `GET /tickets` | HTTP 401 | HTTP 401 | PASS |
| `GET /technicians` | HTTP 401 | HTTP 401 | PASS |
| `GET /appointments` | HTTP 401 | HTTP 401 | PASS |
| `GET /assignments/eligible-technicians/1` | HTTP 401 | HTTP 401 | PASS |

**Result: 4/4 protected endpoints returned HTTP 401.**

Evidence: The original 4/4 HTTP 401 test results are recorded above. The expanded 11/11 HTTP 401 results are recorded in the BT3 verification section below. No dedicated screenshot is claimed.

Additional authentication verification:

- Manager login returned HTTP 200.
- An access token was issued successfully.
- Authenticated `GET /auth/me` returned HTTP 200.
- The authenticated role was verified as `MANAGER`.
- Authentication was also tested through the clean-room Nginx reverse proxy.

## Known Limitations and Recommendations

1. Replace demonstration credentials with private credentials before deployment.
2. Use HTTPS when exposing the application beyond local development.
3. Review authorization rules for every role and sensitive resource.
4. Audit all input validation and SQL queries.
5. Review exception handling and ensure internal error details are not exposed.
6. Verify that application and proxy logs do not contain credentials or access tokens.
7. Run dependency vulnerability scans and review frontend packages.
8. Consider restricting direct backend port exposure in a production environment.
9. Add login rate limiting and additional session security controls for production use.

## Conclusion

Smart CRM implements foundational security controls, including password hashing, token-based authentication, protected API routes, and environment file exclusions.

The unauthenticated API security test passed all four selected cases.

However, several security controls require further verification or hardening. This checklist documents the verified implementation and its remaining limitations.

**Overall assessment:** Suitable for the verified local academic demonstration; not certified or hardened for production deployment.

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
