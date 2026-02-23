import os
import logging
import traceback
from typing import Optional
import azure.functions as func

from libs.github import (
    Authentication as GitHubAuth,
    Organization as GitHubOrg,
    Repository as GitHubRepo,
    Issue as GitHubIssue,
)

from libs.ado import (
    Authentication as AdoAuth,
    Organization as AdoOrg,
    WorkItem as AdoWorkItem,
)

from libs.utils import (
    create_json_response,
    validate_env_vars,
    log_info,
    log_error,
)

from libs.adoghsync import AdoGitHubSync

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the Function App with V2 programming model
app = func.FunctionApp()


def initialize_gh_objects(repo_name: str) -> tuple[GitHubRepo, Optional[func.HttpResponse]]:
    """Initialize GitHub objects."""
    log_info(f"\nInitializing GitHub objects for repo: {repo_name}")
    try:
        gh_auth = GitHubAuth(os.environ['GITHUB_TOKEN'])
        gh_org = GitHubOrg(os.environ['GITHUB_ORG'], gh_auth)
        gh_repo = GitHubRepo(repo_name, gh_org, gh_auth)
        gh_repo.valid_repo()
        return gh_repo, None

    except Exception as e:
        log_error(f"Error initializing GitHub objects: {str(e)}")
        return None, create_json_response({
            "status": "error",
            "message": f"Failed to initialize GitHub objects: {str(e)}"
        }, 400)


def initialize_ado_objects(work_item_id) -> tuple[AdoWorkItem, Optional[func.HttpResponse]]:
    """Initialize ADO objects."""
    log_info(f"\n\nInitializing ADO objects for work item ID: {work_item_id}")
    try:
        ado_auth = AdoAuth(os.environ['ADO_TOKEN'])
        ado_org = AdoOrg(os.environ['ADO_ORG'], ado_auth)
        ado_wi = AdoWorkItem(work_item_id, ado_org, ado_auth)
        return ado_wi, None

    except Exception as e:
        log_error(f"Error initializing ADO objects: {str(e)}")
        return None, create_json_response({
            "status": "error",
            "message": f"Failed to initialize ADO objects: {str(e)}"
        }, 400)


def work_item_created_event(payload, ado_github_sync: AdoGitHubSync):
    work_item_id = str(payload['resource']['id'])
    log_info(f"Work Item ID: {work_item_id}")
    ado_wi, error_response = initialize_ado_objects(work_item_id)
    if error_response:
        return error_response

    repo_name = payload['resource']['fields'].get('Custom.GitHubRepository', '').strip()
    gh_repo, error_response = initialize_gh_objects(repo_name)
    if error_response:
        return error_response

    title = payload['resource']['fields']['System.Title']
    ado_wi.set_attr('title', title)
    description = payload['resource']['fields'].get('System.Description', '')
    ado_wi.set_attr('description', description)

    return ado_github_sync.ado_wi_created_trigger(gh_repo, ado_wi)


def work_item_updated_event(payload, ado_github_sync: AdoGitHubSync):
    work_item_id = str(payload['resource']['workItemId'])
    log_info(f"Work Item ID: {work_item_id}")
    ado_wi, error_response = initialize_ado_objects(work_item_id)
    if error_response:
        return error_response

    repo_name = payload['resource']['revision']['fields'].get('Custom.GitHubRepository', '').strip()
    gh_repo, error_response = initialize_gh_objects(repo_name)
    if error_response:
        return error_response

    title = payload['resource']['revision']['fields']['System.Title']
    ado_wi.set_attr('title', title)
    description = payload['resource']['revision']['fields'].get('System.Description', '')
    ado_wi.set_attr('description', description)

    issue_number = payload['resource']['revision']['fields'].get("Custom.GitHubIssueNumber")
    if not issue_number:
        # If no issue number, create new issue
        return ado_github_sync.ado_wi_created_trigger(gh_repo, ado_wi)

    # Update existing issue
    gh_issue = GitHubIssue(int(issue_number), gh_repo)
    return ado_github_sync.ado_wi_updated_trigger(gh_issue, ado_wi, payload)


@app.route(route="AdoGitHubSync", methods=["POST"])
def ado_github_sync(req: func.HttpRequest) -> func.HttpResponse:
    """
    Azure Function HTTP trigger for syncing ADO work items with GitHub issues.

    This function handles webhooks from Azure DevOps when work items are
    created or updated, and automatically creates or updates corresponding
    GitHub issues.

    Args:
        req: HTTP request containing ADO webhook payload

    Returns:
        HTTP response with success/error status and details
    """
    try:
        log_info("\nAzure Function HTTP trigger started processing request")

        ado_github_sync = AdoGitHubSync()

        # Parse and validate ADO payload
        log_info("Parsing and validating ADO payload")
        payload, payload_error = ado_github_sync.parse_and_validate_ado_payload(req)
        if payload_error:
            return payload_error

        try:
            event_type = payload["eventType"]
            log_info(f"\nProcessing {event_type}")

            ####################################
            # Main Operations
            ####################################
            if event_type == "workitem.created":
                return work_item_created_event(payload, ado_github_sync)
            elif event_type == "workitem.updated":
                return work_item_updated_event(payload, ado_github_sync)
        except Exception as e:
            action = "updating" if event_type == "workitem.updated" else "creating"
            log_error(f"Error {action} GitHub issue: {str(e)}")
            return create_json_response({
                "status": "error",
                "message": f"Failed to {action[:-3]}e GitHub issue: {str(e)}",
            }, 201)

    except Exception as e:
        log_error(f"Unexpected error in main function: {str(e)}")
        log_error(f"Traceback: {traceback.format_exc()}")

        return create_json_response({
            "status": "error",
            "message": "Internal server error"
        }, 201)


# Health check endpoint for monitoring
@app.route(route="health", methods=["GET"], auth_level="anonymous")
def health_check(req: func.HttpRequest) -> func.HttpResponse:

    log_info("\nHealth check endpoint called")
    # Validate required environment variables
    env_error = validate_env_vars(["GITHUB_TOKEN", "GITHUB_ORG",
                                   "ADO_TOKEN", "ADO_ORG"])
    if env_error:
        return env_error

    gh_auth = GitHubAuth(os.environ['GITHUB_TOKEN'])
    try:
        gh_auth.validate_token()
    except Exception as e:
        log_error(f"GitHub token validation error: {str(e)}")
        return create_json_response({
            "status": "error",
            "message": f"GitHub token validation error: {str(e)}"
        }, 500)

    ado_auth = AdoAuth(os.environ['ADO_TOKEN'])
    try:
        ado_auth.validate_token()
    except Exception as e:
        log_error(f"ADO token validation error: {str(e)}")
        return create_json_response({
            "status": "error",
            "message": f"ADO token validation error: {str(e)}"
        }, 500)

    """Health check endpoint for monitoring the function app."""
    return create_json_response({
        "status": "healthy",
        "message": "ADO-GitHub Sync Function App is running",
        "version": "2.0",
        "model": "v2"
    })