from ._anvil_designer import payment_details_extensionTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import timedelta

class payment_details_extension(payment_details_extensionTemplate):
    def __init__(self, selected_row=None, loan_extension_months=None, extension_fee=None, **properties):
        self.selected_row = selected_row
        self.loan_extension_months = loan_extension_months
        self.extension_fee = extension_fee
        self.init_components(**properties)

        if selected_row:
            self.load_payment_details(selected_row)

    def load_payment_details(self, selected_row):
        self.load_entered_values()
        payment_details = []

        entered_extension_months = self.loan_extension_months
        total_tenure = selected_row['tenure'] + entered_extension_months

        monthly_interest_rate = (selected_row['interest_rate'] / 100) / 12

        beginning_balance = selected_row['loan_amount']

        extension_fee_percentage = self.extension_fee if self.extension_fee is not None else selected_row.get('extension_fee', 0)
        extension_fee_amount = (extension_fee_percentage / 100) * selected_row['loan_amount']

        # Find the last paid EMI number for the specific loan
        last_paid_emi_records = app_tables.fin_emi_table.search(loan_id=selected_row['loan_id'], scheduled_payment_made=q.not_(None))
        last_paid_emi_number = max([record['emi_number'] for record in last_paid_emi_records], default=0)
        last_paid_emi_ending_balance = selected_row['loan_amount']

        for month in range(1, total_tenure + 1):
            payment_date = self.calculate_payment_date(selected_row, month)
            loan_id = selected_row['loan_id']
            emi_number = month
            emi_row = app_tables.fin_emi_table.get(loan_id=loan_id, emi_number=emi_number)

            if emi_row is not None:
                scheduled_payment_made = emi_row['scheduled_payment_made']
                account_number = emi_row['account_number']
            else:
                scheduled_payment_made = None
                account_number = None

            formatted_payment_date = f"{payment_date:%Y-%m-%d}" if payment_date else "Awaiting Update"

            if month <= last_paid_emi_number:  # Paid months: Calculate scheduled payment based on the selected row's tenure
                emi = self.calculate_scheduled_payment(selected_row['loan_amount'], monthly_interest_rate, selected_row['tenure'])
                total_payment = emi
            else:
                # Unpaid months: Calculate scheduled payment based on tenure plus extension months
                emi = self.calculate_scheduled_payment(last_paid_emi_ending_balance, monthly_interest_rate, total_tenure - (month - 1))
                total_payment = emi + extension_fee_amount if month == last_paid_emi_number + 1 else emi
            self.emi = emi
            interest_amount = last_paid_emi_ending_balance * monthly_interest_rate
            principal_amount = emi - interest_amount
            ending_balance = last_paid_emi_ending_balance - principal_amount

            payment_details.append({
                'PaymentNumber': month,
                'PaymentDate': formatted_payment_date,
                'EMIDate': f"{scheduled_payment_made:%Y-%m-%d}" if scheduled_payment_made else "N/A",
                'EMITime': f"{scheduled_payment_made:%I:%M %p}" if scheduled_payment_made else "N/A",
                'AccountNumber': account_number if account_number else "N/A",
                'ScheduledPayment': f"₹ {emi:.2f}",
                'Principal': f"₹ {principal_amount:.2f}",
                'Interest': f"₹ {interest_amount:.2f}",
                'BeginningBalance': f"₹ {last_paid_emi_ending_balance:.2f}",
                'ExtensionFee': f"₹ {extension_fee_amount:.2f}" if month == last_paid_emi_number + 1 else "₹ 0.00",
                'TotalPayment': f"₹ {total_payment:.2f}",
                'EndingBalance': f"₹ {ending_balance:.2f}"
            })

            last_paid_emi_ending_balance = ending_balance

        self.repeating_panel_1.items = payment_details

    def load_entered_values(self):
        self.entered_loan_amount = self.selected_row['loan_amount']
        self.entered_tenure = self.selected_row['tenure']
        self.entered_extension_months = self.loan_extension_months

    def calculate_payment_date(self, selected_row, current_month):
        loan_updated_status = selected_row['loan_updated_status'].lower()

        if loan_updated_status in ['close', 'closed loans', 'disbursed loan', 'foreclosure']:
            try:
                loan_disbursed_timestamp = selected_row['loan_disbursed_timestamp']

                if loan_disbursed_timestamp:
                    fin_product_details_row = app_tables.fin_product_details.get(
                        product_id=selected_row['product_id']
                    )
                    first_emi_payment = fin_product_details_row['first_emi_payment']

                    if current_month == 1:
                        payment_date = loan_disbursed_timestamp + timedelta(
                            days=int(first_emi_payment * 30.44)
                        )
                    else:
                        payment_date = loan_disbursed_timestamp + timedelta(
                            days=int(first_emi_payment * 30.44) + (current_month - 1) * 30
                        )

                    return payment_date
                else:
                    return None
            except Exception as e:
                print(f"Error in calculate_payment_date: {e}")
                return None
        else:
            return None

    def calculate_scheduled_payment(self, loan_amount, monthly_interest_rate, remaining_tenure):
        emi = (loan_amount * monthly_interest_rate * ((1 + monthly_interest_rate) ** remaining_tenure)) / (
                ((1 + monthly_interest_rate) ** remaining_tenure) - 1)

        return emi

    def button_1_click(self, **event_args):
        open_form('borrower_registration_form.dashboard.extension_loan_request.borrower_extension.extension2',
                  selected_row=self.selected_row, loan_extension_months=self.loan_extension_months, new_emi = self.emi)

    def button_2_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('borrower_registration_form.dashboard.extension_loan_request.borrower_extension', selected_row = self.selected_row)

    

   