import six
import dateutil
import json
import logging
import numpy as np
import scipy
import pandas as pd
import statsmodels
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def main(event, context):
    # logger.info("available python packages are:")
    # help('modules')
    logger.info("Environment has the following versions:")
    logger.info(f"\tnumpy: ({np.version.version})")  # 1.15.4
    logger.info(f"\tscipy: ({scipy.version.version})")  # 1.1.0
    logger.info(f"\tsix: ({six.__version__})")  # 1.11.0
    logger.info(f"\tdateutil: ({dateutil.__version__})")  # 2.7.3
    logger.info(f"\tpandas: ({pd.__version__})")
    logger.info(f"\tstatsmodels: ({statsmodels.__version__})")

    logger.info(f"Event: {json.dumps(event)}")

    # var = [1, 3, 5, 7]

    # Test 1 - Use numpy to square numbers
    # var = np.array(event['transactions'])
    # var **= 2
    # result = var.tolist()

    # Test 2 - Use Pandas to square numbers
    var = pd.Series(event['transactions'])
    var **= 2
    result = var.to_list()

    # return json.dumps(var**2, cls=NumpyEncoder)
    logger.info(f"Set result: {result}")
    return result


if __name__ == '__main__':
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    with open('test_event.json', 'r') as f:
        event = json.load(f)
    res = main(event, {})
    logger.info(f"Main returned: {res}")
