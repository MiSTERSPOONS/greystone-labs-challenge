from decimal import Decimal
from typing import List
from src.sqlmodel.models.loan_schedule import LoanSchedule

class LoanAmortizationCalculator():
    '''
    The LoanAmortizationCalculator is used to calculate loan payments.
    Amortization is a technique of gradually reducing an account balance over time. When amortizing loans,
    a gradually escalating portion of the monthly debt payment is applied to the principal.

    See more:
    - [What Is an Amortization Schedule? How to Calculate with Formula](https://www.investopedia.com/terms/a/amortization.asp)

    Methods
    -------
    calculate_monthly_interest_rate(interest_rate_decimal: Decimal)
        Prints the animals name and what sound it makes
    '''

    @staticmethod
    def calculate_monthly_interest_rate(
        annual_interest_rate_decimal: Decimal
    ):
        """Calculates the monthly interest rate given a interest rate in decimal form
        Formula:
            Monthly Interest Rate = Annual Interest Rate / 12

        Example:
        An interest rate of 3% in decimal form (.03) will return 0.0025

        Returns
        -------
        Decimal
            the monthly interest rate
        """
        return annual_interest_rate_decimal / 12
    
    @staticmethod
    def calculate_total_monthly_payment(
        principal_loan_balance: Decimal,
        term_months: int,
        annual_interest_rate_decimal: Decimal
    ) -> Decimal:
        """Calculates total monthly payment (princal + interest)

        Returns
        -------
        Decimal
            the total monthly payment rounded to 2 decimal places(ex. 100.00)
        """
        numerator = LoanAmortizationCalculator.get_amortized_numerator(annual_interest_rate_decimal, term_months)
        denominator = LoanAmortizationCalculator.get_amortized_denominator(annual_interest_rate_decimal, term_months)
        return round(principal_loan_balance * (numerator / denominator), 2)

    @staticmethod
    def calculate_monthly_principal_payment(
        total_monthly_payment: Decimal,
        outstanding_loan_balance: Decimal,
        annual_interest_rate_decimal: Decimal
    ) -> Decimal:
        """Calculates the monthly principal payment
         Monthly Principal Payment = Total Monthly Payment - (Outstanding Loan Balance x (Interest Rate / 12 Months))

        Returns
        -------
        Decimal
            the monthly principal payment rounded to 2 decimal places(ex. 100.00)
        """
        return round(total_monthly_payment - ((outstanding_loan_balance * annual_interest_rate_decimal) / 12), 2)

    @staticmethod
    def calculate_monthly_interest_payment(
        total_monthly_payment: Decimal,
        monthly_principal_payment: Decimal
    ) -> Decimal:
        """Calculates the monthly interest payment
         Monthly Interest Payment = Total Monthly Payment - Total Monthly Principal Payment

        Returns
        -------
        Decimal
            the monthly interest payment rounded to 2 decimal places(ex. 100.00)
        """
        return round(total_monthly_payment - monthly_principal_payment, 2)


    @staticmethod
    def get_amortized_numerator(
        annual_interest_rate_decimal: Decimal,
        term_months: int
    ) -> Decimal:
        """Calculates the numerator of the total monthly payment of the amortized loan
        i = monthly interest payment
        n = number of payments (terms in months)
        numerator = i * (1 + i)^n

        Returns
        -------
        Decimal
            the numerator of the monthly payment of the amortized loan
        """
        monthly_interest_rate = LoanAmortizationCalculator.calculate_monthly_interest_rate(annual_interest_rate_decimal)
        return monthly_interest_rate * (1 + monthly_interest_rate) ** term_months
    
    @staticmethod
    def get_amortized_denominator(
        annual_interest_rate_decimal: Decimal,
        term_months: int
    ) -> Decimal:
        """Calculates the denominator of the total monthly payment of the amortized loan
        i = monthly interest payment
        n = number of payments (terms in months)
        denominator = (1 + i)^n - 1

        Returns
        -------
        Decimal
            the denominator of the monthly payment of the amortized loan
        """
        monthly_interest_rate = LoanAmortizationCalculator.calculate_monthly_interest_rate(annual_interest_rate_decimal)
        return ((1 + monthly_interest_rate) ** term_months) - 1

    @staticmethod
    def calculate_loan_schedule(
        principal_loan_balance: Decimal,
        term_months: int,
        annual_interest_rate: Decimal
    ) -> List[LoanSchedule]:
        """Calculates the loan amortization schedule

        Returns
        -------
        List[LoanSchedule]
            [
                {
                    month: n
                    remaining_balance: $xxxx (remaining principal balance),
                    monthly_payment: $xxx (total payment = principal_due + interest_payment)
                },
                ...
            ]
        """
        results = []
        annual_interest_rate_decimal = annual_interest_rate / 100
        principal_balance = principal_loan_balance
        total_monthly_payment = LoanAmortizationCalculator.calculate_total_monthly_payment(principal_loan_balance, term_months, annual_interest_rate_decimal)

        for month in range(1, term_months + 1):

            monthly_principal_payment = LoanAmortizationCalculator.calculate_monthly_principal_payment(
                total_monthly_payment,
                principal_balance,
                annual_interest_rate_decimal
            )

            new_principal_balance = principal_balance - monthly_principal_payment

            if new_principal_balance < monthly_principal_payment:
                monthly_principal_payment += new_principal_balance
                new_principal_balance = 0

            results.append(
                {
                    'month': month,
                    'remaining_balance': new_principal_balance,
                    'monthly_payment': total_monthly_payment,
                }
            )
            principal_balance = new_principal_balance
        return results

