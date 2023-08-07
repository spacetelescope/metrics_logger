from pytest import raises
from metrics_logger.decorators import metrics_logger


def test_one_tag(caplog) -> None:
    @metrics_logger('DMS123')
    def single_tag_test():
        pass

    single_tag_test()
    assert 'METRIC - DMS123 - single_tag_test - PASS' in caplog.text


def test_multiple_tags(caplog) -> None:
    @metrics_logger('DMS123', 'DMS456', 'DMS789')
    def multiple_tag_test():
        pass

    multiple_tag_test()
    assert 'METRIC - DMS123, DMS456, DMS789 - multiple_tag_test - PASS' in caplog.text


def test_hyphen_in_tags(caplog) -> None:
    @metrics_logger('DMS-123', 'DMS-456')
    def hyphen_test():
        pass

    hyphen_test()
    assert 'METRIC - DMS-123, DMS-456 - hyphen_test - PASS' in caplog.text


def test_delimiter_in_tags(caplog) -> None:
    @metrics_logger('DMS - 123')
    def delimiter_test():
        pass

    with raises(ValueError, match='cannot contain'):
        delimiter_test()
        assert 'METRIC - ' not in caplog.text
