def sign_transaction(w3, tx, pkey):
    return w3.eth.account.sign_transaction(tx, pkey)