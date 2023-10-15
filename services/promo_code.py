import random
import string
import datetime
def daily_promo_code():
    #gets the current date in the format YYYY-MM-DD
    current_date = datetime.date.today().isoformat()

    #seeds the random number generator with the current date
    seed = int(current_date.replace("-", ""))
    random.seed(seed)

    #generates a random promo code with a specific format (XXX-XXXX-XXXX)
    promo_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))
    promo_code += '-'
    promo_code += ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
    promo_code += '-'
    promo_code += ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
    return promo_code
daily_promo_code()
