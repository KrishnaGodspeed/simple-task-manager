# Organizational Policies & Compliance Framework

**Document Version:** 1.2
**Effective Date:** 2023-01-01

## Policy 1: Data Handling and Privacy (Inspired by GDPR-Lite)

**1.1. PII Definition:** Personally Identifiable Information (PII) includes any data that can be used to identify an individual. For the Task Manager, task `description` fields might inadvertently contain PII or sensitive project details.
    - **Action:** Exercise caution. User-related data (if added in future) is definitely PII.

**1.2. Data Minimization:** Only collect and store data essential for the service's functionality.
    - **Action:** Task fields should be relevant. Avoid storing unnecessary user agent strings, IP addresses unless explicitly required and justified for security. (Current Task Manager is okay here).

**1.3. Consent (for PII):** If collecting explicit PII directly related to users (e.g. email for notifications), clear consent must be obtained.
    - **Action:** Not directly applicable to current task-only model, but critical for future user features.

**1.4. Data Security in Transit & At Rest:**
    - **Transit:** All API communication must eventually be over HTTPS in production.
    - **At Rest:** Sensitive data (like passwords, if any) must be hashed using strong, modern algorithms (e.g., bcrypt, Argon2). Other PII should be encrypted if highly sensitive and stored long-term.
    - **Action:** Task descriptions are not currently encrypted at rest. Assess risk.

**1.5. Logging:** Do not log PII or sensitive data in plaintext.
    - **Action:** Review all logging statements. Be careful with logging full request/response payloads. Specifically, task descriptions should not be logged if they are deemed sensitive.

## Policy 2: API Security Standards

**2.1. Input Validation:** All inputs from external sources must be validated for type, length, format, and range.
    - **Action:** Implement strict validation for all request body fields and query parameters. Use whitelisting where possible.

**2.2. Output Encoding:** Ensure data sent to clients is properly encoded to prevent XSS if it's ever rendered directly in a browser without client-side sanitization. (Less critical for pure JSON APIs but good practice).
    - **Action:** Flask's `jsonify` typically handles this well for JSON.

**2.3. Authentication & Authorization (Future):**
    - Strong authentication mechanisms (e.g., JWT, OAuth2).
    - Principle of Least Privilege for authorization.
    - **Action:** Prepare for this. Currently, API is open.

**2.4. Error Handling:**
    - Do not expose detailed internal error messages or stack traces to the client.
    - Use generic error messages for clients, log details server-side.
    - **Action:** Ensure Flask `DEBUG` mode is `False` in production. Custom error handlers should return structured error JSON.

**2.5. Dependency Management:** Keep dependencies up-to-date to patch known vulnerabilities.
    - **Action:** Regularly review `requirements.txt` using tools like `pip-audit` or Snyk.

## Policy 3: Coding Standards

**3.1. Naming Conventions:**
    - Python: `snake_case` for functions, variables, and modules. `PascalCase` for classes.
    - **Action:** Enforce via linters and code reviews.

**3.2. Comments & Documentation:**
    - Public functions/classes/methods must have docstrings explaining purpose, arguments, and return values.
    - Complex logic blocks should have inline comments.
    - **Action:** Ensure adequate commenting.

**3.3. Code Complexity:**
    - Functions should be small and do one thing well.
    - Avoid deeply nested control structures.
    - **Action:** Monitor cyclomatic complexity. Refactor large functions.

**3.4. Hardcoding:** Avoid hardcoding configuration values (e.g., API keys, secret strings, server addresses). Use configuration files or environment variables.
    - **Action:** `SECRET_KEY`, `DATABASE_URL` are in `.env`. Check for other instances.

**3.5. Linting & Formatting:**
    - Adhere to PEP 8.
    - Use automated tools like Black for formatting and Flake8 for linting.
    - **Action:** Integrate linters into development workflow. (Project should have some minor violations for Saarthi).

## Policy 4: Testing

**4.1. Unit Tests:** Core business logic and utility functions must have unit tests.
    - **Action:** Aim for >70% unit test coverage for new critical modules.

**4.2. Integration Tests:** API endpoints should have integration tests covering common success and failure scenarios.
    - **Action:** Ensure key API flows are tested.

## Compliance Checklist Reference for Saarthi

- [ ] GDPR-P1.1: PII in task descriptions considered?
- [ ] GDPR-P1.4: Task descriptions encrypted at rest if sensitive?
- [ ] GDPR-P1.5: Task descriptions or other potentially sensitive data avoided in logs?
- [ ] SEC-P2.1: All API inputs robustly validated?
- [ ] SEC-P2.4: No stack traces in production error responses?
- [ ] CODE-P3.1: Naming conventions followed?
- [ ] CODE-P3.2: Adequate docstrings and comments?
- [ ] CODE-P3.3: Function complexity manageable?
- [ ] CODE-P3.4: No hardcoded sensitive values or config?
- [ ] CODE-P3.5: PEP 8 and linter compliance?
- [ ] TEST-P4.1/P4.2: Sufficient test coverage?
- [ ] PRD-FR-010: Task filtering implemented?
- [ ] TLD-5.2: Get All Tasks response matches TLD fields?
