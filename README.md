# Design Doc Break Project

## Overview

The **Design Doc Break** project leverages **Inngest**, an event-driven platform, to automate the process of converting design documents into actionable project tasks. Inngest handles function orchestration based on specific events, such as the submission of a design doc, to trigger automated workflows. The project processes design docs and generates a CSV file containing task details that can be used for bulk Jira ticket creation.

## Design Doc Breakdown

The **Design Doc Breakdown** functionality is at the core of the project. Once a design document is submitted, the system parses it using **Anthropic**'s AI model to extract relevant details, including task descriptions, assignees, components, and estimated story points. After generating a CSV file, the system takes additional steps to sequence tasks based on the type of work (e.g., frontend vs. backend) and complexity. This ensures that tasks are organized and ready to be assigned in a way that optimizes team productivity.

The **CSV file** can be imported into Jira for bulk ticket creation, enabling teams to quickly start working without manually breaking down the design doc. While the project doesn’t create Jira tickets directly, the CSV output provides all the necessary data in a format that Jira can easily accept.

## Motivation

Breaking down design documents into digestible tasks, sequencing work by type (frontend or backend), and estimating relative complexity is a difficult and time-consuming task for tech leads. Parsing through long design docs, determining task assignments, and sequencing them effectively requires careful thought and significant effort. This process can delay the start of projects and lead to errors or inefficiencies.

The **Design Doc Break** project was created to automate and streamline this process. By using Inngest to trigger the breakdown of design documents into structured tasks and generating a CSV file for Jira, the project helps teams save time and reduce errors. The additional step of sequencing tasks based on their type and complexity ensures that work is organized efficiently, allowing teams to quickly transition from planning to execution.

## Tech/Framework Used

Key technologies used in this project:

- **Inngest**: An event-driven platform that triggers functions based on specific events, like the submission of a design doc.
- **Anthropic**: An AI model used to process and extract relevant information from the design doc, such as task descriptions and estimates.
- **FastAPI**: A modern web framework for building APIs in Python, used to handle requests and serve backend logic for the project.

## Features

The main features of **Design Doc Break** include:

- **Document Breakdown**: When a design doc is submitted, it is parsed and relevant information is extracted and organized into a CSV.
- **AI-Powered Parsing**: The **Anthropic** AI model processes the design document to identify tasks and other key details.
- **Task Sequencing**: After generating the CSV, the tasks are sequenced based on the type of work (e.g., frontend or backend) and their estimated complexity.
- **CSV Output**: The project generates a CSV file with task details, which can be imported into Jira for bulk ticket creation.
- **Optimized Task Organization**: The tasks are organized in a way that makes it easier for teams to distribute work and track progress.

## Installation

To set up **Design Doc Break**, follow these steps:

1. **Clone the repository**:

    ```
    git clone git@github.com:harrisjasmine/design_doc_agent.git
    cd design_doc_agent
    ```

2. **Create and activate a virtual environment**:

    ```
    python -m venv .venv && source .venv/bin/activate
    ```

3. **Install required dependencies**:

    ```
    pip install -r requirements.txt
    ```

## How to Run

After setting up your environment, follow these steps to run the project:

1. **Activate the virtual environment** (if not already activated):

    ```
    source .venv/bin/activate # assumes python 3 install
    ```

2. **Start your FastAPI app** in one terminal window:

    ```
    INNGEST_DEV=1 uvicorn main:app --reload
    ```

3. **Run the Inngest Dev Server** in another terminal window:

    ```
    npx inngest-cli@latest dev -u http://127.0.0.1:8000/api/inngest --no-discovery
    ```

4. Access the **Inngest Dev UI** on:

    ```
    http://localhost:8288/
    ```

5. To verify that your functions are running, navigate to the **Functions** section in the left menu. You should see:

    ```
    Function name: design_doc_breakdown
    Triggers: app/doc.submitted
    App: design_doc_agent
    App URL: http://localhost:8000/api/inngest
    ```

6. To generate the CSV containing task details and sequencing information, trigger an event by navigating to **Event**, then **Send Event** in the top right corner. Supply the following sample design doc in an event to trigger the design doc breakdown agent:

    ```json
    {
      "name": "app/doc.submitted",
      "data": {
        "file_url": "./design_doc_example.md"
      }
    }
    ```

7. To monitor function status, select **Runs** to view retries, errors, payloads, and more.

