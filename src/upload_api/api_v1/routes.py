from fastapi import APIRouter, Response, BackgroundTasks, UploadFile, File, status, Security
from lib.upload import Upload
from lib.response import ResponseObj
from core.log_config import logger
from core.auth import get_api_key

# Create router to allow endpoints
router = APIRouter()

# Create a health endpoint
@router.get("/health", tags=["APIv1", "health"])
def health():
    logger.debug("Health check called")
    return {"status": "ok"}

# Create route to allow for upload of files
@router.post("/upload/{folder_name}", tags=["APIv1", "upload"])
async def upload(
    folder_name: str,
    response: Response,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    apikey: str = Security(get_api_key)
):
    
    upload = Upload()
    resp = ResponseObj()

    # check the content type
    if file.content_type not in upload.filetypes:
        response.status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
        resp.set(True, f"Unsupported file type, must be one of: {upload.get_types()}", file.filename)
        return resp

    resp = upload.accept(file, response, folder_name)

    # ensure that the additional processes for the file are run in the background
    background_tasks.add_task(upload.process)

    return resp
