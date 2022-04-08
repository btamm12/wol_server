import logging
import os
from sanic import Sanic
from sanic.response import json, text
from sanic.request import Request
import subprocess

from src.logger import default_logger_path, logger, logger_setup

SRC_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.realpath(os.path.join(SRC_DIR, ".."))

# Create Sanic app.
app = Sanic(__name__)

# Register logging middleware.
@app.middleware("request")
async def extract_user(request: Request):
    msg = "Received request at endpoint '%s'." % request.endpoint
    logger.info(msg)


# Wake endpoint.
@app.get("/wake")
async def wake(request: Request):

    # MAC Addresses to wake.
    macs = {
        "btamm-desktop": "30:9C:23:8B:EF:4C",
    }
    valid_names = ",".join([key for key in macs])

    request_json = request.args
    for key in request_json:
        request_json[key] = request_json[key][0]
    if "name" not in request_json:
        return text("name was not provided", status=400)
    name = request_json["name"]
    if name not in macs:
        return text(
            f"{name} is not a valid name. Valid names: {valid_names}", status=400
        )

    # Get MAC Address.
    mac = macs[name]

    # Send Wake-on-LAN (WoL) broadcast message.
    command = f"wakeonlan {mac}"
    subprocess.run(command, shell=True)

    # Return success.
    return text(f"Magic packet sent to {name}.")


# Status endpoint.
@app.get("/health")
async def test(request: Request):
    return json({"status": "ok"})


if __name__ == "__main__":
    __DEBUG__ = False

    # Set up logger.
    __LOGGING_FMT__ = "[%(levelname)s @ %(asctime)s] %(message)s"
    __LOGGING_LVL_CONSOLE__ = logging.INFO
    __LOGGING_LVL_FILE__ = logging.INFO
    __LOGGING_FILE_PATH__ = default_logger_path(SRC_DIR)
    logger_setup(
        fmt=__LOGGING_FMT__,
        console_level=__LOGGING_LVL_CONSOLE__,
        file_level=__LOGGING_LVL_FILE__,
        file_path=__LOGGING_FILE_PATH__,
    )
    logger.info("Setting up logger.")

    # Run app.
    # 0.0.0.0 means listen to all channels (e.g. both local_host==127.0.0.1 and
    # local_machine_ip==192.168.0.200)
    # Source: https://stackoverflow.com/a/38175246
    app.run(host="0.0.0.0", port=8009, debug=__DEBUG__)
