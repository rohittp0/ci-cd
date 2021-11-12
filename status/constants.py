import os

from dotenv import load_dotenv

BASE_URL = "https://ci.trebuchet.one/api/pull_request"
TEST_FAILED = "I didn't do anything, it just broke."
TEST_PASSED = "Your code rocks !!"

load_dotenv()
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'token {os.getenv("GIT_HUB_TOKEN")}'
}
