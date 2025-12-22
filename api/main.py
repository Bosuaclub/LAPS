"""
FastAPI Backend for Vercel Deployment

Simple REST API wrapper around FAO-Sim core functionality.
This allows deployment to Vercel as serverless functions.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import json
import uuid
from pathlib import Path

from faosim.core.schemas import UserConstraints, OptimizationResult
from faosim.core.orchestrator import FAOSimOrchestrator

app = FastAPI(
    title="FAO-Sim API",
    description="Facebook Ads Optimization & Simulation API",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage (for demo - use Redis/DB in production)
optimization_jobs = {}


class OptimizationRequest(BaseModel):
    """Request model for optimization."""
    config: Dict[str, Any]
    use_existing_kb: bool = True


class OptimizationResponse(BaseModel):
    """Response model for optimization."""
    job_id: str
    status: str
    message: str


class JobStatus(BaseModel):
    """Job status response."""
    job_id: str
    status: str  # pending, running, completed, failed
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "FAO-Sim API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/api/optimize", response_model=OptimizationResponse)
async def start_optimization(
    request: OptimizationRequest,
    background_tasks: BackgroundTasks
):
    """
    Start a new optimization job.

    Note: Due to Vercel's 10-second timeout, this returns a job ID.
    Use /api/status/{job_id} to check progress.
    """
    try:
        # Parse user constraints
        user_constraints = UserConstraints(**request.config)

        # Generate job ID
        job_id = str(uuid.uuid4())

        # Initialize job status
        optimization_jobs[job_id] = {
            "status": "pending",
            "result": None,
            "error": None
        }

        # Start background optimization
        background_tasks.add_task(
            run_optimization,
            job_id,
            user_constraints,
            request.use_existing_kb
        )

        return OptimizationResponse(
            job_id=job_id,
            status="pending",
            message="Optimization started. Check status at /api/status/{job_id}"
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/status/{job_id}", response_model=JobStatus)
async def get_job_status(job_id: str):
    """Get the status of an optimization job."""
    if job_id not in optimization_jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    job = optimization_jobs[job_id]

    return JobStatus(
        job_id=job_id,
        status=job["status"],
        result=job["result"],
        error=job["error"]
    )


@app.get("/api/results/{job_id}")
async def get_results(job_id: str):
    """Get the full results of a completed optimization."""
    if job_id not in optimization_jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    job = optimization_jobs[job_id]

    if job["status"] != "completed":
        raise HTTPException(
            status_code=400,
            detail=f"Job is {job['status']}, not completed"
        )

    return job["result"]


@app.post("/api/validate")
async def validate_config(config: Dict[str, Any]):
    """Validate a configuration without running optimization."""
    try:
        user_constraints = UserConstraints(**config)
        return {
            "valid": True,
            "message": "Configuration is valid",
            "constraints": user_constraints.model_dump()
        }
    except Exception as e:
        return {
            "valid": False,
            "message": str(e)
        }


def run_optimization(
    job_id: str,
    user_constraints: UserConstraints,
    use_existing_kb: bool
):
    """
    Run optimization in background.

    Note: This won't work well on Vercel due to timeout limits.
    Consider using a dedicated worker service (Railway, Render, etc.)
    """
    try:
        # Update status
        optimization_jobs[job_id]["status"] = "running"

        # Initialize orchestrator
        orchestrator = FAOSimOrchestrator(
            user_constraints=user_constraints,
            knowledge_base_docs=None,
            use_existing_kb=use_existing_kb
        )

        # Setup
        orchestrator.setup()

        # Run optimization
        result = orchestrator.run_optimization()

        # Convert to dict
        result_dict = result.model_dump()

        # Store result
        optimization_jobs[job_id]["status"] = "completed"
        optimization_jobs[job_id]["result"] = result_dict

    except Exception as e:
        optimization_jobs[job_id]["status"] = "failed"
        optimization_jobs[job_id]["error"] = str(e)


# For Vercel deployment
app = app
