import logging
import traceback
import azure.functions as func
import json
from services.image_service import ImageService
from services.mock_image_service import MockImageService
from services.live_image_service import LiveImageService

# service: ImageService = MockImageService()
service: ImageService = LiveImageService()

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Executando function com método %s", req.method)
    
    # Responde preflight
    if req.method == "OPTIONS":
        return func.HttpResponse(
            "Empty body",
            status_code=200,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, x-functions-key",
                "Access-Control-Max-Age": "86400"
            }
        )

    # POST normal
    logging.info("Executando UploadImage com retorno de imagem e markdown")

    try:
        # Pega o JSON da requisição
        data = req.get_json()
        uploaded_file = data.get("image")
        logging.info(f"Arquivo recebido: {uploaded_file is not None}")
        
        response_body = service.get_image_and_markdown(uploaded_file)
    except FileNotFoundError as e:
        logging.error(f"Arquivo não encontrado: {e}")
        return func.HttpResponse(str(e), status_code=404)
    except Exception as e:
        logging.error("Erro inesperado")
        logging.error(traceback.format_exc())
        return func.HttpResponse(
            "Erro interno", 
            status_code=500,
            headers={
                "Access-Control-Allow-Origin": "*"
            }
        )

    return func.HttpResponse(
        json.dumps(response_body, ensure_ascii=False),
        mimetype="application/json",
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*"
        }
    )