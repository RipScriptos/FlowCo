"""API endpoints for FlowCo business evaluation."""

import logging
import uuid
from typing import Optional, Dict, Any
from pathlib import Path
import asyncio
from datetime import datetime

from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Query, Response
from fastapi.responses import FileResponse
from pydantic import BaseModel, ValidationError

from ..models.business import BusinessConcept, Demographics, ProductInfo, BusinessCategory, IncomeRange
from ..models.evaluation import EvaluationResult
from ..core.engine import BusinessEvaluationEngine
from ..output.report_generator import ReportGenerator
from ..output.template_generator import TemplateGenerator
from ..core.config import config

logger = logging.getLogger(__name__)

# Initialize components
engine = BusinessEvaluationEngine()
report_generator = ReportGenerator()
template_generator = TemplateGenerator()

# In-memory storage for demo (use database in production)
evaluation_cache: Dict[str, Dict[str, Any]] = {}

router = APIRouter()


class EvaluationRequest(BaseModel):
    """Request model for business evaluation."""
    concept_description: str
    business_model: Optional[str] = None
    target_demographics: Demographics
    product_info: ProductInfo
    competitive_advantages: list[str] = []
    funding_requirements: Optional[str] = None
    timeline: Optional[str] = None


class EvaluationResponse(BaseModel):
    """Response model for evaluation submission."""
    evaluation_id: str
    status: str
    message: str


@router.post("/evaluate", response_model=EvaluationResponse)
async def evaluate_business_concept(request: EvaluationRequest):
    """
    Evaluate a business concept.
    
    Args:
        request: Business concept evaluation request
        
    Returns:
        Evaluation response with ID for tracking
    """
    try:
        # Generate unique evaluation ID
        evaluation_id = str(uuid.uuid4())
        
        # Create business concept
        business_concept = BusinessConcept(
            concept_description=request.concept_description,
            target_demographics=request.target_demographics,
            product_info=request.product_info,
            business_model=request.business_model,
            competitive_advantages=request.competitive_advantages,
            funding_requirements=request.funding_requirements,
            timeline=request.timeline
        )
        
        # Store initial status
        evaluation_cache[evaluation_id] = {
            "status": "processing",
            "concept": business_concept,
            "result": None,
            "created_at": datetime.now(),
            "progress": 0
        }
        
        # Start evaluation in background
        asyncio.create_task(process_evaluation(evaluation_id, business_concept))
        
        return EvaluationResponse(
            evaluation_id=evaluation_id,
            status="processing",
            message="Evaluation started. Use the evaluation ID to check status and retrieve results."
        )
        
    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Invalid input data: {str(e)}")
    except Exception as e:
        logger.error(f"Error starting evaluation: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to start evaluation")


@router.get("/status/{evaluation_id}")
async def get_evaluation_status(evaluation_id: str):
    """
    Get evaluation status.
    
    Args:
        evaluation_id: Evaluation ID
        
    Returns:
        Current status of the evaluation
    """
    if evaluation_id not in evaluation_cache:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    
    evaluation = evaluation_cache[evaluation_id]
    
    return {
        "evaluation_id": evaluation_id,
        "status": evaluation["status"],
        "progress": evaluation.get("progress", 0),
        "created_at": evaluation["created_at"].isoformat(),
        "completed_at": evaluation.get("completed_at", {}).isoformat() if evaluation.get("completed_at") else None
    }


@router.get("/results/{evaluation_id}")
async def get_evaluation_results(evaluation_id: str):
    """
    Get evaluation results.
    
    Args:
        evaluation_id: Evaluation ID
        
    Returns:
        Complete evaluation results
    """
    if evaluation_id not in evaluation_cache:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    
    evaluation = evaluation_cache[evaluation_id]
    
    if evaluation["status"] == "processing":
        raise HTTPException(status_code=202, detail="Evaluation still in progress")
    
    if evaluation["status"] == "error":
        raise HTTPException(status_code=500, detail="Evaluation failed")
    
    if evaluation["result"] is None:
        raise HTTPException(status_code=404, detail="Results not available")
    
    return evaluation["result"].dict()


@router.get("/report/{evaluation_id}")
async def download_report(
    evaluation_id: str,
    format: str = Query("pdf", regex="^(pdf|html|markdown|json)$")
):
    """
    Download evaluation report in specified format.
    
    Args:
        evaluation_id: Evaluation ID
        format: Report format (pdf, html, markdown, json)
        
    Returns:
        Report file
    """
    if evaluation_id not in evaluation_cache:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    
    evaluation = evaluation_cache[evaluation_id]
    
    if evaluation["status"] != "completed" or evaluation["result"] is None:
        raise HTTPException(status_code=400, detail="Evaluation not completed")
    
    try:
        # Generate report
        concept = evaluation["concept"]
        result = evaluation["result"]
        
        # Create temporary file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"business_evaluation_{evaluation_id}_{timestamp}.{format}"
        output_path = Path("temp") / filename
        output_path.parent.mkdir(exist_ok=True)
        
        # Generate report based on format
        if format == "json":
            report_content = await report_generator.generate_report(
                concept, result, format="json", output_path=str(output_path)
            )
        else:
            await report_generator.generate_report(
                concept, result, format=format, output_path=str(output_path)
            )
        
        # Determine media type
        media_types = {
            "pdf": "application/pdf",
            "html": "text/html",
            "markdown": "text/markdown",
            "json": "application/json"
        }
        
        return FileResponse(
            path=str(output_path),
            filename=filename,
            media_type=media_types.get(format, "application/octet-stream")
        )
        
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate report")


