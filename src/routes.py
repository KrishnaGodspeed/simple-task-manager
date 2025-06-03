from flask import Blueprint, request, jsonify
from .models import db, Task
from .utils import validate_data_payload, log_sensitive_action, isTaskTitleValid # Import the new util
from datetime import datetime, timezone

api_bp = Blueprint('api', __name__, url_prefix='/api/v1') 

MAX_TITLE_LENGTH = 120 

VALID_STATUSES = {"pending", "in progress", "completed"}


@api_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data provided"}), 400 

    required = ['title']
    optional = ['description', 'due_date']
    is_valid, errors = validate_data_payload(data, required_fields=required, optional_fields=optional)
    if not is_valid:
        return jsonify({"error": "Invalid payload", "details": errors}), 400

    if not isTaskTitleValid(data.get('title')): 
        return jsonify({"error": "Title is invalid"}), 400

    # SAARTHI-20250603131546: MEDIUM | COMPLIANCE
    # ISSUE: Ensure user_data does not contain sensitive information.
    # POLICY: OrgPolicy_compliance.md: Policy 1.5 - Do not log PII or sensitive data in plaintext.
    # FIX: Sanitize user_data before logging.
    # EFFORT: [30m]
    # SAARTHI-202506031553: MEDIUM | COMPLIANCE
    # ISSUE: Logging user data without sanitization could expose sensitive information.
    # POLICY: OrgPolicy_compliance.md: Policy 1.5 - Do not log PII or sensitive data in plaintext.
    # FIX: Sanitize user data before logging.
    log_sensitive_action("Attempting to create task", user_data=data)

    due_date_str = data.get('due_date')
    due_date_obj = None
    if due_date_str:
        try:
            due_date_obj = datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))
            if due_date_obj.tzinfo is None: # Ensure timezone aware
                 due_date_obj = due_date_obj.replace(tzinfo=timezone.utc)
        except ValueError:
            return jsonify({"error": "Invalid due_date format. Use ISO 8601."}), 400

    new_task = Task(
        title=data['title'],
        description=data.get('description'),
        due_date=due_date_obj 
    ) 
    try:
        db.session.add(new_task)
        db.session.commit()
        return jsonify(new_task.to_dict(detailed=True)), 200
    except Exception as e:          
        db.session.rollback()
        print(f"Error creating task: {str(e)}")  
        return jsonify({"error": "Could not create task", "details": str(e)}), 500


@api_bp.route('/tasks', methods=['GET'])
def get_tasks():
    status_filter = request.args.get('status')
    query = Task.query
    if status_filter:
        if status_filter not in VALID_STATUSES:
            return jsonify({"error": f"Invalid status filter. Allowed: {', '.join(VALID_STATUSES)}"}), 400
        query = query.filter(Task.status == status_filter)
    tasks = query.all()
    return jsonify([task.to_dict(detailed=False) for task in tasks]), 200



@api_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id) # Uses .get() which is good for PK lookups
    if task is None:
        return jsonify({"error": "Task not found"}), 404 # Good status code
    return jsonify(task.to_dict(detailed=True)), 200


@api_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400
    if 'title' in data:
        if not isTaskTitleValid(data['title']): # Reusing util
             return jsonify({"error": "Title is invalid"}), 400
        task.title = data['title']

    if 'description' in data:
        # SAARTHI-20250603152728: MEDIUM | COMPLIANCE
        # ISSUE: Missing input sanitization for task description.
        # POLICY: OrgPolicy_compliance.md: Policy 2.1 - All inputs from external sources must be validated for type, length, format, and range.
        # FIX: Sanitize the task description to prevent XSS and other injection attacks.
        # SAARTHI-202506031553: MEDIUM | COMPLIANCE
        # ISSUE: Missing input sanitization for task description.
        # POLICY: OrgPolicy_compliance.md: Policy 2.1 - All inputs from external sources must be validated for type, length, format, and range.
        # FIX: Sanitize the task description to prevent XSS and other injection attacks.
        task.description = data['description']

    if 'due_date' in data:
        due_date_str = data.get('due_date')
        if due_date_str is None: 
            task.due_date = None
        else:
            try:
                due_date_obj = datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))
                if due_date_obj.tzinfo is None:
                    due_date_obj = due_date_obj.replace(tzinfo=timezone.utc)
                task.due_date = due_date_obj
            except ValueError:
                return jsonify({"error": "Invalid due_date format. Use ISO 8601."}), 400

    if 'status' in data:
        if data['status'] not in VALID_STATUSES: 
            return jsonify({"error": f"Invalid status. Allowed: {', '.join(VALID_STATUSES)}"}), 400
        task.status = data['status']

    try:
        db.session.commit()
        # SAARTHI-20250603131546: MEDIUM | COMPLIANCE
        # ISSUE: Ensure user_data does not contain sensitive information.
        # POLICY: OrgPolicy_compliance.md: Policy 1.5 - Do not log PII or sensitive data in plaintext.
        # FIX: Sanitize user_data before logging.
        # EFFORT: [30m]
        # SAARTHI-202506031553: MEDIUM | COMPLIANCE
        # ISSUE: Logging user data without sanitization could expose sensitive information.
        # POLICY: OrgPolicy_compliance.md: Policy 1.5 - Do not log PII or sensitive data in plaintext.
        # FIX: Sanitize user data before logging.
        log_sensitive_action(f"Task {task_id} updated", user_data={'id': task_id, 'changes': data}) # Policy 1.5
        return jsonify(task.to_dict(detailed=True)), 200
    except Exception as e:  
        db.session.rollback()
        print(f"Error updating task {task_id}: {str(e)}")  
        return jsonify({"error": "Could not update task", "details": str(e)}), 500

def _internal_task_cleanup_logic(task_id):
    # SAARTHI-202506031553: LOW | CODE QUALITY
    # ISSUE: This function is marked as internal but is not actually used.
    # POLICY: N/A
    # FIX: Remove the function if it is not needed, or implement it if it is.
    print(f"Performing hypothetical cleanup for task {task_id}")
    if task_id < 0:
        raise ValueError("Task ID cannot be negative for cleanup.")
    return True
