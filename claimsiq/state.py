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
    
    async def load_all_data(self):
        await self.load_summary()
        await self.load_claims()
        await self.load_risk_analysis()
        await self.load_providers()
