from fastapi import APIRouter, Depends, File, Request
from schemas.api_response import APIResponse
from schemas.recognition_schema import RecognitionRequest, RecognitionResponse
from services.recognition_service import RecognitionService
from services.efficientnetb0_service import Efficientnetb0Service
from exceptions.custom_exception import CustomException
from fastapi import Depends
from utils.jwt_bearer import JWTBearer

# public_router = APIRouter(prefix="/train", tags=["Training"])
router = APIRouter(prefix="/train", tags=["Training"])
# router = APIRouter(prefix="/train", tags=["Training"], dependencies=[Depends(JWTBearer())])

class TrainingController:
    def __init__(self):
        self.router = router
        # self.public_router = public_router
        self.setup_routes()

    def setup_routes(self):
        @self.router.get("/", 
                          response_model=APIResponse, 
                          status_code=201,
                          response_model_exclude_none=True,
                          summary="Training model",
                          description="Training beef recognition model",)
        async def training(request: Request = None) -> APIResponse:
            service = Efficientnetb0Service()
            history, model_name = service.train_model(2)
            return APIResponse(
                status=True,
                message="Training successfully",
                data=model_name
            )
   
        