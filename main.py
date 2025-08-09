from fastapi import FastAPI
from inngest import Inngest, TriggerEvent, RetryAfterError, NonRetriableError, Context
import inngest.fast_api
from inngest.experimental.ai.anthropic import Adapter as AnthropicAdapter
import logging

logger = logging.getLogger("uvicorn.inngest")
logger.setLevel(logging.DEBUG)
# Initialize Inngest client
inngest_client = Inngest(
    app_id="design_doc_agent",
    logger=logger,
    is_production=False,
)

# Inngest Function: design_doc_breakdown
@inngest_client.create_function(
    fn_id="design_doc_breakdown",
    trigger=TriggerEvent(event="app/doc.submitted"),
)
async def design_doc_breakdown(ctx: Context) -> str:
    ctx.logger.info(ctx.event)

    try:
        adapter = AnthropicAdapter(
            auth_key="your-anthropic-api-key",  # Replace with your actual API key
            model="claude-3-5-sonnet-20230601"
        )
        
        with open(ctx.event.data['file_url'], 'r') as file:
            design_doc_content = file.read()

        # Step AI: Task breakdown
        task_breakdown_prompt = (
            "Pretend you are a technical project manager. I will give a design document "
            "containing project summary, architecture, and requirements. Create a task breakdown "
            "for implementing the solution. For each task provide a summary, description, story points, "
            "assignee type (backend or frontend), issue type. The output should be a CSV containing "
            "the previous elements as columns.\n\n"
            f"Design Document:\n{design_doc_content}"
        )

        csv_task_breakdown = await ctx.step.ai.infer(
            step_id="breakdown_design_doc",
            adapter=adapter,
            body={ 
                "prompt": task_breakdown_prompt,
                "max_tokens": 2000
            },
        )

        # Step AI: Task sequencing
        sequencing_prompt = (
            "Using the following task breakdown, paying close attention to assignee type, story points, "
            "and description, create a sequence of tasks that can be executed in parallel or sequentially. "
            "The output should be a CSV with columns: summary, description, story points, "
            "assignee type (backend or frontend), issue type ordered by sequence of tasks.\n\n"
            f"Task Breakdown CSV:\n{csv_task_breakdown}"
        )

        sequencing_breakdown = await ctx.step.ai.infer(
            step_id="convert_breakdown_to_csv",
            adapter=adapter,
            body={
                "prompt": sequencing_prompt,
                "max_tokens": 2000
            },
        )

        return sequencing_breakdown

    except FileNotFoundError:
        ctx.logger.error(f"File not found: {ctx.event.data['file_url']}")
        raise RetryAfterError("file not present - retrying in 10 seconds", 10000)
    except PermissionError:
        ctx.logger.error(f"Permission denied when accessing: {ctx.event.data.file_url}")
        raise NonRetriableError("permission denied - missing required file permissions")
    except Exception as e:
        ctx.logger.error(f"An error occurred while reading the file: {e}")
        raise e


# Initialize FastAPI app
app = FastAPI()

# Register Inngest functions with FastAPI
inngest.fast_api.serve(
    app=app,
    client=inngest_client,
    functions=[design_doc_breakdown],
)

"""
Example event to trigger:
{
  "name": "app/doc.submitted",
  "data": {
    "file_url": "./design_doc_example.md"
  }
}
"""
