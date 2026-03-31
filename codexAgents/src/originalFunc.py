
"""Basic pricing helpers for discounted cost calculations."""


def calculate_final_cost(price, discount=0) :
    """Return the final cost after applying a percentage discount.

    Args:
        price: Original item price. Must be zero or greater.
        discount: Discount percentage to subtract from the price. Defaults to 0.
            A value of None is treated as 0. Valid values are from 0 to 100.

    Returns:
        The discounted final price.

    Raises:
        ValueError: If price is negative, discount is negative, or discount is
            greater than 100.
    """
    if price < 0:
        raise ValueError("price cannot be negative")

    if discount is None:
        discount = 0

    if discount < 0:
        raise ValueError("discount cannot be negative")

    if discount > 100:
        raise ValueError("discount cannot be greater than 100")

    return price - (price * discount) / 100;


if __name__ == "__main__":
    print ("Cost for discount " + str(calculate_final_cost(100, 20)))
