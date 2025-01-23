from locust import task, run_single_user, between
from locust import FastHttpUser

class browse(FastHttpUser):
    host = "http://localhost:5000"
    
    # Define common headers to avoid redundancy
    default_headers = {
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "DNT": "1",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    }

    # Optionally, add a token or cookie setup in on_start
    def on_start(self):
        # If token or cookie setup is required
        self.token = "your_token_here"  # Replace with actual token retrieval if needed
        self.headers = {
            **self.default_headers,
            "Cookies": f"token={self.token}",  # Add token if needed
        }
    
    @task
    def t(self):
        with self.client.request(
            "GET",
            "/browse",
            headers=self.headers,  # Reuse headers here
            catch_response=True,
        ) as resp:
            if resp.status_code != 200:
                resp.failure(f"Failed to load /browse: {resp.status_code}")
            else:
                resp.success()

if __name__ == "__main__":
    run_single_user(browse)
