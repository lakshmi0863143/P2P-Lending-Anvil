from ._anvil_designer import extension_detailsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, timedelta

class extension_details(extension_detailsTemplate):
    def __init__(self, selected_row, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.selected_row = selected_row
        self.name.text = f"{selected_row['borrower_full_name']}"
        self.loan.text = f"{selected_row['loan_amount']}"      
        self.exten_fee.text = f"{selected_row['extend_fee']}"
        self.extension_amount.text = f"{selected_row['extension_amount']}"
        self.total.text = f"{selected_row['total_extension_months']}"
        self.ra.text = f"{selected_row['final_repayment_amount']}"
        self.reason.text = f"{selected_row['reason']}"
        self.new_emi.text = f"{selected_row['new_emi']}"

        if self.selected_row['status'] not in ('approved', 'rejected'):
            # Calculate the time difference between now and the request date
            print("Extension Request Date:", self.selected_row['extension_request_date'])
            time_difference = datetime.now() - datetime.combine(self.selected_row['extension_request_date'], datetime.min.time())
            print("Time Difference (seconds):", time_difference.total_seconds())

            # Check if the time difference is more than 48 hours (2 days)
            if time_difference.total_seconds() > (48 * 3600):
                self.selected_row['status'] = 'approved'
                self.selected_row.update()
                Notification("Borrower request has been automatically approved.").show()
                open_form("lendor_registration_form.dashboard.view_loan_extension_requests")


    def approve_click(self, **event_args):
        """This method is called when the 'Approve' button is clicked"""      
        self.selected_row['status'] = 'approved'
        # Save changes to the table
        self.selected_row.update()
        Notification("Borrower will get notified").show()
        open_form("lendor_registration_form.dashboard.view_loan_extension_requests")

    def decline_click(self, **event_args):
        """This method is called when the 'Decline' button is clicked"""
        self.selected_row['status'] = 'rejected'
        self.selected_row.update()
        Notification("Borrower will get notified").show()
        open_form("lendor_registration_form.dashboard.view_loan_extension_requests")

    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('lendor_registration_form.dashboard.view_loan_extension_requests')

    def button_1_copy_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form('lendor_registration_form.dashboard')

    def approve_copy_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('lendor_registration_form.dashboard.view_loan_extension_requests')
