import runpod

def handler(job):
    """
    Handler function for RunPod serverless endpoint.
    Processes requests from the local bridge and returns responses.
    
    Args:
        job: Job object containing input data
        
    Returns:
        str or dict: Response to be sent back to the client
    """
    # Extract input from job
    job_input = job["input"]
    prompt = job_input.get("prompt", "No prompt provided")
    
    # Process the prompt (you can add your custom logic here)
    response = f"GPU Received your message: {prompt}"
    
    # Return the response
    # The response will be automatically wrapped in the RunPod response format
    return response

runpod.serverless.start({"handler": handler})