from ._anvil_designer import Navigation_bar_lender_dashbordTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Navigation_bar_lender_dashbord(Navigation_bar_lender_dashbordTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def borrower_dashboard_home_linkhome_borrower_registration_button_copy_1_click(self, **event_args):
    open_form("lendor_registration_form.dashboard")

  def wallet_dashboard_link_click(self, **event_args):
    open_form("wallet.wallet")

  def contact_main_form_link_click(self, **event_args):
    open_form("lendor_registration_form.dashboard.dasboard_contact")
    
  def borrower_dashboard_report_problem_linkclick(self, **event_args):
    """This method is called when the link is clicked"""
    pass

  def help_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    pass
