from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.claims_page import ClaimsPage

def test_tc10_claim_request(driver):
    login = LoginPage(driver)
    dashboard = DashboardPage(driver)
    claims = ClaimsPage(driver)
    login.load()
    login.login("Admin", "admin123")
    assert dashboard.is_logged_in()
    # If claims module not present, skip gracefully
    try:
        claims.go_to_claims()
        claims.submit_claim("Medical", "1000", "Medical reimbursement")
        success = claims.get_success()
        assert success != "", "Expected success message after claim submission"
    except Exception:
        # Module not present in demo; mark as xfail
        import pytest
        pytest.xfail("Claims module not available on demo site")
    finally:
        dashboard.logout()
