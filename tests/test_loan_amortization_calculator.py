from pytest import approx, fixture
from src.utils.loan_amortization_calculation import LoanAmortizationCalculator

class TestLoanAmortizationCalculator:

    principal_loan_balance = 30000.00
    annual_interest_rate = 3
    term_months = 48
    total_monthly_payment = 664.03

    def test_calculate_monthly_interest_rate(self):
        annual_interest_rate_decimal = TestLoanAmortizationCalculator.annual_interest_rate / 100
        assert LoanAmortizationCalculator.calculate_monthly_interest_rate(annual_interest_rate_decimal) == 0.0025
    
    def test_calculate_total_monthly_payment(self):
        assert LoanAmortizationCalculator.calculate_total_monthly_payment(
            TestLoanAmortizationCalculator.principal_loan_balance,
            TestLoanAmortizationCalculator.term_months,
            TestLoanAmortizationCalculator.annual_interest_rate / 100
        ) == TestLoanAmortizationCalculator.total_monthly_payment

    def test_calculate_monthly_principal_payment(self):
        assert LoanAmortizationCalculator.calculate_monthly_principal_payment(
            TestLoanAmortizationCalculator.total_monthly_payment,
            TestLoanAmortizationCalculator.principal_loan_balance,
            TestLoanAmortizationCalculator.annual_interest_rate / 100
        ) == 589.03
    
    def test_calculate_monthly_interest_payment(self):
        monthly_principal_payment = 589.03
        assert LoanAmortizationCalculator.calculate_monthly_interest_payment(
            TestLoanAmortizationCalculator.total_monthly_payment,
            monthly_principal_payment
        ) == 75.00
    
    def test_get_amortized_numerator(self):
        ### using approx because pytest rounding up the number
        ### assert 0.0028183200525998277 == 0.002818320052599835
        ###                         ^rounded to 835----------^
        assert LoanAmortizationCalculator.get_amortized_numerator(
            TestLoanAmortizationCalculator.annual_interest_rate / 100,
            TestLoanAmortizationCalculator.term_months
        ) == approx(0.002818320052599834944899996728)

    def test_get_amortized_denominator(self):
        ### using approx because pytest rounding up the number
        ### assert 0.12732802103993102 == 0.127328021039934
        ###                     ^rounded to 934---------^
        assert LoanAmortizationCalculator.get_amortized_denominator(
            TestLoanAmortizationCalculator.annual_interest_rate / 100,
            TestLoanAmortizationCalculator.term_months
        ) == approx(0.127328021039933977959998691)
    
    def test_calculate_loan_schedule(self):
        loan_schedule = LoanAmortizationCalculator.calculate_loan_schedule(
            TestLoanAmortizationCalculator.principal_loan_balance,
            TestLoanAmortizationCalculator.term_months,
            TestLoanAmortizationCalculator.annual_interest_rate
        )
        assert len(loan_schedule) == TestLoanAmortizationCalculator.term_months
