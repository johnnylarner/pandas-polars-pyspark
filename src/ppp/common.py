from enum import Enum


# TODO: would be easier to use a dictionary directly
class PaymentType(Enum):
    """Enum representing the payment types
    for the NYC Taxi dataset.
    """

    CREDIT_CARD = 1
    CASH = 2
    NO_CHARGE = 3
    DISPUTE = 4
    UNKNOWN = 5
    VOIDED_TRIP = 6


ROUTE_COLUMNS = [
    "pulocationid_borough",
    "pulocationid_zone",
    "dolocationid_borough",
    "dolocationid_zone",
]
