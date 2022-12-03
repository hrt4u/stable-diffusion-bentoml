import uuid

import httpx

SD_SERVICE_URL = "65.108.33.79"

while True:
    r = httpx.post(
        f"http://{SD_SERVICE_URL}:3000/txt2img",
        json={
            "prompt": "joyfreeze Anaglyph Artstation",
            "negative_prompt": "fat, cropped face, ugly, deformed, deformity, ugliness",
            "guidance_scale": 15,
            "num_inference_steps": 42,
            "safety_check": False,
            # "height": 752,
        },
        timeout=60,
    )

    if r.status_code == 200:
        new_filename = f"{uuid.uuid4().hex[:8]}.jpg"
        print(new_filename)
        with open(f"trash/{new_filename}", 'wb') as f:
            # r.content.decode_content = True
            f.write(r.content)
    else:
        print("error code: ", r.status_code, r.json())
