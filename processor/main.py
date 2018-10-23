from sawtooth_sdk.processor.core import TransactionProcessor

from sawtooth_healthcare.common.helper import TP_PREFFIX_HEX6
from sawtooth_healthcare.processor.handler import HealthCareTransactionHandler


def main():
    # In docker, the url would be the validator's container name with
    # port 4004
    print("Starting...")
    try:
        processor = TransactionProcessor(url='tcp://127.0.0.1:4004')

        handler = HealthCareTransactionHandler(TP_PREFFIX_HEX6)
        processor.add_handler(handler)

        processor.start()
        print("Started!!!")
    except Exception as e:
        print("Error: {}".format(e))
    print("Done!!!")


if __name__ == "__main__":
    main()
