"""
Local Bridge Script - Communicate with RunPod GPU Endpoint
============================================================

This script allows you to send requests from your local machine to your RunPod GPU endpoint.

SETUP INSTRUCTIONS:
1. Get your RunPod API Key from: https://www.runpod.io/console/user/settings
2. Get your Endpoint ID from your RunPod Serverless endpoint
3. Replace the placeholder values below with your actual credentials
"""

import requests
import json
import time
import sys

# ============================================================================
# CONFIGURATION - REPLACE THESE VALUES WITH YOUR ACTUAL CREDENTIALS
# ============================================================================

# Your RunPod API Key (get it from: https://www.runpod.io/console/user/settings)
RUNPOD_API_KEY = "YOUR_API_KEY_HERE"

# Your RunPod Endpoint ID (get it from your serverless endpoint)
RUNPOD_ENDPOINT_ID = "YOUR_ENDPOINT_ID_HERE"

# ============================================================================
# DO NOT MODIFY BELOW THIS LINE UNLESS YOU KNOW WHAT YOU'RE DOING
# ============================================================================

def send_request(prompt, max_wait_time=60):
    """
    Send a request to the RunPod GPU endpoint.
    
    Args:
        prompt (str): The text prompt to send to the GPU
        max_wait_time (int): Maximum time to wait for response in seconds
    
    Returns:
        dict: Response from the GPU endpoint
    """
    
    # Validate configuration
    if RUNPOD_API_KEY == "YOUR_API_KEY_HERE":
        print("ERROR: You need to set your RUNPOD_API_KEY in local_bridge.py")
        print("Get your API key from: https://www.runpod.io/console/user/settings")
        sys.exit(1)
    
    if RUNPOD_ENDPOINT_ID == "YOUR_ENDPOINT_ID_HERE":
        print("ERROR: You need to set your RUNPOD_ENDPOINT_ID in local_bridge.py")
        print("Find your endpoint ID in your RunPod serverless endpoint dashboard")
        sys.exit(1)
    
    # Construct the RunPod endpoint URL
    endpoint_url = f"https://api.runpod.ai/v2/{RUNPOD_ENDPOINT_ID}/run"
    
    # Prepare headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {RUNPOD_API_KEY}"
    }
    
    # Prepare the request payload
    payload = {
        "input": {
            "prompt": prompt
        }
    }
    
    print(f"Sending request to GPU endpoint...")
    print(f"Prompt: {prompt}")
    
    try:
        # Send the request
        response = requests.post(endpoint_url, json=payload, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        
        # Check if we got a job ID (async response)
        if "id" in result:
            job_id = result["id"]
            print(f"Job submitted! ID: {job_id}")
            print(f"Waiting for result...")
            
            # Poll for the result
            return poll_for_result(job_id, max_wait_time)
        else:
            # Direct response
            return result
            
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Failed to send request to RunPod endpoint")
        print(f"Details: {str(e)}")
        
        if hasattr(e, 'response') and e.response is not None:
            print(f"Status Code: {e.response.status_code}")
            try:
                error_detail = e.response.json()
                print(f"Error Details: {json.dumps(error_detail, indent=2)}")
            except:
                print(f"Response Text: {e.response.text}")
        
        print("\nTroubleshooting:")
        print("1. Check that your RUNPOD_API_KEY is correct")
        print("2. Check that your RUNPOD_ENDPOINT_ID is correct")
        print("3. Make sure your endpoint is deployed and active in RunPod")
        print("4. Verify you have an active internet connection")
        sys.exit(1)


def poll_for_result(job_id, max_wait_time=60):
    """
    Poll the RunPod endpoint for job results.
    
    Args:
        job_id (str): The job ID to poll
        max_wait_time (int): Maximum time to wait in seconds
    
    Returns:
        dict: The job result
    """
    status_url = f"https://api.runpod.ai/v2/{RUNPOD_ENDPOINT_ID}/status/{job_id}"
    
    headers = {
        "Authorization": f"Bearer {RUNPOD_API_KEY}"
    }
    
    start_time = time.time()
    
    while True:
        elapsed_time = time.time() - start_time
        
        if elapsed_time > max_wait_time:
            print(f"ERROR: Request timed out after {max_wait_time} seconds")
            sys.exit(1)
        
        try:
            response = requests.get(status_url, headers=headers)
            response.raise_for_status()
            result = response.json()
            
            status = result.get("status")
            
            if status == "COMPLETED":
                print("Request completed successfully!")
                return result
            elif status == "FAILED":
                print("ERROR: Job failed on the GPU")
                print(f"Details: {json.dumps(result, indent=2)}")
                sys.exit(1)
            elif status in ["IN_QUEUE", "IN_PROGRESS"]:
                print(f"Status: {status} (elapsed: {int(elapsed_time)}s)")
                time.sleep(2)  # Wait 2 seconds before polling again
            else:
                print(f"Unknown status: {status}")
                time.sleep(2)
                
        except requests.exceptions.RequestException as e:
            print(f"ERROR: Failed to check job status")
            print(f"Details: {str(e)}")
            sys.exit(1)


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Example 1: Simple prompt
    print("=" * 60)
    print("Example: Sending a simple prompt")
    print("=" * 60)
    
    result = send_request("Hello from my local machine!")
    
    print("\n" + "=" * 60)
    print("RESULT FROM GPU:")
    print("=" * 60)
    print(json.dumps(result, indent=2))
    
    # You can extract the output like this:
    if "output" in result:
        print("\nGPU Response:")
        print(result["output"])
    
    print("\n" + "=" * 60)
    print("Example completed!")
    print("=" * 60)
    
    # Example 2: Send your own prompt
    print("\n\nTo send your own prompt, modify the script or use gpu_cli.py")
    print("Example:")
    print('  result = send_request("Your custom prompt here")')
