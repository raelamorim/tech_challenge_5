import traceback
import azure.functions as func
import json
from services.image_service import ImageService
from services.mock_image_service import MockImageService
from services.live_image_service import LiveImageService

# service: ImageService = MockImageService()
service: ImageService = LiveImageService()

app = func.FunctionApp()

@app.route(route="ai-arch-review/image-upload", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def UploadImage(req: func.HttpRequest) -> func.HttpResponse:
    print("Executando UploadImage com retorno de imagem e markdown")

    try:
        uploaded_file = req.get_json().get('image') 
        response_body = service.get_image_and_markdown(uploaded_file)
    except FileNotFoundError as e:
        return func.HttpResponse(str(e), status_code=404)
    except Exception as e:
        print("Erro inesperado:", e)
        traceback.print_exc()
        return func.HttpResponse("Erro interno", status_code=500)

    return func.HttpResponse(
        json.dumps(response_body, ensure_ascii=False),
        mimetype="application/json",
        status_code=200
    )