import reflex as rx
import httpx
from typing import List, Dict
from claimsiq.config import API_URL

class ClaimsState(rx.State):
    claims_data: List[Dict] = []
    summary_stats: Dict = {}
    risk_analysis: Dict = {}
    provider_metrics: List[Dict] = []

    is_loading: bool = False
    error_message: str = ""
    selected_status: str = "all"

    total_claims: int = 0
    approved_count: int = 0
    pending_count: int = 0
    flagged_count: int = 0
    approval_rate: float = 0.0

    # Pagination
    current_page: int = 1
    page_size: int = 25
    total_pages: int = 1

    # Search
    search_query: str = ""

    # Sorting
    sort_column: str = "id"
    sort_direction: str = "asc"

    # Advanced filters
    date_start: str = ""
    date_end: str = ""
    amount_min: float = 0.0
    amount_max: float = 100000.0
    risk_filters: list[str] = []

    # Modal state
    selected_claim_id: str = ""
    show_claim_modal: bool = False

    # Theme
    dark_mode: bool = False

    # Notifications
    notification_message: str = ""
    notification_type: str = "info"  # info, success, warning, error
    show_notification: bool = False
    
    async def load_summary(self):
        self.is_loading = True
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{API_URL}/api/claims/summary")
                if response.status_code == 200:
                    data = response.json()
                    self.summary_stats = data
                    self.total_claims = data.get("total_claims", 0)
                    self.approved_count = data.get("approved_count", 0)
                    self.pending_count = data.get("pending_count", 0)
                    self.flagged_count = data.get("flagged_count", 0)
                    self.approval_rate = data.get("approval_rate", 0.0)
                    self.error_message = ""
                else:
                    self.error_message = f"Failed to load summary: {response.status_code}"
        except Exception as e:
            self.error_message = f"Error loading summary: {str(e)}"
        finally:
            self.is_loading = False
    
    async def load_claims(self):
        self.is_loading = True
        try:
            params = {"limit": 100, "offset": 0}
            if self.selected_status != "all":
                params["status"] = self.selected_status
            
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{API_URL}/api/claims", params=params)
                if response.status_code == 200:
                    data = response.json()
                    self.claims_data = data.get("claims", [])
                    self.error_message = ""
                else:
                    self.error_message = f"Failed to load claims: {response.status_code}"
        except Exception as e:
            self.error_message = f"Error loading claims: {str(e)}"
        finally:
            self.is_loading = False
    
    async def load_risk_analysis(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{API_URL}/api/analytics/risks")
                if response.status_code == 200:
                    self.risk_analysis = response.json()
        except Exception as e:
            print(f"Error loading risk analysis: {str(e)}")
    
    async def load_providers(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{API_URL}/api/providers")
                if response.status_code == 200:
                    self.provider_metrics = response.json()
        except Exception as e:
            print(f"Error loading providers: {str(e)}")
    
    def set_status_filter(self, status: str):
        self.selected_status = status
        self.current_page = 1  # Reset to first page when filtering

    def set_search_query(self, query: str):
        self.search_query = query
        self.current_page = 1  # Reset to first page when searching

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1

    def previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1

    def set_page(self, page: int):
        if 1 <= page <= self.total_pages:
            self.current_page = page

    def sort_by(self, column: str):
        if self.sort_column == column:
            # Toggle direction if same column
            self.sort_direction = "desc" if self.sort_direction == "asc" else "asc"
        else:
            self.sort_column = column
            self.sort_direction = "asc"

    @rx.var
    def filtered_claims(self) -> List[Dict]:
        """Filter claims based on search query"""
        claims = self.claims_data

        if self.search_query:
            query = self.search_query.lower()
            claims = [
                claim for claim in claims
                if query in str(claim.get("id", "")).lower()
                or query in str(claim.get("patient_name", "")).lower()
                or query in str(claim.get("status", "")).lower()
            ]

        return claims

    @rx.var
    def sorted_claims(self) -> List[Dict]:
        """Sort filtered claims"""
        claims = self.filtered_claims

        if self.sort_column and claims:
            reverse = self.sort_direction == "desc"
            try:
                claims = sorted(
                    claims,
                    key=lambda x: x.get(self.sort_column, ""),
                    reverse=reverse
                )
            except Exception as e:
                print(f"Error sorting: {e}")

        return claims

    @rx.var
    def paginated_claims(self) -> List[Dict]:
        """Get claims for current page"""
        claims = self.sorted_claims
        start = (self.current_page - 1) * self.page_size
        end = start + self.page_size

        # Update total pages
        total = len(claims)
        self.total_pages = max(1, (total + self.page_size - 1) // self.page_size)

        return claims[start:end]

    @rx.var
    def page_start(self) -> int:
        """Starting index for current page"""
        return (self.current_page - 1) * self.page_size + 1

    @rx.var
    def page_end(self) -> int:
        """Ending index for current page"""
        total = len(self.sorted_claims)
        end = self.current_page * self.page_size
        return min(end, total)

    @rx.var
    def is_last_page(self) -> bool:
        """Check if current page is the last page"""
        return self.current_page >= self.total_pages

    # Advanced Filters
    def set_date_range(self, start: str, end: str):
        self.date_start = start
        self.date_end = end
        self.current_page = 1

    def set_amount_range(self, min_val: float, max_val: float):
        self.amount_min = min_val
        self.amount_max = max_val
        self.current_page = 1

    def set_risk_filters(self, filters: list[str]):
        self.risk_filters = filters
        self.current_page = 1

    def clear_filters(self):
        self.date_start = ""
        self.date_end = ""
        self.amount_min = 0.0
        self.amount_max = 100000.0
        self.risk_filters = []
        self.search_query = ""
        self.selected_status = "all"
        self.current_page = 1

    # Modal actions
    def open_claim_modal(self, claim_id: str):
        self.selected_claim_id = claim_id
        self.show_claim_modal = True

    def close_claim_modal(self):
        self.show_claim_modal = False
        self.selected_claim_id = ""

    @rx.var
    def selected_claim(self) -> Dict:
        """Get the currently selected claim"""
        for claim in self.claims_data:
            if str(claim.get("id")) == str(self.selected_claim_id):
                return claim
        return {}

    # Theme toggle
    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode

    # Notifications
    def show_toast(self, message: str, type: str = "info"):
        self.notification_message = message
        self.notification_type = type
        self.show_notification = True

    def hide_notification(self):
        self.show_notification = False
        self.notification_message = ""

    # Export functionality
    def export_to_csv(self):
        """Export current filtered/sorted claims to CSV"""
        import csv
        import io
        from datetime import datetime

        try:
            # Get current filtered and sorted claims
            claims = self.sorted_claims

            if not claims:
                self.show_toast("No data to export", "warning")
                return

            # Create CSV in memory
            output = io.StringIO()
            fieldnames = ["id", "claim_date", "claim_amount", "status", "risk_score"]
            writer = csv.DictWriter(output, fieldnames=fieldnames)

            writer.writeheader()
            for claim in claims:
                writer.writerow({
                    "id": claim.get("id", ""),
                    "claim_date": claim.get("claim_date", ""),
                    "claim_amount": claim.get("claim_amount", ""),
                    "status": claim.get("status", ""),
                    "risk_score": claim.get("risk_score", ""),
                })

            # Trigger download
            csv_content = output.getvalue()
            filename = f"claims_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

            self.show_toast(f"Exported {len(claims)} claims successfully!", "success")

            return csv_content

        except Exception as e:
            self.show_toast(f"Export failed: {str(e)}", "error")
            return None

    async def load_all_data(self):
        await self.load_summary()
        await self.load_claims()
        await self.load_risk_analysis()
        await self.load_providers()

    # Data Management
    is_loading_data: bool = False

    async def load_kaggle_data(self):
        """Load real insurance data from Kaggle"""
        self.is_loading_data = True
        self.show_toast("Downloading Kaggle dataset...", "info")

        try:
            async with httpx.AsyncClient(timeout=300.0) as client:  # 5 min timeout
                response = await client.post(f"{API_URL}/data/load-kaggle")

                if response.status_code == 200:
                    result = response.json()
                    if result.get("success"):
                        message = f"Loaded {result.get('claims_count', 0)} claims and {result.get('providers_count', 0)} providers from Kaggle!"
                        self.show_toast(message, "success")
                        # Reload data
                        await self.load_all_data()
                    else:
                        self.show_toast(result.get("message", "Failed to load Kaggle data"), "error")
                else:
                    self.show_toast("Failed to load Kaggle data. Check API logs.", "error")

        except httpx.TimeoutException:
            self.show_toast("Request timed out. Kaggle download may take a few minutes on first run.", "warning")
        except Exception as e:
            self.show_toast(f"Error loading Kaggle data: {str(e)}", "error")
        finally:
            self.is_loading_data = False

    async def generate_sample_data(self, num_claims: int = 1000):
        """Generate synthetic sample data"""
        self.is_loading_data = True
        self.show_toast(f"Generating {num_claims} sample claims...", "info")

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{API_URL}/data/generate-sample",
                    params={"num_claims": num_claims}
                )

                if response.status_code == 200:
                    result = response.json()
                    if result.get("success"):
                        message = f"Generated {result.get('claims_count', 0)} claims and {result.get('providers_count', 0)} providers!"
                        self.show_toast(message, "success")
                        # Reload data
                        await self.load_all_data()
                    else:
                        self.show_toast(result.get("message", "Failed to generate data"), "error")
                else:
                    self.show_toast("Failed to generate sample data. Check API logs.", "error")

        except Exception as e:
            self.show_toast(f"Error generating sample data: {str(e)}", "error")
        finally:
            self.is_loading_data = False

    async def clear_all_data(self):
        """Clear all data from the database"""
        self.is_loading_data = True
        self.show_toast("Clearing all data...", "info")

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(f"{API_URL}/data/clear-data")

                if response.status_code == 200:
                    result = response.json()
                    if result.get("success"):
                        self.show_toast(result.get("message", "Data cleared successfully"), "success")
                        # Reload data (should be empty now)
                        await self.load_all_data()
                    else:
                        self.show_toast("Failed to clear data", "error")
                else:
                    self.show_toast("Failed to clear data. Check API logs.", "error")

        except Exception as e:
            self.show_toast(f"Error clearing data: {str(e)}", "error")
        finally:
            self.is_loading_data = False
