
"""Basic pricing helpers for discounted cost calculations."""


def calculateFinalCost(price, discount) :
    """Return the final cost after applying a percentage discount.

    Args:
        price: Original item price.
        discount: Discount percentage to subtract from the price.

    Returns:
        The discounted final price.
    """
    return price - (price * discount) / 100;


if __name__ == "__main__":
    print ("Cost for discount " + str(calculateFinalCost(100, 20)))
