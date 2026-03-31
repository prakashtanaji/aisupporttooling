
def calculateFinalCost(price, discount) :
    return price - (price * discount) / 100;


if __name__ == "__main__":
    print ("Cost for discount " + str(calculateFinalCost(100, 20)))
