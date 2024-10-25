"""
A very basic settings manager. I chose this because this app requires only a few
 settings and no special features.

A better alternative, in case the app requires more settings and advanced features,
 is Dynaconf.
"""

from pathlib import Path

from ..utils import settings_utils

CURR_DIR = Path(__file__).parent
ROOT_DIR = CURR_DIR.parent.parent


class settings:
    """
    Usage:
        from conf import settings
        print(setting.APP_NAME)
    """

    APP_NAME = "Reborn Automator"
    IS_TEST = False

    # Read the Reborn creds from env vars (when running in AWS Lambda) or from
    #  local file (when running in dev machine) - which is git ignored indeed ;).
    REBORN_CREDS_USERNAME = settings_utils.get_string_from_env_or_aws_parameter_store(
        env_key="REBORN_CREDS_USERNAME",
        parameter_store_key_path="/reborn-automator/production/reborn-creds-username",
        default="XXX",
    )
    REBORN_CREDS_PASSWORD = settings_utils.get_string_from_env_or_aws_parameter_store(
        env_key="REBORN_CREDS_PASSWORD",
        parameter_store_key_path="/reborn-automator/production/reborn-creds-password",
        default="XXX",
    )


class test_settings:
    IS_TEST = True