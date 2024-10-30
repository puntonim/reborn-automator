from datetime import datetime

import pytest

from reborn_automator.domains.book_class_domain import (
    BookClassDomain,
    FailedBooking,
    NoCalisthenicsClassFoundInPalinsesto,
)
from reborn_automator.utils.testutils import datetime_testutils

frozen_date1 = datetime(2024, 10, 25, 11, 0, 0).astimezone()
frozen_date2 = datetime(2024, 10, 30, 11, 0, 0).astimezone()


class TestBookClassDomainGetNextCalisthenicsClass:

    @datetime_testutils.freeze_time(frozen_date1)
    def test_happy_flow(self):
        klass_id, klass, day = BookClassDomain().get_next_calisthenics_class()
        assert klass_id
        assert klass
        assert day

    @datetime_testutils.freeze_time(frozen_date2)
    def test_no_calisthenics_class_found_in_palinsesto(self):
        with pytest.raises(NoCalisthenicsClassFoundInPalinsesto):
            BookClassDomain().get_next_calisthenics_class()


class TestBookClassDomainBookNextCalisthenicsClass:
    @datetime_testutils.freeze_time(frozen_date1)
    def test_too_early(self):
        with pytest.raises(FailedBooking) as exc:
            BookClassDomain().book_next_calisthenics_class()
        assert exc.value.response["status"] == 1

    @datetime_testutils.freeze_time(frozen_date2)
    def test_no_calisthenics_class_found_in_palinsesto(self):
        with pytest.raises(NoCalisthenicsClassFoundInPalinsesto):
            BookClassDomain().book_next_calisthenics_class()
