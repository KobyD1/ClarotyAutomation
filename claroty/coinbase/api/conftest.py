import logging
import pytest
from claroty.coinbase.utils.chart_utils import ChartUtils
from claroty.coinbase.utils.mail_utils import MailUtils


@pytest.fixture(scope="session", autouse=True)
def configure_test():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    root_logger = logging.getLogger()
    if not root_logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        root_logger.addHandler(handler)

    logging.getLogger("matplotlib.category").setLevel(logging.CRITICAL)
    logging.info("=== Start test ===")
    mail_utils = MailUtils(root_logger)
    chart_utils = ChartUtils(root_logger)

    yield root_logger, mail_utils, chart_utils
    root_logger.info("=== End test ===")
