"""Persistent welcome, staged lighting and copy, preferences, and unchanged sections."""
import os
from playwright.sync_api import sync_playwright
base = os.environ.get('BASE_URL', 'http://127.0.0.1:8000')
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH', '/usr/bin/chromium'), args=['--no-sandbox'])
    for width, height in [(320,740),(390,844),(844,390),(1440,900)]:
        page = browser.new_page(viewport={'width':width,'height':height})
        page.add_init_script('Object.defineProperty(navigator,"hardwareConcurrency",{get:()=>8});Object.defineProperty(navigator,"deviceMemory",{get:()=>8});')
        page.goto(base,wait_until='domcontentloaded')
        page.locator('.welcome-hero.is-running').wait_for()
        for elapsed, expected in [(0,[0,0,0]),(1150,[1,0,0]),(2100,[1,1,0]),(3100,[1,1,1])]:
            values=page.evaluate('''time=>['.ignition-rings','.ignition-headlights','.ignition-roof'].map(selector=>{
              const node=document.querySelector(selector);node.getAnimations().forEach(a=>{a.pause();a.currentTime=time});return Number(getComputedStyle(node).opacity);
            })''',elapsed)
            assert all(abs(a-b)<.02 for a,b in zip(values,expected)),(elapsed,values)
        page.wait_for_function("document.querySelector('.welcome-hero').classList.contains('is-complete')",timeout=8500)
        assert page.locator('.welcome-hero').is_visible()
        assert page.locator('.intro,.hero').count()==0
        assert page.locator('.welcome-actions a').all_text_contents()==['Découvrir l’application','Explorer']
        assert page.locator('.welcome-actions').evaluate('(n)=>getComputedStyle(n).opacity')=='1'
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
        # Text must begin below the roof lights on phones and beside them on desktop.
        text=page.locator('.welcome-copy').bounding_box();art=page.locator('.ignition-stage').bounding_box()
        if width<=760: assert text['y']>art['y']+art['height']*.65
        else: assert text['x']>=art['x']+art['width']-1
        page.locator('.welcome-actions a[href="#explore"]').click();page.wait_for_timeout(750)
        assert page.evaluate('location.hash')=='#explore'
        page.locator('#accueil').scroll_into_view_if_needed()
        assert page.locator('.welcome-hero').is_visible()
        print(f'{width}×{height}: lights, persistent copy, layout and Explorer link pass',flush=True)
        page.close()
    for mode in ['reduced','slow','failed','no-js']:
        page=browser.new_page(reduced_motion='reduce' if mode=='reduced' else 'no-preference',java_script_enabled=mode!='no-js')
        if mode=='slow':page.add_init_script('Object.defineProperty(navigator,"hardwareConcurrency",{get:()=>2});')
        if mode=='failed':page.route('**/assets/scene-front-1536.webp',lambda route:route.abort())
        page.goto(base,wait_until='domcontentloaded')
        if mode=='slow':
            page.locator('.welcome-hero.is-running').wait_for()
            assert not page.locator('.welcome-hero').evaluate('(n)=>n.classList.contains("is-complete")')
        if mode!='no-js':page.wait_for_function("document.querySelector('.welcome-hero').classList.contains('is-complete')",timeout=8500)
        assert page.locator('.welcome-actions').evaluate('(n)=>getComputedStyle(n).opacity')=='1'
        print(mode+': welcome content remains available',flush=True)
        page.close()
    browser.close()
