class TransactionChoices:
    INCOME = "Income"
    EXPENSE = "Expense"

    TYPE_CHOICES = (
        (INCOME, INCOME),
        (EXPENSE, EXPENSE)
    )

    CASH = "Cash"
    CHECK = "Check"
    CREDIT_CARD = "Credit Card"
    DEBIT_CARD = "Debit Card"
    DIRECT_DEPOSIT = "Direct Deposit"
    OTHER = "Other"

    METHOD_CHOICES = (
        (CASH, CASH),
        (CHECK, CHECK),
        (CREDIT_CARD, CREDIT_CARD),
        (DEBIT_CARD, DEBIT_CARD),
        (DIRECT_DEPOSIT, DIRECT_DEPOSIT),
        (OTHER, OTHER)
    )


class TransactionVerboseNames:

    DATE = "Date"
    TYPE = "Type of Transaction"
    METHOD = "Method of Transaction"
    NAME = "Name"
    AMOUNT = "Amount"
    CATEGORY = "Category"