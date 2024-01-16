import anvil
from ._anvil_designer import Borr_loan_requestTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
from anvil.tables import app_tables
from anvil import open_form
from datetime import datetime
from ... import lendor_main_form_module as main_form_1
from .....bank_users.main_form import main_form_module


# In Borr_loan_request class

class Borr_loan_request(Borr_loan_requestTemplate):
    def __init__(self, selected_row, **properties):
       # Set Form properties and Data Bindings.
        self.selected_row = selected_row
        self.init_components(**properties)
        self.user_id=main_form_1.userId
        use_id = self.user_id

        self.email=main_form_module.email
        email = self.email

        
        
        # Populate labels with the selected row details
        self.label_user_id.text = f"{selected_row['borrower_customer_id']}"
        self.label_name.text = f"{selected_row['borrower_full_name']}"
        self.label_loan_amount_applied.text = f"{selected_row['loan_amount']}"
        self.label_loan_id.text = f"{selected_row['loan_id']}"
        self.label_beseem_score.text = f"{selected_row['beseem_score']}"
        self.label_loan_tenure.text = f"{selected_row['tenure']}"
        self.label_credit_limit.text = f"{selected_row['credit_limit']}"
        self.label_interest_rate.text = f"{selected_row['interest_rate']}"
        self.update_ui_based_on_status()

        # Fetch additional details from the 'borrower' table
        try:
            user_request = app_tables.borrower.get(customer_id=str(selected_row['borrower_customer_id']))
            if user_request is not None:
                # Assuming 'bank_acc_details' is a valid column name in the 'borrower' table
                bank_acc_details = user_request['bank_acc_details']
                borrower_approve_date = user_request['borrower_approve_date']
                self.label_member_since.text = f"{borrower_approve_date}"
                self.label_bank_acc_details.text = f"{bank_acc_details}"
                
                # Fetch additional details from the 'loan_details' table
                try:
                    #loan_details = app_tables.loan_details.get(loan_id=int(selected_row['loan_id']))
                    loan_details = app_tables.loan_details.get(loan_id=str(selected_row['loan_id']))
                    if loan_details is not None:
                        # Assuming 'interest_rate' and 'min_amount' are valid column names in the 'loan_details' table
                        interest_rate = loan_details['interest_rate']
                        min_amount_text = loan_details['loan_amount']
                        
                        # Calculate and display ROM in amount format
                        rom_amount = self.calculate_rom(interest_rate,min_amount_text)
                        self.label_member_rom.text = f"{rom_amount:.2f}"
                    else:
                        self.label_member_rom.text = "No data for loan_id in loan_details"
                except anvil.tables.TableError as e:
                    self.label_member_rom.text = f"Error fetching loan details: {e}"
            else:
                self.label_bank_acc_details.text = "No data for bank_acc_details in user_request"
        except anvil.tables.TableError as e:
            self.label_bank_acc_details.text = f"Error fetching user details: {e}"
           
     
    def calculate_rom(self, interest_rate, min_amount_text):
        # Calculate ROM based on your business logic
        try:
            # Convert min_amount_text to a numeric value (assuming it's a string representing a number)
            min_amount = float(min_amount_text)

            earnings = interest_rate * min_amount

            return earnings
        except ValueError as e:
            print(f"Error converting min_amount_text to numeric: {e}")
            return 0

    

    def button_1_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('lendor_registration_form.dashboard.vblr')
   
  
    def update_ui_based_on_status(self):
        # Check the value of 'loan_updated_status' in the database
        loan_status = self.selected_row['loan_updated_status']

        if loan_status == 'accepted':
            # Set the text of the Output Label with blue color
            self.output_label1.text = "This Borrower Loan is Accepted"
            self.output_label1.foreground = '#0000FF'  # Blue color
            self.output_label1.visible = True
            # Disable the "Accept" button
            self.accepted_btn.enabled = False
            self.accepted_btn.visible = False
            self.rejected_btn.visible = False
        elif loan_status == 'rejected':
            # Set the text of the Output Label with red color
            self.output_label1.text = "This Borrower Loan is Rejected"
            self.output_label1.foreground = '#FF0000'  # Red color
            self.output_label1.visible = True
            # Disable the "Reject" button
            self.rejected_btn.enabled = False
            self.accepted_btn.visible = False
            self.rejected_btn.visible = False

    # def accepted_btn_click(self, **event_args):
    #   """This method is called when the button is clicked"""
    #   # self.accepted_btn_click(selected_row=self.selected_row)
    #   loan_amount_applied = self.selected_row['loan_amount']
    
    #   lender = app_tables.lender.get(customer_id=int(self.selected_row['lender_customer_id']))
    
    #   if int(lender['investment']) >= int(loan_amount_applied):
    #       # Sufficient balance available, proceed with accepting the loan
    #       self.accepted_btn.visible = False
    #       self.output_label1.text = "This Borrower Loan is Accepted"
    #       self.output_label1.foreground = '#0000FF'  # Blue color
    #       self.output_label1.visible = True
    #       self.selected_row['loan_updated_status'] = 'accepted'
    #       self.selected_row.update()
    #       self.update_ui_based_on_status()
    #       Notification("Borrower will get notified").show()
    #       open_form("lendor_registration_form.dashboard.vblr")
    #   else:
    #       # Insufficient balance, prompt the user to top-up the amount
    #       alert("You don't have enough balance. Please add the amount in wallet.", buttons=[("OK")])
    # #       self.open_opbal_form()
                                                                                     
    # # def open_opbal_form(self):
    # #   try:
    # #       open_form("wallet.wallet")
    # #   except Exception as e:
    # #       print(f"Error opening wallet form: {e}")
        
    def accepted_btn_click(self, **event_args):
        """This method is called when the button is clicked"""
        
        self.accepted_btn.visible = True
        self.rejected_btn.visible = False
        self.loan_disbursment_btn.visible = False
      
        self.accepted_btn.visible = False
        # Set the text of the Output Label with blue color
        self.output_label1.text = "This Borrower Loan is Rejected"
        self.output_label1.foreground = '#0000FF'  # Blue color
        self.output_label1.visible = True
        # Update the 'loan_updated_status' column in the 'loan_details' table to 'accepted'
        self.selected_row['loan_updated_status'] = 'accepted'
        self.selected_row['lender_accepted_timestamp'] = datetime.now()
        # Save changes to the table
        self.selected_row.update()
        # Update UI based on the new status
        Notification("Borrower will get notified").show()
        self.update_ui_based_on_status()
        self.loan_disbursment_btn.visible = True
        

        # Close the form after deletion
        # open_form("lendor_registration_form.dashboard.vblr")

    def rejected_btn_click(self, **event_args):
        """This method is called when the button is clicked"""
        
        self.accepted_btn.visible = False
        self.rejected_btn.visible = True
        self.loan_disbursment_btn.visible = False
      
        self.rejected_btn.visible = False
        # Set the text of the Output Label with blue color
        self.output_label1.text = "This Borrower Loan is Rejected"
        self.output_label1.foreground = '#FF0000'  # Red color
        self.output_label1.visible = True
        # Update the 'loan_updated_status' column in the 'loan_details' table to 'Rejected'
        self.selected_row['loan_updated_status'] = 'rejected'
        # Save changes to the table
        self.selected_row.update()
        # Update UI based on the new status
        self.update_ui_based_on_status()
        

        # Close the form after deletion
        open_form("lendor_registration_form.dashboard.vblr")

    def open_wallet_form(self):
        # Call the server-side function to get the signal
        signal = anvil.server.call('open_wallet_form')

    def loan_disbursment_btn_click(self, **event_args):
        """This method is called when the button is clicked"""
        
        # Assuming 'selected_row' is the selected row from the loan_details table
        selected_row = self.selected_row  
        email = main_form_module.email
      
        # Call the server-side function
        signal = anvil.server.call('loan_disbursement_action', selected_row, email)

        # Check the signal and perform actions accordingly
        if signal == "insufficient_balance":
            alert("Insufficient balance. Please add the amount in the wallet. If not added within 30 min, it will go to lost opportunities.")
            open_form("wallet.wallet")
        elif signal == "pay_to_borrower":
            alert("Pay to Borrower")
            open_form("wallet.wallet")

  