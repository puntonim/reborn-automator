from datetime import datetime

import pytest

from reborn_automator.domains.book_class_domain import (
    FailedBooking,
    NoCalisthenicsClassFoundInPalinsesto,
)
from reborn_automator.utils.testutils import datetime_testutils
from reborn_automator.utils.testutils.aws_testfactories.cloudwatch_event_factory import (
    CloudWatchEventFactory,
)
from reborn_automator.utils.testutils.aws_testfactories.lambda_context_factory import (
    LambdaContextFactory,
)
from reborn_automator.views.cron_book_class_view import lambda_handler

frozen_date1 = datetime(2024, 10, 25, 11, 0, 0).astimezone()
frozen_date2 = datetime(2024, 10, 30, 11, 0, 0).astimezone()
frozen_date3 = datetime(2025, 4, 15, 12, 0, 0).astimezone()


class TestCronBookClassView:
    def setup_method(self):
        self.context = LambdaContextFactory().make()

    @datetime_testutils.freeze_time(frozen_date1)
    def test_happy_flow(self):
        lambda_handler(
            CloudWatchEventFactory.make_for_scheduled_event(),
            self.context,
        )

    @datetime_testutils.freeze_time(frozen_date2)
    def test_no_calisthenics_class_found_in_palinsesto(self):
        with pytest.raises(NoCalisthenicsClassFoundInPalinsesto):
            lambda_handler(
                CloudWatchEventFactory.make_for_scheduled_event(),
                self.context,
            )

    @datetime_testutils.freeze_time(frozen_date3)
    def test_no_active_subscription(self):
        with pytest.raises(FailedBooking):
            lambda_handler(
                CloudWatchEventFactory.make_for_scheduled_event(),
                self.context,
            )
