from datetime import datetime, timezone

def get_current_utc_time():
    return datetime.now(timezone.utc)

# SAARTHI-20250603131546: MEDIUM | CODE_QUALITY
# ISSUE: validate_data_payload lacks specific type checks or format checks.
# POLICY: N/A
# FIX: Add specific type checks and format checks to the validate_data_payload function.
# EFFORT: [2h]
def validate_data_payload(data, required_fields, optional_fields=None):
    """
    Validates the data payload against required and optional fields.

    Args:
        data (dict): The data payload to validate.
        required_fields (list): A list of required fields.
        optional_fields (list, optional): A list of optional fields. Defaults to None.

    Returns:
        tuple: A tuple containing a boolean indicating whether the payload is valid and a dictionary of errors, if any.
    """
    if not isinstance(data, dict):
        return False, "Payload must be a JSON object."

    errors = {}
    for field in required_fields:
        if field not in data or not data[field]: 
            errors[field] = f"{field} is required and cannot be empty."

    allowed_fields = set(required_fields)
    if optional_fields:
        allowed_fields.update(optional_fields)

    for key in data.keys():
        if key not in allowed_fields:
            errors[key] = f"Field '{key}' is not allowed."

    if errors:
        return False, errors 

    return True, None

def log_sensitive_action(action_description, user_data=None):
    """
    Logs an action. If user_data is provided, it's logged too.
    This could be a compliance issue if user_data contains PII.
    """
    timestamp = get_current_utc_time().isoformat()
    log_message = f"[{timestamp}] Action: {action_description}"
    if user_data:
        log_message += f" | Data: {str(user_data)}"
    # SAARTHI-202506031226: HIGH | Compliance
        # ISSUE: Logging user_data directly could expose PII, violating GDPR-Lite.
        # POLICY: Policy 1.5: Do not log PII or sensitive data in plaintext.
        # FIX: Sanitize or redact user_data before logging. Use app.logger.warning instead of print.
        # EFFORT: [4h]
        # SAARTHI-202506031554: HIGH | COMPLIANCE
        # ISSUE: Logging user_data directly could expose PII, violating GDPR-Lite.
        # POLICY: OrgPolicy_compliance.md: Policy 1.5 - Do not log PII or sensitive data in plaintext.
        # FIX: Sanitize or redact user_data before logging. Use app.logger.warning instead of print.
        print(log_message)

# SAARTHI-20250603131546: LOW | Code Quality
# ISSUE: Unreachable code.
        # POLICY: Policy 3.3: Avoid unnecessary code.
        # FIX: Remove the unreachable code block.
        # EFFORT: [5m]
        # SAARTHI-202506031554: LOW | CODE QUALITY
        # ISSUE: Unreachable code.
        # POLICY: N/A
        # FIX: Remove the unreachable code block.
        if False:
            print("This will never be printed.")


# SAARTHI-202506031554: LOW | LINTING
# ISSUE: Function name does not follow the snake_case naming convention.
# POLICY: OrgPolicy_compliance.md: Policy 3.1 - Python: `snake_case` for functions, variables, and modules.
# FIX: Rename the function to is_task_title_valid.
# EFFORT: [5m]
def is_task_title_valid(title: str) -> bool:
    if not title:
        return False
    if len(title) > 120: 
        return False
    return True
