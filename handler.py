import runpod

def handler(job):
    # This is the 'brain' that receives your phone commands
    job_input = job["input"]
    prompt = job_input.get("prompt", "No prompt provided")
    
    return f"GPU Received your message: {prompt}"

runpod.serverless.start({"handler": handler})