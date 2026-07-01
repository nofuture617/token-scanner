"""Browser automation manager using Playwright."""
import asyncio
from typing import Optional
from loguru import logger
from playwright.async_api import async_playwright, Browser, Page


class BrowserManager:
    """Manages browser automation with Playwright."""

    def __init__(self, headless: bool = True, auto_open: bool = True, new_tab: bool = True):
        """Initialize browser manager.

        Args:
            headless: Run browser in headless mode
            auto_open: Auto open browser for tokens
            new_tab: Open in new tab instead of window
        """
        self.headless = headless
        self.auto_open = auto_open
        self.new_tab = new_tab
        self.browser: Optional[Browser] = None
        self.opened_urls = set()

    async def initialize(self) -> None:
        """Initialize browser."""
        try:
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.launch(headless=self.headless)
            logger.info(f"Browser initialized (headless={self.headless})")
        except Exception as e:
            logger.error(f"Failed to initialize browser: {e}")
            raise

    async def open_url(self, url: str) -> Optional[Page]:
        """Open URL in browser.

        Args:
            url: URL to open

        Returns:
            Browser page or None
        """
        if not self.auto_open or not self.browser:
            logger.debug(f"Browser auto-open disabled or not initialized: {url}")
            return None

        # Prevent duplicate opens
        if url in self.opened_urls:
            logger.debug(f"URL already opened: {url}")
            return None

        try:
            # Create new context
            context = await self.browser.new_context()
            page = await context.new_page()

            # Navigate to URL
            await page.goto(url, wait_until="domcontentloaded")
            self.opened_urls.add(url)

            logger.info(f"Opened URL in browser: {url}")
            return page
        except Exception as e:
            logger.error(f"Failed to open URL: {e}")
            return None

    async def open_token_page(self, token_mint: str, token_name: str) -> Optional[Page]:
        """Open token page on Axiom Trade.

        Args:
            token_mint: Token mint address
            token_name: Token name/symbol

        Returns:
            Browser page or None
        """
        url = f"https://axiom.trade/token/{token_mint}"
        logger.info(f"Opening token page: {token_name} ({token_mint})")
        return await self.open_url(url)

    async def close(self) -> None:
        """Close browser."""
        if self.browser:
            await self.browser.close()
            logger.info("Browser closed")

    def get_opened_urls(self) -> set:
        """Get set of opened URLs.

        Returns:
            Set of URLs
        """
        return self.opened_urls.copy()
