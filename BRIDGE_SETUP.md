# 🌉 CPU-to-GPU Bridge Setup Guide

This guide will help you set up communication between your local computer and your RunPod GPU endpoint. Follow the steps below - everything is designed to be copy-paste ready!

## 📋 Prerequisites

- Python 3.7 or higher installed on your local machine
- A RunPod account with a deployed serverless endpoint
- Internet connection

## 🚀 Quick Setup (5 Minutes)

### Step 1: Install Python Dependencies

Open your terminal/command prompt and navigate to this project folder, then run:

```bash
pip install -r local_requirements.txt
```

**What this does:** Installs the necessary Python libraries (`requests` and `click`) to communicate with RunPod.

### Step 2: Get Your RunPod API Key

1. Go to [RunPod User Settings](https://www.runpod.io/console/user/settings)
2. Scroll down to the **API Keys** section
3. Click **+ Create API Key**
4. Give it a name (e.g., "Local Bridge")
5. Copy the API key (it looks like: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)

⚠️ **Important:** Save this key somewhere safe! You won't be able to see it again.

### Step 3: Get Your Endpoint ID

1. Go to [RunPod Serverless Dashboard](https://www.runpod.io/console/serverless)
2. Click on your endpoint (the one you deployed this code to)
3. Look for the **Endpoint ID** (it's usually shown at the top)
4. Copy the Endpoint ID (it looks like: `abc123defg456`)

### Step 4: Configure the Bridge

1. Open the file `local_bridge.py` in a text editor
2. Find these two lines near the top (around lines 21-24):

```python
RUNPOD_API_KEY = "YOUR_API_KEY_HERE"
RUNPOD_ENDPOINT_ID = "YOUR_ENDPOINT_ID_HERE"
```

3. Replace `YOUR_API_KEY_HERE` with your actual API key from Step 2
4. Replace `YOUR_ENDPOINT_ID_HERE` with your actual Endpoint ID from Step 3
5. Save the file

**Example of what it should look like:**
```python
RUNPOD_API_KEY = "abc123de-4567-89fg-hijk-lmnopqrstuv"
RUNPOD_ENDPOINT_ID = "my-endpoint-123xyz"
```

### Step 5: Test Your Setup ✅

Run this command to verify everything is working:

```bash
python gpu_cli.py status
```

You should see a success message! If you get an error, see the [Troubleshooting](#-troubleshooting) section below.

## 💻 Usage Examples

### Using the CLI Tool (Easiest Method)

The `gpu_cli.py` tool provides the easiest way to send requests to your GPU:

#### Example 1: Send a simple message
```bash
python gpu_cli.py send "Hello from my computer!"
```

#### Example 2: Send a prompt with a longer timeout
```bash
python gpu_cli.py send "Process this complex data" --wait 120
```

#### Example 3: Get the full JSON response
```bash
python gpu_cli.py send "Generate something" --json-output
```

#### Example 4: See all available commands
```bash
python gpu_cli.py --help
```

#### Example 5: See example commands
```bash
python gpu_cli.py examples
```

### Using the Python Bridge Script Directly

If you want to integrate the bridge into your own Python code:

```python
from local_bridge import send_request

# Send a request
result = send_request("Your prompt here")

# Get the output
if "output" in result:
    print("GPU says:", result["output"])
```

### Running the Example Script

The `local_bridge.py` file includes a built-in example. Just run:

```bash
python local_bridge.py
```

This will send a test message to your GPU and print the response.

## 📝 How It Works

1. **Your Local Machine** → You type a command or run a script
2. **local_bridge.py** → Sends your request to RunPod's API over the internet
3. **RunPod API** → Routes your request to your GPU endpoint
4. **handler.py** (on GPU) → Processes your request
5. **Response Path** → Results travel back to your local machine

```
[Your Computer] → [Internet] → [RunPod API] → [Your GPU] → [Response] → [Your Computer]
```

## 🔧 Troubleshooting

### Error: "You need to set your RUNPOD_API_KEY"

**Solution:** You haven't configured your API key yet. Go back to [Step 4](#step-4-configure-the-bridge) and make sure you've replaced `YOUR_API_KEY_HERE` with your actual API key.

### Error: "You need to set your RUNPOD_ENDPOINT_ID"

**Solution:** You haven't configured your Endpoint ID yet. Go back to [Step 4](#step-4-configure-the-bridge) and make sure you've replaced `YOUR_ENDPOINT_ID_HERE` with your actual endpoint ID.

### Error: "Failed to send request" or "Status Code: 401"

**Solutions:**
- Double-check that your API key is correct (no extra spaces)
- Make sure you copied the entire API key
- Try creating a new API key in RunPod settings

### Error: "Status Code: 404"

**Solutions:**
- Verify your Endpoint ID is correct
- Make sure your endpoint is actually deployed in RunPod
- Check that your endpoint is in "Active" status (not paused or stopped)

### Error: "Request timed out"

**Solutions:**
- Your endpoint might be scaling up (cold start) - try again in a few seconds
- Increase the wait time: `python gpu_cli.py send "prompt" --wait 120`
- Check if your endpoint is active in the RunPod dashboard

### Error: "No module named 'requests'" or "No module named 'click'"

**Solution:** You need to install the dependencies. Run:
```bash
pip install -r local_requirements.txt
```

### The script runs but nothing happens

**Solutions:**
- Check if your endpoint is deployed and active in RunPod
- Look at your endpoint logs in the RunPod dashboard
- Try sending a simple test: `python gpu_cli.py send "test"`

### My endpoint is cold starting (taking a long time)

This is normal! Serverless endpoints "sleep" when not in use and take 10-30 seconds to wake up the first time.

**Solutions:**
- Just wait for the first request to complete
- Subsequent requests will be faster
- Increase workers in RunPod if you need it always active

## 🎯 Next Steps

Now that your bridge is set up, you can:

1. **Modify handler.py** - Add your own processing logic on the GPU side
2. **Create automation scripts** - Use `local_bridge.py` in your own Python scripts
3. **Build applications** - Integrate the bridge into your apps
4. **Experiment** - Try different prompts and see what your GPU can do!

## 📚 Additional Information

### File Descriptions

- **`local_bridge.py`** - Core bridge script with all the communication logic
- **`gpu_cli.py`** - User-friendly command-line interface
- **`local_requirements.txt`** - Python dependencies for your local machine
- **`handler.py`** - The code running on your GPU (in RunPod)
- **`BRIDGE_SETUP.md`** - This file!

### Security Notes

- ⚠️ **Never share your API key publicly or commit it to GitHub**
- Keep your `local_bridge.py` file private
- If you accidentally expose your API key, delete it immediately in RunPod settings and create a new one

### Cost Considerations

- You're only charged when your GPU is actively processing requests
- Idle time (waiting for requests) is free
- Monitor your usage in the RunPod dashboard

## 🆘 Getting More Help

If you're still stuck:

1. Check the [RunPod Documentation](https://docs.runpod.io/)
2. Look at your endpoint logs in the RunPod dashboard
3. Try the RunPod Discord community
4. Make sure your endpoint is showing as "Active" in RunPod

## 🎉 Success Checklist

- [ ] Installed Python dependencies
- [ ] Got RunPod API key
- [ ] Got RunPod Endpoint ID
- [ ] Configured `local_bridge.py` with credentials
- [ ] Ran `python gpu_cli.py status` successfully
- [ ] Sent first test message to GPU
- [ ] Received response from GPU

If you've checked all these boxes, you're all set! 🚀

---

**Happy Computing!** Your CPU and GPU are now best friends. 🤝
