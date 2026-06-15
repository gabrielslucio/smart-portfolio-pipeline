import sys
import requests

def main():
    # Inputs do GitHub Actions
    project_id = sys.argv[1]
    project_source = sys.argv[2]
    pipeline_type = sys.argv[3]
    pipeline_id = sys.argv[4]
    project_name = sys.argv[5]
    project_status = sys.argv[6]

    print("Running analysis... ")

    # Lógica simples

    # Summary
    summary = f"Project '{project_name}' is currently in status '{project_status}'."

    # Risk report
    if project_status.lower() != "active":
        risk_report = "Project may be at risk due to inactive status."
    else:
        risk_report = "No major risks detected."

    print("Summary:", summary)
    print("Risk Report:", risk_report)

    # Callback to OutSystems
    callback_url = "https://personal-fspba94p-dev.outsystems.app/SmartPortfolioManager_APP/rest/PipelineCallback/receive"

    payload = {
        "PipelineId": pipeline_id,
        "Status": project_status,
        "Summary": summary,
        "RiskReport": risk_report,
        "ErrorMessage": "",
        "WorkflowRunUrl": "https://github.com/gabrielslucio/smart-portfolio-pipeline/actions"
    }

    print("Payload:", payload)

    try:
        response = requests.post(callback_url, json=payload, timeout=30)
        print("Callback response:", response.status_code)
        print(response.text)
        response.raise_for_status()  # Raise an error for bad responses
    
    except Exception as e:
        print("Error during callback:", str(e))

if __name__ == "__main__":
    main()