import uuid

import httpx

SD_SERVICE_URL = "65.108.32.156"

while True:
    r = httpx.post(
        f"http://{SD_SERVICE_URL}:3000/txt2img",
        json={
            "prompt": "anamuseme in style of fullmetal alchemist",
            "guidance_scale": 12,
            "num_inference_steps": 45,
            "safety_check": False,
        },
        timeout=30,
    )

    if r.status_code == 200:
        new_filename = f"{uuid.uuid4().hex[:8]}.jpg"
        print(new_filename)
        with open(f"trash/{new_filename}", 'wb') as f:
            # r.content.decode_content = True
            f.write(r.content)
