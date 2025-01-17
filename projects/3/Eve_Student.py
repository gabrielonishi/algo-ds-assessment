
import time

class Transaction:
    def __init__(self, transactionID, accountIBan, amount: str, receiverIBan):
        assert transactionID is not None
        assert accountIBan is not None
        assert len(accountIBan) > 6
        assert "$" in amount
        amount = amount.replace('$', '')
        self.transactionID = transactionID
        self.accountIBan = accountIBan.strip()
        self.amount = float(amount)
        self.receiverIBan = receiverIBan.strip()


class Client:
    def __init__(self, account_number, name, username, balance):
        self.account_number = account_number
        self.name = name
        self.username = username
        self.balance = balance

    def __repr__(self):
        return (f"Client(account_number='{self.account_number}', "
                f"name='{self.name}', username='{self.username}', "
                f"balance={self.balance})")

def parse_client_from_string_DO_NOT_PROFILE(client_string):
    """
    DO NOT PROFILE AS DIFFRENT HARDWARE WILL TAKE DIFFRENT TIMES TO PROCESS.

    :param client_string:
    :return:
    """
    try:
        # Split the input string using commas
        parts = client_string.split(",")

        if len(parts) != 4:
            raise ValueError(
                "Input string must have exactly 4 fields: accountNumber, name, username, $balance")

        # Extract fields
        account_number = parts[0]
        name = parts[1]
        username = parts[2]
        balance_str = parts[3].strip()

        # Remove the dollar sign and convert to a float
        if balance_str.startswith("$"):
            balance = float(balance_str[1:])
        else:
            raise ValueError("Balance must start with a dollar sign ($)")

        # Create and return an instance of Client
        return Client(account_number, name, username, balance)

    except Exception as e:
        print(f"Error parsing client string: {e}")
        return None


def read__client_file_DO_NOT_PROFILE(file_name: str) -> list[Client]:
    assert file_name is not None, "No null file names please."
    clients = []
    with open(file_name, 'r') as file:
        next(file)  # skip header
        for line in file:
            aClient = parse_client_from_string_DO_NOT_PROFILE(line)
            assert aClient is not None, "Something went wrong reading file "
            clients.append(aClient)
            # print( aClient )
    return clients

def find_client_by_IBAN(IBAN: str, clients: list[Client]) -> Client | None:
    """

    :param IBAN: str
    :param clients:
    :return: Client
    """
    assert IBAN is not None, "No null arguments "
    assert clients is not None, "No null lists "
    assert len(clients) > 0, "No empty lists "

    for who in clients:
        if who.account_number == IBAN:
            return who

    return None

def read_transactions_from_DO_NOT_PROFILE(file_name: str) -> list[Transaction]:
    assert file_name is not None, "No null file names please."

    translist = list()
    lookUp = dict()

    with open(file_name, 'r') as file:
        next(file)
        for line in file:
            line = line.strip()
            transactionID, accountIBan, amount, receiverIBan = line.split(',')
            accountIBan = accountIBan.strip()
            receiverIBan = receiverIBan.strip()

            # print(f"TransactionID: {transactionID}, Account IBAN: {accountIBan}, Amount: {amount}, Receiver IBAN: {receiverIBan}")
            translist.append(Transaction(
                transactionID, accountIBan.strip(), amount, receiverIBan.strip()))

        print(f"numbers of transactions  read  {len(translist)} ")
    return (translist)

def find_all_transfers(transactions: list[Transaction]):
    transfer_amounts = set()
    for trans in transactions:
        transfer_amounts.add(trans.amount)
    return transfer_amounts


""" 
    Notes: I know that the same amount of money is being passed from one account to the next. 
    I feel this is important some how but putting 
        apex_trans.amount  == blue_trans.amount
    doesn't seem to speed this up. Eve. 
    I don't get it - the program works on the small files - why not the big one ? Eve. 
    
    I don't know how long this will take - I will leave this running just incase I get lucky. 
    
"""

