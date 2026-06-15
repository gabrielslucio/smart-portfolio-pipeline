import sys
import requests
import os

# Fetch project overview from OutSystems API
def get_project_overview(project_id):
    url = f"https://personal-fspba94p-dev.outsystems.app/SmartPortfolioManager_APP/rest/GetProjectById/projects/{project_id}/overview"

    print(f"Fetching project data from ODC: {url}")

    response = requests.get(url, timeout=30)
    response.raise_for_status()  # Raise an error for bad responses

    return response.json()

# Generate summary
def generate_summary(project_name, project_status, total_tasks, completed_tasks, overdue_tasks):
    progress = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0

    summary = f"""
Project '{project_name}' is currently '{project_status}' with {progress}% completion.

Out of {total_tasks} tasks:
- {completed_tasks} are completed
- {overdue_tasks} are overdue
"""

    if overdue_tasks > 0:
        summary += "\nThere are overdue tasks that require immediate attention."
    else:
        summary += "\nThe project is progressing smoothly with no overdue tasks."

    return summary.strip()

# Generate risk report
def generate_risk(project_status, overdue_tasks, progress):
    risks = []

    if project_status.lower() != "active":
        risks.append("Project is not active which may indicate delays or blockers.")

    if overdue_tasks > 0:
        risks.append(f"There are {overdue_tasks} overdue tasks requiring attention.")

    if progress < 50:
        risks.append("Project progress is below 50%, indicating potential delays.")

    if not risks:
        return "No major risks detected."

    return " ".join(risks)


def main():
    # Inputs from GitHub Actions
    project_id = sys.argv[1]
    project_source = sys.argv[2]
    pipeline_type = sys.argv[3]
    pipeline_id = sys.argv[4]
    project_name = sys.argv[5]
    project_status = sys.argv[6]

    print("Starting pipeline analysis...")
    print(f"Project: {project_name}")
    print(f"Status: {project_status}")

    try:
        #Fetch real data
        overview = get_project_overview(project_id)

        total_tasks = overview.get("TotalTasks", 0)
        completed_tasks = overview.get("CompletedTasks", 0)
        overdue_tasks = overview.get("OverdueTasks", 0)
        progress = overview.get("Progress", 0)

        print("Project metrics:")
        print(f"Total Tasks: {total_tasks}")
        print(f"Completed Tasks: {completed_tasks}")
        print(f"Overdue Tasks: {overdue_tasks}")
        print(f"Progress: {progress}%")

        # ✅ Generate insights
        print(" Generating summary...")
        summary = generate_summary(
            project_name,
            project_status,
            total_tasks,
            completed_tasks,
            overdue_tasks
        )
        print(summary)

        print("Generating risk report...")
        risk_report = generate_risk(project_status, overdue_tasks, progress)
        print(risk_report)

        #Build GitHub run URL
        run_url = f"https://github.com/gabrielslucio/smart-portfolio-pipeline/actions/runs/{os.environ.get('GITHUB_RUN_ID')}"

        #Callback to OutSystems
        callback_url = "https://personal-fspba94p-dev.outsystems.app/SmartPortfolioManager_APP/rest/PipelineCallback/receive"

        payload = {
            "PipelineId": int(pipeline_id),
            "Status": "Completed",
            "Summary": summary,
            "RiskReport": risk_report,
            "ErrorMessage": "",
            "WorkflowRunUrl": run_url
        }

        print("Sending callback payload:")
        print(payload)

        response = requests.post(callback_url, json=payload, timeout=30)
        print("Callback response:", response.status_code)
        print(response.text)

        response.raise_for_status()

    except Exception as e:
        print("Error during pipeline execution:", str(e))

        #Send failure callback
        try:
            fail_payload = {
                "PipelineId": int(pipeline_id),
                "Status": "Failed",
                "Summary": "",
                "RiskReport": "",
                "ErrorMessage": str(e),
                "WorkflowRunUrl": ""
            }

            requests.post(callback_url, json=fail_payload, timeout=10)

        except Exception as callback_error:
            print("Failed to send error callback:", str(callback_error))


#ENTRY POINT
if __name__ == "__main__":
    main()
