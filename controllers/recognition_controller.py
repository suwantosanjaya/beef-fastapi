from fastapi import APIRouter, Depends, File, Request, UploadFile
from schemas.api_response import APIResponse
from schemas.recognition_schema import RecognitionRequest, RecognitionResponse
from services.recognition_service import RecognitionService
from exceptions.custom_exception import CustomException
from fastapi import Depends

public_router = APIRouter(prefix="/recognition", tags=["Recognition"])
# router = APIRouter(prefix="/institusi", tags=["Institusi"], dependencies=[Depends(JWTBearer())])

class RecognitionController:
    def __init__(self):
        # self.router = router
        self.public_router = public_router
        self.setup_routes()

    def setup_routes(self):
        @self.public_router.post("/", 
                          response_model=APIResponse, 
                          status_code=201,
                          response_model_exclude_none=True,
                          summary="Recognition beef",
                          description="Recognize beef using the provided data and image",)
        async def recognition(
            # form_data: RecognitionRequest = Depends(RecognitionRequest.as_form),
            image: UploadFile = File(None),
            request: Request = None
        ) -> APIResponse:
            if image and image.size > 1024 * 1024:  # 1 MB
                raise CustomException(
                    status_code=400, 
                    message="image file size must be <= 1 MB"
                )
            service = RecognitionService()
            # result = service.recognition(form_data, image)
            result = service.recognition(image)
            # result = service.recognition(image)
            return APIResponse(
                status=True,
                message="Recognition successfully",
                data=result
            )
   
        