def find_money_chain(transactions_Apex: list[Transaction], 
                     transactions_Blue: list[Transaction],  
                     transactions_Crest: list[Transaction],
                     transactions_Delta: list[Transaction]):
    
    # Divide and conquer
    apex_to_blue = list()
    for trans1 in transactions_Apex:
        for trans2 in transactions_Blue:
            if (trans1.receiverIBan == trans2.accountIBan and
                trans1.amount == trans2.amount):
                    apex_to_blue.append(trans1)
    
    print(len(apex_to_blue))
    
    blue_to_crest = list()
    for trans1 in transactions_Blue:
        for trans2 in transactions_Crest:
            if (trans1.receiverIBan == trans2.accountIBan and
                trans1.amount == trans2.amount):
                    blue_to_crest.append(trans1)
    
    print(len(blue_to_crest))
    
    crest_to_delta = list()
    for trans1 in transactions_Crest:
        for trans2 in transactions_Delta:
            if (trans1.receiverIBan == trans2.accountIBan and
                trans1.amount == trans2.amount):
                    crest_to_delta.append(trans1)
    
    print(len(crest_to_delta))
    
    for apex_trans in apex_to_blue:
        for blue_trans in blue_to_crest:
            for crest_trans in crest_to_delta:
                # print( crest_trans.accountIBan, blue_trans.receiverIBan)
                for delat_trans in transactions_Delta:
                    if (apex_trans.receiverIBan == blue_trans.accountIBan and
                        apex_trans.amount == blue_trans.amount and
                        blue_trans.receiverIBan == crest_trans.accountIBan and
                        blue_trans.amount == crest_trans.amount and
                        crest_trans.receiverIBan == delat_trans.accountIBan and
                            crest_trans.amount == delat_trans.amount):

                        print(f"""Found link {apex_trans.accountIBan} gave {apex_trans.amount} to
    {apex_trans.receiverIBan}  in Apex. who moved it to blue so {blue_trans.receiverIBan}
    gave  {blue_trans.amount} to {blue_trans.receiverIBan}  they transfered to Cretview.
    {crest_trans.accountIBan} gave {crest_trans.amount} to {crest_trans.receiverIBan}
    who moved it to delta bank ang then gave {delat_trans.accountIBan} to {delat_trans.receiverIBan}
                            """)

                        return (apex_trans, blue_trans, crest_trans, delat_trans)


if __name__ == "__main__":
    program_start = time.time()
    
    dir = 'Eve_Big/'  # change to Eve_Big when you find this

    clients_Apex = read__client_file_DO_NOT_PROFILE(
        dir + 'Apex_Bank_Clients.csv')
    clients_Blue = read__client_file_DO_NOT_PROFILE(
        dir + 'Blue_Ridge_Bank_Clients.csv')
    clients_Crestview = read__client_file_DO_NOT_PROFILE(
        dir + 'Crestview_Financial_Clients.csv')
    clients_Delta = read__client_file_DO_NOT_PROFILE(
        dir + 'Delta_Trust_Bank_Clients.csv')

    transactions_Apex = read_transactions_from_DO_NOT_PROFILE(
        dir + 'Apex_Bank_transaction.csv')
    transactions_Blue = read_transactions_from_DO_NOT_PROFILE(
        dir + 'Blue_Ridge_Bank_transaction.csv')
    transactions_Crest = read_transactions_from_DO_NOT_PROFILE(
        dir + 'Crestview_Financial_transaction.csv')
    transactions_Delta = read_transactions_from_DO_NOT_PROFILE(
        dir + 'Delta_Trust_Bank_transaction.csv')

    print("Processing - Perhaps this time it will come back ")

    find_money_chain_start = time.time()
    apex_trans, blue_trans, crest_trans, delat_trans = (
        find_money_chain(transactions_Apex, transactions_Blue,  transactions_Crest, transactions_Delta))
    find_money_chain_end = time.time()

    apex_start = time.time()
    apex_client = find_client_by_IBAN(apex_trans.accountIBan, clients_Apex)
    apex_end = time.time()
    assert apex_client is not None, "Client has no name"
    print(apex_client)

    blue_start = time.time()
    blue_client = find_client_by_IBAN(blue_trans.accountIBan, clients_Blue)
    blue_end = time.time()
    print(blue_client)

    cretview_start = time.time()
    cretview_client = find_client_by_IBAN(
        crest_trans.accountIBan, clients_Crestview)
    cretview_client_end = time.time()
    print(cretview_client)

    delta_start = time.time()
    delta_client = find_client_by_IBAN(delat_trans.accountIBan, clients_Delta)
    delta_end = time.time()
    print(delta_client)

    print("Computation complete. End of line ")
    
    print("*" * 80)
    print("Profiling Results")
    print("Finding the money chain took ", find_money_chain_end - find_money_chain_start)
    print("Apex Client Search took ", apex_end - apex_start)
    print("Blue Client Search took ", blue_end - blue_start)
    print("Crestview Client Search took ", cretview_client_end - cretview_start)
    print("Delta Client Search took ", delta_end - delta_start)
    print("Total program run time ", time.time() - program_start)