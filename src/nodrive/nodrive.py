import asyncio

import nodriver as uc


async def main():
    browser = await uc.start()
    page = await browser.get("https://www.nowsecure.nl")

    await page.save_screenshot()
    await page.get_content()
    await page.scroll_down(150)
    elems = await page.select_all("*[src]")
    for elem in elems:
        await elem.flash()

    page1 = await browser.get("https://www.zhihu.com", new_tab=True)
    await page1.bring_to_front()
    await page1.scroll_down(200)
    await page1  # wait for events to be processed
    await page1.reload()
    await asyncio.sleep(5)


if __name__ == "__main__":

    # since asyncio.run never worked (for me)
    uc.loop().run_until_complete(main())
