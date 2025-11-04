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

    async def load_all_data(self):
        await self.load_summary()
        await self.load_claims()
        await self.load_risk_analysis()
        await self.load_providers()
