from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from celery.result import AsyncResult
from celery_app import celery_app, process_topic

app = FastAPI()

class TopicRequest(BaseModel):
    topic: str

@app.post("/tasks")
async def create_task(topic_request: TopicRequest):
    topic = topic_request.topic
    task = process_topic.delay(topic)
    return {"task_id": task.id}

@app.get("/tasks/{task_id}")
async def get_task(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    if task_result.state == 'PENDING':
        return {"status": "Processing"}
    elif task_result.state == 'SUCCESS':
        return {"status": "Completed", "summary": task_result.result}
    else:
        return {"status": task_result.state}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
