from ._anvil_designer import new_loan_requestTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import main_form_module as main_form_module

class new_loan_request(new_loan_requestTemplate):
    def __init__(self, **properties):
        self.user_id = main_form_module.userId
        self.init_components(**properties)

        options = app_tables.fin_product_group.search()
        # Exclude empty strings from the drop-down options
        option_strings = [option['name'] for option in options if option['name'].strip()]
        self.name.items = option_strings
        self.name.selected_value = None  # Set to None initially, as there is no default selection

        # Add a placeholder to drop_down_2
        self.drop_down_2.items = ['']  # Add your placeholder text here
        self.drop_down_2.selected_value = None
    # In borrower_registration_form.dashboard.new_loan_request module (client-side code)
    # def loan_type():
    #     # Call the server-side function to get product details
    #     product_details = anvil.server.call('get_fin_product_details', 'desired_category')
    #     # Process the product_details as needed

    def name_change(self, **event_args):
        self.selected_value = self.name.selected_value

        if self.selected_value:
            self.label_1.visible = True
            self.label_2.visible = True
            self.name.visible = True
            self.drop_down_2.visible = True
            self.label_4.visible = True

            # Fetch product categories based on the selected loan type
            product_categories = app_tables.fin_product_categories.search(
                name_group=self.name.selected_value
            )

            if product_categories:
                # Display product categories in drop_down_2, excluding empty strings
                self.drop_down_2.items = [category['name_categories'] for category in product_categories if category['name_categories'].strip()]
                self.drop_down_2.selected_value = None

    def button_2_click(self, **event_args):
        open_form('borrower_registration_form.dashboard')

    def button_1_copy_click(self, **event_args):
        name = self.name.selected_value
        category = self.drop_down_2.selected_value

        if not name:
            self.label_3.text = "Please select a product group"
            self.label_3.foreground = '#FF0000'
        else:
            self.label_3.text = ""

        if not category:
            self.label_4.text = "Please select a category"
            self.label_4.foreground = '#FF0000'
        else:
            self.label_4.text = ""

        if name and category:
            open_form('borrower_registration_form.dashboard.new_loan_request.loan_type', name, category,self.max_amount_lb.text)

    def max_amount_lb_show(self, **event_args):
        data = app_tables.fin_product_details.search()
        # Exclude empty strings from the max_amount values
        data1_strings = [str(data['max_amount']) for data in data if str(data['max_amount']).strip()]
        self.max_amount_lb.text = data1_strings[0] if data1_strings else None
        # user_request = app_tables.product_details.get(product_categories=self.prodct_cate)
        # if user_request:
        #     self.credit_limit = user_request['max_amount']

    def button_1_click(self, **event_args):
      open_form("borrower_registration_form.dashboard")
