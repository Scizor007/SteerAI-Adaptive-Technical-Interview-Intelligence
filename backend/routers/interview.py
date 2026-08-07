"""
Interview router.
Single POST /api/interview endpoint as defined in the technical specification.
"""

from fastapi import APIRouter, HTTPException

from models.schemas import InterviewRequest, InterviewResponse
from modules.interview_manager import InterviewManager

router = APIRouter()

interview_manager = InterviewManager()


@router.post("/api/interview", response_model=InterviewResponse)
async def interview(request: InterviewRequest) -> InterviewResponse:
    """
    Unified interview endpoint.

    Handles three phases:
    1. Start — sessionId + candidate object → initialize session, return first question
    2. Continue — sessionId + message → evaluate response, return next question
    3. End — automatically triggered when interview is complete → return feedback
    """
    try:
        # Phase 1: Start a new interview
        if request.candidate is not None:
            return await interview_manager.start_interview(
                session_id=request.sessionId,
                candidate=request.candidate,
            )

        # Phase 2 & 3: Continue or end
        if request.message is not None:
            return await interview_manager.continue_interview(
                session_id=request.sessionId,
                message=request.message,
            )

        raise HTTPException(
            status_code=400,
            detail="Request must include either 'candidate' (to start) or 'message' (to continue).",
        )

    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"Session '{request.sessionId}' not found. Start a new interview first.",
        )
