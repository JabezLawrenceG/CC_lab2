from locust import task, FastHttpUser, between
from insert_product import login

class AddToCart(FastHttpUser):
    host = "http://localhost:5000"
    
    # Default headers are reused across tasks
    default_headers = {
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "DNT": "1",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    }

    # Execute once at the start for setting up login and token retrieval
    def on_start(self):
        self.username = "test123"
        self.password = "test123"
        cookies = login(self.username, self.password)
        self.token = cookies.get("token")
        
        self.headers = {  # Set headers specific for this user session
            "Cookie": f"token={self.token}",
            "Referer": f"{self.host}/product/1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
        }

    # Task for accessing the cart
    @task
    def view_cart(self):
        with self.client.get(
            "/cart", 
            headers={**self.default_headers, **self.headers}, 
            catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure("Failed to access cart")

if __name__ == "__main__":
    from locust import run_single_user
    run_single_user(AddToCart)
