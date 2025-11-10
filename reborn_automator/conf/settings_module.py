"""
A very basic settings manager. I chose this because this app requires only a few
 settings and no special features.

A better alternative, in case the app requires more settings and advanced features,
 is Dynaconf.
"""

from abc import ABC
from pathlib import Path

import settings_utils

CURR_DIR = Path(__file__).parent
ROOT_DIR = CURR_DIR.parent.parent

# Set to True by conftest.py::test_settings_fixture().
IS_TEST = False


class _BaseSettings(ABC):  # noqa: B024
    def __getattribute__(self, name):
        """
        Baseclass meant to be used by the prod settings: _Settings(_BaseSettings)
         and not by the test settings.

        This method is a trick to make `_Settings` return test settings when
         IS_TEST = True.
        """
        if name == "IS_TEST":
            return IS_TEST
        # When IS_TEST and the test settings have the attr `name`, then return it.
        if IS_TEST and hasattr(test_settings, name):
            return getattr(test_settings, name)
        return super().__getattribute__(name)


class _Settings(_BaseSettings):
    """
    Settings class to be used as an instance, a global var `settings` in this module.

    Note: it has to be an instance for _BaseSettings.__getattribute__() to work.

    Usage:
        from conf import settings
        print(setting.APP_NAME)
    """

    APP_NAME = "Reborn Automator"

    # Credentials used in Reborn mobile app.
    # Read the Reborn creds from env vars in prod, when running in AWS Lambda.
    REBORN_CREDS_USERNAME = settings_utils.get_string_from_env(
        key="REBORN_CREDS_USERNAME",
        default="XXX",
    )
    REBORN_CREDS_PASSWORD = settings_utils.get_string_from_env(
        key="REBORN_CREDS_PASSWORD",
        default="XXX",
    )


class _TestSettings:
    # Reborn creds: read from Param Store in test (when recording tests).
    # Mind that this is better than using a local file with the secret in plain-text.
    # Mind that it needs to be a @property for lazily evaluation, so vcr.py can catch
    #  it on time.
    # And also, mind that it requires the fixture `clear_cache_for_aws_param_store_client()`
    #  in conftest.py, to clear AWS Param Store client cache, to make its HTTP
    #  interactions deterministic (otherwise vcr.py fails).
    @property
    def REBORN_CREDS_USERNAME(self):
        return settings_utils.get_string_from_env_or_aws_parameter_store(
            env_key="REBORN_CREDS_USERNAME",
            # AWS Param Store used in dev and when recording tests.
            param_store_key_path="/reborn-automator/prod/reborn-creds-username",
            default="XXX",
        )

    @property
    def REBORN_CREDS_PASSWORD(self):
        return settings_utils.get_string_from_env_or_aws_parameter_store(
            env_key="REBORN_CREDS_PASSWORD",
            # AWS Param Store used in dev and when recording tests.
            param_store_key_path="/reborn-automator/prod/reborn-creds-password",
            default="XXX",
        )


settings = _Settings()
test_settings = _TestSettings()
