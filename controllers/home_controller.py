from fastapi import APIRouter, Request
from schemas.api_response import APIResponse

router = APIRouter(prefix="/home", tags=["Home"])

class HomeController:
    def __init__(self):
        self.router = router
        self.setup_routes()

    def setup_routes(self):
        @self.router.get("/", 
                          response_model=APIResponse, 
                          status_code=200,
                          response_model_exclude_none=True,
                          summary="API Home",
                          description="Welcome to API Home",)
        async def home(request: Request = None) -> APIResponse:
            return APIResponse(
                status=True,
                message="Connection successfully",
                data="Welcome to Beef Recognition API"
            )
   
        