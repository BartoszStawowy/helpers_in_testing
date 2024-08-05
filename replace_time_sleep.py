from functools import wraps
import time
from selenium.webdriver.remote.webdriver import WebDriver


def wait_for_dom_change(check_interval=1, timeout=30):
    """
    Decorator to avoid using time.sleep by waiting for a change in the HTML DOM.

    Args:
    check_interval (int): Time in seconds to wait between checks.
    timeout (int): Maximum time in seconds to wait for a DOM change.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            driver = kwargs.get('driver')

            if not driver:
                for arg in args:
                    if isinstance(arg, WebDriver):
                        driver = arg
                        break
                    elif hasattr(arg, 'driver') and isinstance(getattr(arg, 'driver'), WebDriver):
                        driver = getattr(arg, 'driver')
                        break

            if not driver or not isinstance(driver, WebDriver):
                raise ValueError(
                    "----> Additional info <----"
                    "A valid selenium webdriver instance must be passed as 'driver' in args,"
                    " kwargs, or as an attribute of the first argument.")

            start_time = time.time()
            initial_dom = driver.page_source

            while True:
                func(*args, **kwargs)

                time.sleep(check_interval)
                new_dom = driver.page_source

                if initial_dom != new_dom:
                    break
                elif time.time() - start_time > timeout:
                    raise TimeoutError("HTML DOM did not change within the specified timeout.")

            return func(*args, **kwargs)

        return wrapper

    return decorator
