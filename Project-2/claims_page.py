from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ClaimsPage(BasePage):
    # OrangeHRM demo may not have a claims module; this is a generic implementation
    CLAIMS_MENU = (By.LINK_TEXT, "Claims")
    NEW_CLAIM = (By.ID, "btnNewClaim")
    CLAIM_TYPE = (By.ID, "claim_type")
    CLAIM_AMOUNT = (By.ID, "claim_amount")
    CLAIM_REASON = (By.ID, "claim_reason")
    SUBMIT_BTN = (By.ID, "btnSubmit")
    SUCCESS_MSG = (By.XPATH, "//div[contains(@class,'message success')]")

    def go_to_claims(self):
        self.click(self.CLAIMS_MENU)

    def submit_claim(self, ctype, amount, reason):
        self.click(self.NEW_CLAIM)
        self.send_keys(self.CLAIM_TYPE, ctype)
        self.send_keys(self.CLAIM_AMOUNT, amount)
        self.send_keys(self.CLAIM_REASON, reason)
        self.click(self.SUBMIT_BTN)

    def get_success(self):
        el = self.is_visible(self.SUCCESS_MSG)
        return el.text if el else ""
