import torch
from torch import autocast
from diffusers import StableDiffusionPipeline
from diffusers import StableDiffusionImg2ImgPipeline

import bentoml
from bentoml.io import Image, JSON, Multipart

class StableDiffusionRunnable(bentoml.Runnable):
    SUPPORTED_RESOURCES = ("nvidia.com/gpu", )
    SUPPORTS_CPU_MULTI_THREADING = True

    def __init__(self):
        model_id = "./models/v1_4_fp16"
        self.device = "cuda"

        txt2img_pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16, revision="fp16")
        self.txt2img_pipe = txt2img_pipe.to(self.device)

        self.img2img_pipe = StableDiffusionImg2ImgPipeline(
            vae=self.txt2img_pipe.vae,
            text_encoder=self.txt2img_pipe.text_encoder,
            tokenizer=self.txt2img_pipe.tokenizer,
            unet=self.txt2img_pipe.unet,
            scheduler=self.txt2img_pipe.scheduler,
            safety_checker=self.txt2img_pipe.safety_checker,
            feature_extractor=txt2img_pipe.feature_extractor,
        ).to(self.device)

    @bentoml.Runnable.method(batchable=False, batch_dim=0)
    def txt2img(self, input_data):
        prompt = input_data["prompt"]
        with autocast(self.device):
            images = self.txt2img_pipe(prompt, guidance_scale=7.5).images
            image = images[0]
            return image


    @bentoml.Runnable.method(batchable=False, batch_dim=0)
    def img2img(self, img, data):
        prompt = data["prompt"]
        with autocast(self.device):
            images = self.img2img_pipe(
                prompt=prompt,
                init_image=img,
                strength=0.75,
                guidance_scale=7.5
            ).images
            image = images[0]
            return image
                    

stable_diffusion_runner = bentoml.Runner(StableDiffusionRunnable, max_batch_size=10)

svc = bentoml.Service("stable_diffusion_demo_fp16", runners=[stable_diffusion_runner])

@svc.api(input=JSON(), output=Image())
def txt2img(input_data):
    return stable_diffusion_runner.txt2img.run(input_data)

img2img_input_spec = Multipart(img=Image(), data=JSON())
@svc.api(input=img2img_input_spec, output=Image())
def img2img(img, data):
    return stable_diffusion_runner.img2img.run(img, data)