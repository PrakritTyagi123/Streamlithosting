import base64

def load_image_base64(image_path):
    if not image_path.exists():
        return None

    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")
