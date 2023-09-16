from fastapi import APIRouter, status, Response, Header, Security
from lib.indexer import Indexer
from lib.response import ResponseObj
from lib.document import Document
from lib.question import Question
from core.log_config import logger
from core.auth import get_api_key
import time

# Create a router to allow for endpoints
router = APIRouter()

@router.get("/health", tags=["APIv1", "health"])
def health():
    logger.debug("Health check called")
    return {"status": "ok"}

@router.get("/index/{name}", tags=["APIv1", "index"])
async def get_index(name, apikey: str = Security(get_api_key)) -> ResponseObj:
    """
        Determine if the index already exists
    """

    if name == "":
        return {"status": "error", "message": "Index name cannot be empty"}
    
    idx_status = Indexer().get_index(name)

    resp = ResponseObj()
    resp.status = idx_status
    resp.name = name
    resp.message = "Index status"
    return resp

@router.post("/index/{name}", tags=["APIv1", "index"])
async def create_index(name, response: Response, apikey: str = Security(get_api_key)) -> ResponseObj:
    """
        Create an index, but check if it already exists
    """

    resp = ResponseObj()

    # Create an instance of the Indexer
    try:
        idx = Indexer()
    except Exception as e:
        resp.error = True
        resp.message = str(e)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return resp
    
    # Check to see if the nbde index already exists
    idx_status = Indexer().get_index(name)

    if idx_status:
        resp.message = "Index already exists"
        resp.status = True
        resp.name = name
        response.status_code = status.HTTP_409_CONFLICT
        return resp
    else:
        resp.message = "Index created"
        resp.status = True
        resp.name = name
        response.status_code = status.HTTP_201_CREATED
        return resp

@router.put("/index/{name}", tags=["APIv1", "index"])
def index_document(
    name,
    document: Document,
    response: Response,
    content_type: str = Header(None),
    x_content_encoding: str = Header(None),
    apikey: str = Security(get_api_key)
) -> ResponseObj:
    """
        Submit a document to the API and index it in the search service
    """

    resp = ResponseObj()

    # if the content-type is not JSON reject the request
    if content_type != "application/json":
        resp.error = True
        resp.message = "Content type must be application/json"
        response.status_code = status.HTTP_400_BAD_REQUEST
        return resp

    # Add the document to the index
    result = Indexer().index(name, document, x_content_encoding)

    return result

@router.post("/question", tags=["APIv1", "question"])
def ask_question(
    question: Question,
    response: Response,
    content_type: str = Header(None),
    apikey: str = Security(get_api_key)
) -> ResponseObj:
    """
        Ask a question of the indexed documents
    """

    resp = ResponseObj()

    # if the content-type is not JSON reject the request
    if content_type != "application/json":
        resp.error = True
        resp.message = "Content type must be application/json"
        response.status_code = status.HTTP_400_BAD_REQUEST
        return resp

    # Ask the question and return the results
    start_time = time.time()

    try:
        resp.message = question.ask()
        resp.status = True
    except Exception as e:
        resp.error = True
        resp.message = str(e)

    end_time = time.time()
    resp.duration = end_time - start_time
    
    return resp

