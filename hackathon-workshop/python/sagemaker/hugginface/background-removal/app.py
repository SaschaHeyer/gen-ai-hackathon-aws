from flask import Flask, request, jsonify, Response
import torch
import numpy as np
from PIL import Image
from transformers import AutoModelForImageSegmentation
from torchvision.transforms.functional import normalize
import io

# Load the model
app = Flask(__name__)
model_id = "briaai/RMBG-1.4"
model = AutoModelForImageSegmentation.from_pretrained(model_id, trust_remote_code=True)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Health check endpoint
@app.route('/ping', methods=['GET'])
def ping():
    health = model is not None  # Simple health check
    status = 200 if health else 404
    return Response(status=status)

# Inference endpoint
@app.route('/invocations', methods=['POST'])
def invocations():
    # Read image bytes from the request
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image_file = request.files['image']
    image = Image.open(image_file.stream).convert("RGB")

    # Preprocess image
    orig_im_size = image.size
    model_input_size = [512, 512]
    image_tensor = preprocess_image(np.array(image), model_input_size).to(device)

    # Perform inference
    with torch.no_grad():
        result = model(image_tensor)

    # Post-process result
    result_image = postprocess_image(result[0][0], orig_im_size)
    pil_im = Image.fromarray(result_image)

    # Return processed image
    output = io.BytesIO()
    pil_im.save(output, format="PNG")
    output.seek(0)
    return Response(output, mimetype='image/png')

def preprocess_image(im: np.ndarray, model_input_size: list) -> torch.Tensor:
    if len(im.shape) < 3:
        im = im[:, :, np.newaxis]
    im_tensor = torch.tensor(im, dtype=torch.float32).permute(2, 0, 1)
    im_tensor = torch.nn.functional.interpolate(torch.unsqueeze(im_tensor, 0), size=model_input_size, mode='bilinear')
    image = torch.divide(im_tensor, 255.0)
    image = normalize(image, [0.5, 0.5, 0.5], [1.0, 1.0, 1.0])
    return image

def postprocess_image(result: torch.Tensor, im_size: list) -> np.ndarray:
    result = torch.squeeze(torch.nn.functional.interpolate(result, size=im_size, mode='bilinear'), 0)
    result = (result - result.min()) / (result.max() - result.min())
    im_array = (result * 255).permute(1, 2, 0).cpu().data.numpy().astype(np.uint8)
    return np.squeeze(im_array)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
