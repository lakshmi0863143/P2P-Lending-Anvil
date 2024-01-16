from ._anvil_designer import View_DetailsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ...import lendor_main_form_module as main_form_module
from datetime import datetime
from datetime import datetime, timezone


class View_Details(View_DetailsTemplate):
  def __init__(self,selected_row, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    # Display loan details
    self.loan_id_label.text = f"{selected_row['loan_id']}"
    self.loan_amount_label.text=f"{selected_row['credit_limit']}"
    self.intrest_rate_label.text=f"{selected_row['interest_rate']}"
    self.tenure_label.text=f"{selected_row['tenure']}"
    self.date_of_apply_label.text=f"{selected_row['lender_accepted_timestamp']}"
    self.due_amount_label.text=f"{selected_row['loan_amount']}"
    self.due_date_label.text=f"{selected_row['emi_due_date']}"
    
    due_date = selected_row['emi_due_date']
# Check if due_date is not None before processing
    if due_date is not None:
    # Convert due_date to datetime with a fixed time (e.g., midnight) and set the time zone
      due_date_aware = datetime.combine(due_date, datetime.min.time()).replace(tzinfo=timezone.utc)

      days_left = (due_date_aware - datetime.now(timezone.utc)).days
      self.days_left_label.text = f"{days_left} days left"
    else:
      self.days_left_label.text = "N/A"
    
  def button_1_copy_click(self, **event_args):
    open_form('lendor_registration_form.dashboard')

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('lendor_registration_form.dashboard.td')
