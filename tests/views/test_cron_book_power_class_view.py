from datetime import datetime, timedelta

import pytest
from aws_utils.aws_testfactories.eventbridge_scheduler_event_to_lambda_factory import (
    EventbridgeSchedulerEventToLambdaFactory,
)
from aws_utils.aws_testfactories.lambda_context_factory import LambdaContextFactory
from datetime_utils import datetime_testutils

from reborn_automator.domains.book_class_domain import (
    FailedBooking,
    NoClassFoundInPalinsesto,
)
from reborn_automator.views.cron_book_power_class_view import lambda_handler

frozen_date1 = datetime(2025, 10, 19, 11, 0, 0).astimezone()
frozen_date2 = datetime(2025, 4, 15, 12, 0, 0).astimezone()


class TestCronBookPowerClassView:
    def setup_method(self):
        self.context = LambdaContextFactory().make()

    @datetime_testutils.freeze_time(frozen_date1)
    def test_happy_flow(self):
        # Note: I built the 200 response in the cassette, it's not a real one.
        lambda_handler(
            EventbridgeSchedulerEventToLambdaFactory.make_for_scheduled_event(),
            self.context,
        )

    @datetime_testutils.freeze_time(frozen_date1 + timedelta(days=7))
    def test_no_powerlifting_class_found_in_palinsesto(self):
        with pytest.raises(NoClassFoundInPalinsesto) as exc:
            lambda_handler(
                EventbridgeSchedulerEventToLambdaFactory.make_for_scheduled_event(),
                self.context,
            )
        assert exc.value.class_name == "Powerlifting"

    @datetime_testutils.freeze_time(frozen_date1)
    def test_no_active_subscription(self):
        # Note: I built the response copying the original one recorder
        #  with the cali class.
        with pytest.raises(FailedBooking):
            lambda_handler(
                EventbridgeSchedulerEventToLambdaFactory.make_for_scheduled_event(),
                self.context,
            )
