def donate2usd(amount, currency, upd_rate={}):
    if type(amount) == str:
        amount = float(amount.replace(',', '.'))
    rate = dict(
        RUB=66,
        UAH=27,
        USD=1,
    )
    if upd_rate:
        rate.update(upd_rate)
    return amount / rate[currency]
