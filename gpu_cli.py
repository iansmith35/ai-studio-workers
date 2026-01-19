"""
GPU CLI Tool - Easy Command-Line Access to RunPod GPU
======================================================

This CLI tool provides an easy way to interact with your RunPod GPU endpoint
from the command line.

Usage:
    python gpu_cli.py send "Your prompt here"
    python gpu_cli.py send "Your prompt here" --wait 120
"""

import click
import requests
import json
import time
import sys

# Import configuration from local_bridge
try:
    from local_bridge import RUNPOD_API_KEY, RUNPOD_ENDPOINT_ID
except ImportError:
    print("ERROR: Could not import configuration from local_bridge.py")
    print("Make sure local_bridge.py is in the same directory as gpu_cli.py")
    sys.exit(1)


def validate_config():
    """Validate that the API key and endpoint ID are configured."""
    if RUNPOD_API_KEY == "YOUR_API_KEY_HERE":
        click.echo(click.style("ERROR: You need to set your RUNPOD_API_KEY in local_bridge.py", fg="red"))
        click.echo("Get your API key from: https://www.runpod.io/console/user/settings")
        sys.exit(1)
    
    if RUNPOD_ENDPOINT_ID == "YOUR_ENDPOINT_ID_HERE":
        click.echo(click.style("ERROR: You need to set your RUNPOD_ENDPOINT_ID in local_bridge.py", fg="red"))
        click.echo("Find your endpoint ID in your RunPod serverless endpoint dashboard")
        sys.exit(1)


def send_to_gpu(prompt, max_wait_time=60):
    """Send a request to the GPU and return the result."""
    endpoint_url = f"https://api.runpod.ai/v2/{RUNPOD_ENDPOINT_ID}/run"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {RUNPOD_API_KEY}"
    }
    
    payload = {
        "input": {
            "prompt": prompt
        }
    }
    
    try:
        response = requests.post(endpoint_url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        
        if "id" in result:
            job_id = result["id"]
            return poll_for_result(job_id, max_wait_time)
        else:
            return result
            
    except requests.exceptions.RequestException as e:
        click.echo(click.style(f"ERROR: Failed to communicate with GPU endpoint", fg="red"))
        click.echo(f"Details: {str(e)}")
        
        if hasattr(e, 'response') and e.response is not None:
            click.echo(f"Status Code: {e.response.status_code}")
            try:
                error_detail = e.response.json()
                click.echo(f"Error Details: {json.dumps(error_detail, indent=2)}")
            except:
                click.echo(f"Response Text: {e.response.text}")
        
        click.echo("\nTroubleshooting:")
        click.echo("1. Check that your credentials are correct in local_bridge.py")
        click.echo("2. Make sure your endpoint is deployed and active in RunPod")
        click.echo("3. Verify you have an active internet connection")
        sys.exit(1)


def poll_for_result(job_id, max_wait_time=60):
    """Poll for job completion."""
    status_url = f"https://api.runpod.ai/v2/{RUNPOD_ENDPOINT_ID}/status/{job_id}"
    
    headers = {
        "Authorization": f"Bearer {RUNPOD_API_KEY}"
    }
    
    start_time = time.time()
    
    with click.progressbar(length=max_wait_time, 
                          label='Waiting for GPU response',
                          show_eta=True) as bar:
        while True:
            elapsed_time = time.time() - start_time
            
            if elapsed_time > max_wait_time:
                click.echo(click.style(f"\nERROR: Request timed out after {max_wait_time} seconds", fg="red"))
                sys.exit(1)
            
            try:
                response = requests.get(status_url, headers=headers)
                response.raise_for_status()
                result = response.json()
                
                status = result.get("status")
                
                if status == "COMPLETED":
                    bar.update(max_wait_time)
                    return result
                elif status == "FAILED":
                    click.echo(click.style("\nERROR: Job failed on the GPU", fg="red"))
                    click.echo(f"Details: {json.dumps(result, indent=2)}")
                    sys.exit(1)
                elif status in ["IN_QUEUE", "IN_PROGRESS"]:
                    bar.update(int(elapsed_time))
                    time.sleep(2)
                else:
                    time.sleep(2)
                    
            except requests.exceptions.RequestException as e:
                click.echo(click.style(f"\nERROR: Failed to check job status", fg="red"))
                click.echo(f"Details: {str(e)}")
                sys.exit(1)


@click.group()
def cli():
    """GPU CLI - Command-line tool to interact with your RunPod GPU endpoint."""
    pass


@cli.command()
@click.argument('prompt')
@click.option('--wait', default=60, help='Maximum time to wait for response (seconds)')
@click.option('--json-output', is_flag=True, help='Output full JSON response')
def send(prompt, wait, json_output):
    """
    Send a prompt to the GPU endpoint.
    
    Example:
        python gpu_cli.py send "Hello GPU!"
        python gpu_cli.py send "Process this data" --wait 120
        python gpu_cli.py send "Generate text" --json-output
    """
    validate_config()
    
    click.echo(click.style(f"📤 Sending to GPU: ", fg="cyan") + f"{prompt}")
    
    result = send_to_gpu(prompt, max_wait_time=wait)
    
    if json_output:
        # Output full JSON
        click.echo("\n" + "=" * 60)
        click.echo(click.style("Full JSON Response:", fg="green", bold=True))
        click.echo("=" * 60)
        click.echo(json.dumps(result, indent=2))
    else:
        # Output just the GPU response
        click.echo("\n" + "=" * 60)
        click.echo(click.style("✅ GPU Response:", fg="green", bold=True))
        click.echo("=" * 60)
        if "output" in result:
            click.echo(result["output"])
        else:
            click.echo(json.dumps(result, indent=2))
    
    click.echo("\n" + click.style("✓ Done!", fg="green"))


@cli.command()
def status():
    """Check if your GPU endpoint configuration is valid."""
    validate_config()
    
    click.echo(click.style("✓ Configuration looks good!", fg="green"))
    click.echo(f"  Endpoint ID: {RUNPOD_ENDPOINT_ID}")
    # Safely display last 4 chars of API key, or show asterisks if too short
    if len(RUNPOD_API_KEY) >= 4:
        masked_key = f"{'*' * (len(RUNPOD_API_KEY) - 4)}{RUNPOD_API_KEY[-4:]}"
    else:
        masked_key = '*' * len(RUNPOD_API_KEY)
    click.echo(f"  API Key: {masked_key}")
    click.echo("\nYou can now send requests to your GPU endpoint!")


@cli.command()
def examples():
    """Show example commands."""
    click.echo(click.style("GPU CLI - Example Commands", fg="cyan", bold=True))
    click.echo("=" * 60)
    click.echo("\n1. Send a simple prompt:")
    click.echo(click.style('   python gpu_cli.py send "Hello GPU!"', fg="yellow"))
    click.echo("\n2. Send a prompt with longer wait time:")
    click.echo(click.style('   python gpu_cli.py send "Complex task" --wait 120', fg="yellow"))
    click.echo("\n3. Get full JSON response:")
    click.echo(click.style('   python gpu_cli.py send "My prompt" --json-output', fg="yellow"))
    click.echo("\n4. Check configuration status:")
    click.echo(click.style('   python gpu_cli.py status', fg="yellow"))
    click.echo("\n5. Show this help:")
    click.echo(click.style('   python gpu_cli.py --help', fg="yellow"))
    click.echo("=" * 60)


if __name__ == "__main__":
    cli()
