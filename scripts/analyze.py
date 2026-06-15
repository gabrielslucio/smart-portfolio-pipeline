import sys

def main():
    # Inputs do GitHub Actions
    project_id = sys.argv[1]
    project_source = sys.argv[2]
    pipeline_type = sys.argv[3]
    correlation_id = sys.argv[4]
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

if __name__ == "__main__":
    main()