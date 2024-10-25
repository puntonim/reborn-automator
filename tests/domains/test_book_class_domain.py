import pytest

from reborn_automator.domains.book_class_domain import BookClassDomain, FailedBooking


class TestBookClassDomainGetNextCalisthenicsClass:
    def test_happy_flow(self):
        domain = BookClassDomain()
        klass_id, klass, day = domain.get_next_calisthenics_class()
        assert klass_id
        assert klass
        assert day


class TestBookClassDomainBookNextCalisthenicsClass:
    def test_too_early(self):
        domain = BookClassDomain()
        with pytest.raises(FailedBooking) as exc:
            domain.book_next_calisthenics_class()
        assert exc.value.response["status"] == 1
