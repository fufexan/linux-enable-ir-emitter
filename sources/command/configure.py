from typing import NoReturn

import logging
import subprocess

from command import boot
from globals import (BIN_GENERATE_DRIVER_PATH, SAVE_DRIVER_FOLDER_PATH,
                     BIN_IS_CAMERA_PATH, ExitCode)


def configure(device: str | None, manual: bool, exhaustive: bool, emitters: int, neg_answer_limit: int) -> NoReturn:
    """Find a driver for the infrared camera and exit.

    Args:
        device (str | None): path to the infrared camera, None for automatic detection
        manual (bool): true for enabling the manual configuration
        exhaustive (bool): true for enabling the exhaustive configuration
        emitters (int): number of emitters on the device
        neg_answer_limit (int): after k negative answer the pattern will be skiped, use 256 for unlimited
    """
    logging.info("Ensure to not use the camera during the execution.")
    logging.info("Warning to do not kill the process !")

    if device is None:
        dev_devices = subprocess.run(
            f"ls /dev/v4l/by-path/*",
            shell=True,
            capture_output=True,
            text=True,
        ).stdout.strip().split()

        for dev in dev_devices:
            exit_code = subprocess.call(
                [BIN_IS_CAMERA_PATH, dev],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            if exit_code == ExitCode.SUCCESS:
                device = dev
                break

    if device is None:
        logging.critical("Impossible to find your infrared camera.")
        logging.info(
            "Please specify your infrared camera path using the -d option."
        )
        exit(ExitCode.FAILURE)

    logging.info(f"Configuring the camera: {device}.")
    log_level = int(logging.getLogger().level == logging.DEBUG)
    exit_code = subprocess.call(
        [
            BIN_GENERATE_DRIVER_PATH,
            device,
            str(emitters),
            str(neg_answer_limit if manual else 256),
            SAVE_DRIVER_FOLDER_PATH,
            str(log_level),
            str(int(manual)),
            str(int(exhaustive)),
        ]
    )

    if exit_code != ExitCode.SUCCESS:
        logging.error("The configuration has failed.")
        logging.info(
            "Do not hesitate to visit the GitHub ! https://github.com/EmixamPP/linux-enable-ir-emitter/blob/master/docs/README.md"
        )
    else:
        logging.info("The driver has been successfully generated.")
        boot("enable")

    exit(exit_code)
