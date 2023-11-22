import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def scrape_hrefs():
    async with async_playwright() as p:
        # Launch the browser
        browser = await p.chromium.launch(headless=False)  # Set headless=True to run without a browser UI
        page = await browser.new_page()

        url = 'https://www.public.gr'
        await page.goto(url)

        # Click the menu item to reveal the "Black Friday 2023" link
        #await asyncio.sleep(2)  # Wait for the menu to open
        cookie_consent_button = await page.wait_for_selector('#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')
        if cookie_consent_button:
            await cookie_consent_button.click()
        else:
            print("Cookie consent button not found")
            return
        # Click on the "Black Friday 2023" link
        black_friday_link = await page.query_selector('.ic-black-friday.mdc-list-item__graphic')
        
        if black_friday_link:
            await black_friday_link.click()
        else:
            print("Black Friday 2023 link not found")
            return

        await asyncio.sleep(1)  # Wait for the page to load the content

        # Get the HTML content of the page
        page_content = await page.content()

        soup = BeautifulSoup(page_content, 'html.parser')

        filtered_elements = soup.find_all('a', class_='mdc-link-button animate mdc-link-button--black text-left')

        # Extract hrefs
        hrefs = [url + element.get('href') for element in filtered_elements]

        # Write the hrefs to a text file
        with open('extracted_hrefs.txt', 'w') as file:
            for href in hrefs:
                file.write(href + '\n')

        # Close the browser
        await browser.close()

        print('Hrefs extracted and saved to extracted_hrefs.txt')

# Run the async function
asyncio.run(scrape_hrefs())
