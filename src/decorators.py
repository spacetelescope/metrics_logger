import functools
import logging


METRICS_LOGGER_DELIMITER = ' - '


def metrics_logger(*requirement_tags):
    """ Decorator method for tests that require result logging for SOC level
        requirements. Results will appear in the pytest log at the INFO level
        in the format of a comma delimited string of the requirement_tags that
        are passed in. For example, calling @metrics_logger('DMS79', 'DMS80')
        would result in an entry that looks like:
        src
        

        Example Usage:

        @metrics_logger('DMS86', 'DMS-129')
        def test_some_functional_thing():
            assert True
    """

    def decorator(test_function):
        
        @functools.wraps(test_function)
        def inner(*args, **kwargs) -> None:
            """ Wrap the test function and provide access to the pytest logger,
                allowing output at INFO regardless of current loglevel. Note,
                pytest needs to be called with the `-s` flag to see this output
                on passing tests.
            """
            
            def log_result(result):
                if requirement_tags:
                    # Look for delimiter in tags
                    if list(filter(lambda t: METRICS_LOGGER_DELIMITER in t, requirement_tags)):
                        raise ValueError('metrics_logger tags cannot contain reserved text " - "')

                    # Construct message
                    message_tokens = [
                        'METRIC',
                        # Cleanse tags
                        ', '.join(requirement_tags),
                        test_function.__name__,
                        'PASS' if result else 'FAIL'
                    ]

                    # Override log level temporarily
                    logger_obj = logging.getLogger('metrics_logger')
                    orig_level = logger_obj.level
                    try:
                        logger_obj.setLevel(logging.INFO)
                        logger_obj.info(METRICS_LOGGER_DELIMITER.join(message_tokens))
                    finally:
                        logger_obj.setLevel(orig_level)

            try:
                # Call test function
                test_function(*args, **kwargs)
                
                # Success!
                log_result(True)
            except Exception:
                # Log failure
                log_result(False)
                raise
        
        return inner
    
    return decorator
