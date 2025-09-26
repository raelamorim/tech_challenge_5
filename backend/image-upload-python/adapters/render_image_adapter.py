import json, io, os, base64
from typing import Any, Dict, Tuple
from PIL import Image, ImageDraw, ImageFont

def render_overlay_on_image(
    image_base64: str,
    overlay_spec: Any,
    min_font_px: int = 14
) -> str:
    """
    Desenha as anotações do overlay_spec na imagem (base64) e salva em out_path.
    overlay_spec pode ser: list | dict | str(JSON).
    Retorna o caminho salvo.
    """
    if isinstance(overlay_spec, str):
        overlay_spec = json.loads(overlay_spec)
    if isinstance(overlay_spec, dict):
        if "items" in overlay_spec:
            items = overlay_spec["items"]
        elif "annotations" in overlay_spec:
            items = overlay_spec["annotations"]
        elif all(k in overlay_spec for k in ("bbox", "short_label_pt")):
            items = [overlay_spec]
        else:
            items = []
    elif isinstance(overlay_spec, list):
        items = overlay_spec
    else:
        items = []

    img = Image.open(io.BytesIO(base64.b64decode(image_base64))).convert("RGBA")
    W, H = img.size
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", size=max(min_font_px, int(max(W, H)*0.018)))
    except Exception:
        font = ImageFont.load_default()

    box_color  = (255, 0, 0, 255)
    line_color = (255, 0, 0, 255)
    call_bg    = (255, 255, 255, 235)
    call_fg    = (0, 0, 0, 255)
    box_w      = max(2, int(max(W, H)*0.003))
    pad        = max(6, int(max(W, H)*0.006))

    def denorm(b: Dict[str, float]) -> Tuple[int,int,int,int]:
        x = int(b.get("x",0)*W); y = int(b.get("y",0)*H)
        w = max(1, int(b.get("w",0)*W)); h = max(1, int(b.get("h",0)*H))
        return x, y, w, h

    def callout_rect(x:int,y:int,w:int,h:int, anchor:str, text:str)->Tuple[Tuple[int,int,int,int],Tuple[int,int]]:
        tx0, ty0, tx1, ty1 = draw.textbbox((0,0), text, font=font)
        tw, th = (tx1-tx0), (ty1-ty0)
        cw, ch = tw + 2*pad, th + 2*pad

        anchor = (anchor or "right").lower()
        if anchor == "top":
            cx, cy = x, y - ch - pad; tip = (x + w//2, y)
        elif anchor == "bottom":
            cx, cy = x, y + h + pad;   tip = (x + w//2, y + h)
        elif anchor == "left":
            cx, cy = x - cw - pad, y;  tip = (x, y + h//2)
        else:  # right
            cx, cy = x + w + pad, y;   tip = (x + w, y + h//2)

        cx = max(0, min(cx, W - cw))
        cy = max(0, min(cy, H - ch))
        return (cx, cy, cx+cw, cy+ch), tip

    for it in items:
        bbox = it.get("bbox", {})
        stride = it.get("stride", [])
        label  = it.get("short_label_pt") or it.get("label_pt") or it.get("label") or ""
        anchor = it.get("anchor", "right")

        tag = f"[{','.join(stride)}] " if stride else ""
        text = (tag + label).strip()

        x, y, w, h = denorm(bbox)
        draw.rectangle((x, y, x+w, y+h), outline=box_color, width=box_w)

        rect, tip = callout_rect(x, y, w, h, anchor, text)
        draw.rounded_rectangle(rect, radius=8, fill=call_bg, outline=box_color, width=1)
        draw.text((rect[0]+pad, rect[1]+pad), text, fill=call_fg, font=font)

        cx, cy = (rect[0]+rect[2])//2, (rect[1]+rect[3])//2
        draw.line((cx, cy, tip[0], tip[1]), fill=line_color, width=max(1, box_w-1))

    img = img.convert("RGB")
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_base64_out = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return img_base64_out
