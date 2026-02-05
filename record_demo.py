import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=False, slow_mo=150)
        context = await browser.new_context(record_video_dir="videos/")
        page = await context.new_page()

        # Navigate to Streamlit
        print("Navigating to UI...")
        await page.goto("http://localhost:8503")
        await page.wait_for_timeout(5000) # Wait for load

        # Interaction 1
        print("Typing prompt 1...")
        # Streamlit input fields are tricky, we target the input
        await page.get_by_placeholder("What is the future of AI?").fill("What is PagedAttention?")
        await page.keyboard.press("Enter")
        print("Waiting for response 1...")
        await page.wait_for_timeout(15000) # Wait for generation (increased for CPU)

        # Interaction 2
        print("Typing prompt 2...")
        await page.get_by_placeholder("What is the future of AI?").fill("How does continuous batching work?")
        await page.keyboard.press("Enter")
        print("Waiting for response 2...")
        await page.wait_for_timeout(15000)

        # Scroll
        await page.mouse.wheel(0, 500)
        await page.wait_for_timeout(1000)

        # Close
        await context.close()
        await browser.close()
        print("Video saved to videos/ directory")

if __name__ == "__main__":
    asyncio.run(run())
