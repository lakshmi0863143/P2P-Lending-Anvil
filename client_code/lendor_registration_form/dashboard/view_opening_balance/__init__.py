from ._anvil_designer import view_opening_balanceTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class view_opening_balance(view_opening_balanceTemplate):
  def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Fetch all rows from the table and get the latest one based on timestamp
        all_requests = app_tables.lender.search(
            tables.order_by("lender_accepted_timestamp", ascending=False)
        )

        if all_requests:
            # Extract the necessary information from the latest row
            latest_request = all_requests[0]
            final_rta = latest_request['final_rta']
            self.output_lbl.text = f" {final_rta}"
          
  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor_registration_form.dashboard.view_available_balance")

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("lendor_registration_form.dashboard")

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor_registration_form.dashboard.view_borrower_loan_request")

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor_registration_form.dashboard.loan_disbursement")

  def link_4_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor_registration_form.dashboard.view_lost_oppurtunities")

  def link_5_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor_registration_form.dashboard.today_dues")

  def link_6_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor_registration_form.dashboard.vcl")

  def link_7_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor_registration_form.dashboard.view_loan_extension_requests")

  def link_8_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor_registration_form.dashboard.view_loan_foreclosure_Requests")

  def link_9_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor_registration_form.dashboard.top_up_amount")

  def link_10_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor_registration_form.dashboard.view_or_download_portfolio")

  def link_11_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor_registration_form.dashboard.view_profile")

  def link_12_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor_registration_form.dashboard.view_or_send_notifications")

  def link_13_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("lendor_registration_form.dashboard.change_password")

  def outlined_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("lendor_registration_form.dashboard.top_up_amount")



    # Any code you write here will run before the form opens.

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("lendor_registration_form.dashboard.top_up_amount")
