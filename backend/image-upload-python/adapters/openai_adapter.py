import os
from typing import Dict, Optional
from openai import OpenAI

class StrideAPI:
    def __init__(self, api_key: Optional[str] = None,
                 text_model: str = "gpt-4o",
                 image_model: str = "gpt-image-1"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        
        if not self.api_key:
            raise RuntimeError("Defina OPENAI_API_KEY no ambiente ou passe api_key no construtor.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.text_model = text_model
        self.image_model = image_model


    def analyze_text(self, image_base64: str, max_tokens: int = 1500) -> str:
        """
        Retorna apenas o texto (análise STRIDE) do modelo.
        """
        
        PROMPT_ANALYSE = """
        Você é um analista de cibersegurança especializado em STRIDE.
        Analise a imagem fornecida e descreva detalhadamente os possíveis riscos de segurança
        usando o modelo STRIDE (Spoofing, Tampering, Repudiation, Information Disclosure,
        Denial of Service, Elevation of Privilege). Responda em português (pt-BR).
        Forneça a resposta em formato markdown, com seções claras para cada categoria STRIDE.
        Inclua exemplos específicos observados na imagem e sugestões de mitigação.
        Use a imagem fornecida para fundamentar sua análise.
        Seja detalhado e técnico, adequado para um público de profissionais de segurança.
        """
        
        
        resp = self.client.chat.completions.create(
            model=self.text_model,
            messages=[
                {
                    "role": "system",
                    "content": "Você é um analista de cibersegurança especializado em STRIDE. "
                               "Responda em português (pt-BR)."
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{image_base64}"}
                        },
                        {
                            "type": "text",
                            "text": PROMPT_ANALYSE
                        }
                    ]
                }
            ],
            max_tokens=max_tokens
        )
        return resp.choices[0].message.content or ""

    def analyze_and_annotate(self, image_base64: str, prompt: str) -> Dict[str, Optional[str]]:
        """
        Conveniência: realiza duas análises sobre a mesma imagem:
        1. Overlay de anotações (retorna como string/json)
        2. Markdown detalhado da análise STRIDE

        Retorna um dicionário:
        {
            "markdown": str,
            "overlay": str
        }
        """
        
        # Chamada para gerar o overlay/anotações
        overlay_resp = self.client.chat.completions.create(
            model=self.text_model,
            messages=[
                {
                    "role": "system",
                    "content": "Você é um analista de cibersegurança especializado em STRIDE. "
                               "Forneça respostas em português (pt-BR)."
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}"}},
                        {"type": "text", "text": prompt}
                    ]
                }
            ],
            max_tokens=1500
        )

        overlay_content = overlay_resp.choices[0].message.content or ""

        # Segunda chamada: retorna markdown detalhado
        markdown_content = self.analyze_text(image_base64)

        return  markdown_content, overlay_content