@router.get("/landing-page/{evaluation_id}")
async def generate_landing_page(evaluation_id: str):
    """
    Generate landing page for the business concept.
    
    Args:
        evaluation_id: Evaluation ID
        
    Returns:
        Generated landing page HTML
    """
    if evaluation_id not in evaluation_cache:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    
    evaluation = evaluation_cache[evaluation_id]
    
    if evaluation["status"] != "completed" or evaluation["result"] is None:
        raise HTTPException(status_code=400, detail="Evaluation not completed")
    
    try:
        concept = evaluation["concept"]
        result = evaluation["result"]
        
        html_content = await template_generator.generate_landing_page(concept, result)
        
        return Response(content=html_content, media_type="text/html")
        
    except Exception as e:
        logger.error(f"Error generating landing page: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate landing page")


@router.post("/evaluate-with-image")
async def evaluate_with_image(
    concept_description: str = Form(...),
    business_model: Optional[str] = Form(None),
    product_name: Optional[str] = Form(None),
    product_description: Optional[str] = Form(None),
    product_category: Optional[str] = Form(None),
    product_features: Optional[str] = Form(None),
    age_min: int = Form(...),
    age_max: int = Form(...),
    income_range: str = Form(...),
    location: str = Form(...),
    interests: Optional[str] = Form(None),
    gender: Optional[str] = Form(None),
    education_level: Optional[str] = Form(None),
    competitive_advantages: Optional[str] = Form(None),
    funding_requirements: Optional[str] = Form(None),
    timeline: Optional[str] = Form(None),
    product_image: Optional[UploadFile] = File(None)
):
    """
    Evaluate business concept with optional image upload.
    
    This endpoint accepts form data including an optional image file.
    """
    try:
        # Process image if provided
        image_data = None
        if product_image:
            image_data = await product_image.read()
        
        # Parse lists from form data
        features_list = []
        if product_features:
            features_list = [f.strip() for f in product_features.split('\n') if f.strip()]
        
        advantages_list = []
        if competitive_advantages:
            advantages_list = [a.strip() for a in competitive_advantages.split('\n') if a.strip()]
        
        interests_list = []
        if interests:
            interests_list = [i.strip() for i in interests.split(',') if i.strip()]
        
        # Create business concept
        demographics = Demographics(
            age_min=age_min,
            age_max=age_max,
            income_range=IncomeRange(income_range),
            location=location,
            interests=interests_list,
            gender=gender,
            education_level=education_level
        )
        
        product_info = ProductInfo(
            name=product_name,
            description=product_description,
            category=BusinessCategory(product_category) if product_category else None,
            features=features_list,
            image_data=image_data
        )
        
        business_concept = BusinessConcept(
            concept_description=concept_description,
            target_demographics=demographics,
            product_info=product_info,
            business_model=business_model,
            competitive_advantages=advantages_list,
            funding_requirements=funding_requirements,
            timeline=timeline
        )
        
        # Generate unique evaluation ID
        evaluation_id = str(uuid.uuid4())
        
        # Store initial status
        evaluation_cache[evaluation_id] = {
            "status": "processing",
            "concept": business_concept,
            "result": None,
            "created_at": datetime.now(),
            "progress": 0
        }
        
        # Start evaluation in background
        asyncio.create_task(process_evaluation(evaluation_id, business_concept))
        
        return EvaluationResponse(
            evaluation_id=evaluation_id,
            status="processing",
            message="Evaluation started with image analysis."
        )
        
    except Exception as e:
        logger.error(f"Error processing evaluation with image: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process evaluation")


@router.get("/summary/{evaluation_id}")
async def get_evaluation_summary(evaluation_id: str):
    """
    Get a summary of evaluation results for quick viewing.
    
    Args:
        evaluation_id: Evaluation ID
        
    Returns:
        Summary of evaluation results
    """
    if evaluation_id not in evaluation_cache:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    
    evaluation = evaluation_cache[evaluation_id]
    
    if evaluation["status"] != "completed" or evaluation["result"] is None:
        raise HTTPException(status_code=400, detail="Evaluation not completed")
    
    try:
        concept = evaluation["concept"]
        result = evaluation["result"]
        
        summary = await report_generator.generate_summary_report(concept, result)
        return summary
        
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate summary")


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "ai_available": engine.ai_client.is_available(),
        "timestamp": datetime.now().isoformat()
    }


async def process_evaluation(evaluation_id: str, business_concept: BusinessConcept):
    """
    Process business evaluation in background.
    
    Args:
        evaluation_id: Unique evaluation ID
        business_concept: Business concept to evaluate
    """
    try:
        logger.info(f"Starting evaluation {evaluation_id}")
        
        # Update progress
        evaluation_cache[evaluation_id]["progress"] = 10
        
        # Perform evaluation
        result = await engine.evaluate_business_concept(business_concept)
        
        # Update progress
        evaluation_cache[evaluation_id]["progress"] = 100
        
        # Store result
        evaluation_cache[evaluation_id].update({
            "status": "completed",
            "result": result,
            "completed_at": datetime.now()
        })
        
        logger.info(f"Evaluation {evaluation_id} completed successfully")
        
    except Exception as e:
        logger.error(f"Evaluation {evaluation_id} failed: {str(e)}")
        evaluation_cache[evaluation_id].update({
            "status": "error",
            "error": str(e),
            "completed_at": datetime.now()
        })