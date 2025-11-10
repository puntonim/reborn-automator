from datetime import datetime, timedelta

import pytest
from datetime_utils.datetime_testutils import freeze_time

from reborn_automator.domains.book_class_domain import (
    BookClassDomain,
    FailedBooking,
    NoClassFoundInPalinsesto,
)

frozen_date1 = datetime(2024, 10, 25, 11, 0, 0).astimezone()
frozen_date2 = datetime(2025, 10, 19, 11, 0, 0).astimezone()


class TestBookClassDomain_GetNextCalisthenicsClass:
    @freeze_time(frozen_date1)
    def test_happy_flow(self):
        klass_id, klass, day = BookClassDomain().get_next_calisthenics_class()
        assert klass_id
        assert klass
        assert day

    @freeze_time(frozen_date1 + timedelta(days=5))
    def test_no_calisthenics_class_found_in_palinsesto(self):
        with pytest.raises(NoClassFoundInPalinsesto) as exc:
            BookClassDomain().get_next_calisthenics_class()
        assert exc.value.class_name == "Calisthenics"


class TestBookClassDomain_BookNextCalisthenicsClass:
    @freeze_time(frozen_date1)
    def test_too_early(self):
        with pytest.raises(FailedBooking) as exc:
            BookClassDomain().book_next_calisthenics_class()
        assert exc.value.response["status"] == 1
        assert exc.value.class_name == "Calisthenics"

    @freeze_time(frozen_date1 + timedelta(days=5))
    def test_no_calisthenics_class_found_in_palinsesto(self):
        with pytest.raises(NoClassFoundInPalinsesto) as exc:
            BookClassDomain().book_next_calisthenics_class()
        assert exc.value.class_name == "Calisthenics"


class TestBookClassDomain_GetNextPowerliftingClass:
    @freeze_time(frozen_date2)
    def test_happy_flow(self):
        klass_id, klass, day = BookClassDomain().get_next_powerlifting_class()
        assert klass_id
        assert klass
        assert day

    @freeze_time(frozen_date2 + timedelta(days=7))
    def test_no_powerlifting_class_found_in_palinsesto(self):
        with pytest.raises(NoClassFoundInPalinsesto) as exc:
            BookClassDomain().get_next_powerlifting_class()
        assert exc.value.class_name == "Powerlifting"


class TestBookClassDomain_BookNextPowerliftingClass:
    @freeze_time(frozen_date2)
    def test_too_early(self):
        with pytest.raises(FailedBooking) as exc:
            BookClassDomain().book_next_powerlifting_class()
        assert exc.value.response["status"] == 1
        assert exc.value.class_name == "Powerlifting"

    @freeze_time(frozen_date2 + timedelta(days=7))
    def test_no_powerlifting_class_found_in_palinsesto(self):
        with pytest.raises(NoClassFoundInPalinsesto) as exc:
            BookClassDomain().book_next_powerlifting_class()
        assert exc.value.class_name == "Powerlifting"
