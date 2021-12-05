import json
import subprocess

import requests


def send_status(description, post_params):
    requests.post(post_params[1], headers=post_params[0],
                  data=json.dumps({"state": "pending", "context": "The Ultimate Test", "description": description}))


def save_and_update(proc, model, post_params, name):
    output = (proc.stderr or proc.stdout).decode()
    model.test_output += f"\n{output}"
    model.save()

    send_status(f"{name} finished", post_params)

    return proc.returncode


def test_with_yarn(cwd, model, post_params):
    yarn = "/usr/local/bin/yarn"
    cmd_arrays = [
        ([yarn, "ci"], "Installing Dependencies"),
        ([yarn, "test"], "Unit tests"),
        ([yarn, "lint"], "Lint"),
        ([yarn, "stage"], "Build")
    ]

    code = [save_and_update(subprocess.run(cmd_array, capture_output=True, cwd=cwd), model, post_params, name) for
            (cmd_array, name) in cmd_arrays]

    send_status(f"Deploying", post_params)

    deploy = subprocess.run(["cp", "-rf", "build", "../"], capture_output=True, cwd=cwd)
    model.test_output += f"\n{deploy}"
    model.save()

    return sum(code)
