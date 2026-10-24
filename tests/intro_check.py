"""Check the staged lights, skip control, mobile layout, and failed image fallback."""
import os
from playwright.sync_api import sync_playwright

base = os.environ.get('BASE_URL', 'http://127.0.0.1:8000')
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH', '/usr/bin/chromium'), args=['--no-sandbox'])
    for width, height in [(390, 844), (844, 390), (1440, 900)]:
        page = browser.new_page(viewport={'width': width, 'height': height})
        page.goto(base, wait_until='domcontentloaded')
        page.locator('.cinematic-intro.is-running').wait_for()
        for elapsed, expected in [(0, [0, 0, 0]), (1150, [1, 0, 0]), (2100, [1, 1, 0]), (3100, [1, 1, 1])]:
            values = page.evaluate('''time => ['.ignition-rings','.ignition-headlights','.ignition-roof'].map(selector => {
                const node = document.querySelector(selector);
                node.getAnimations().forEach(animation => { animation.pause(); animation.currentTime = time; });
                return Number(getComputedStyle(node).opacity);
            })''', elapsed)
            assert all(abs(actual - want) < .02 for actual, want in zip(values, expected)), (elapsed, values)
        page.locator('.intro-skip').click()
        assert page.locator('.intro').is_hidden()
        page.locator('#depart').scroll_into_view_if_needed()
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        assert page.locator('#depart img').evaluate('(i)=>i.decode().then(()=>i.naturalWidth>0)')
        print(f'{width}×{height}: ordered lights, skip, closing image and overflow pass', flush=True)
        page.close()
    page = browser.new_page()
    page.route('**/assets/scene-front-1536.webp', lambda route: route.abort())
    page.goto(base, wait_until='domcontentloaded')
    page.locator('.intro').wait_for(state='hidden', timeout=8500)
    print('Missing intro image: navigation released', flush=True)
    browser.close()
