"""Exercise static copy, SEO, browser choice, storage and responsive language navigation."""
import os
import subprocess
from pathlib import Path
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
subprocess.run(['python',str(ROOT/'scripts/build_i18n.py'),'--check'],check=True)
BASE=os.environ.get('BASE_URL','http://127.0.0.1:8000').rstrip('/')+'/'
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),args=['--no-sandbox'])
    errors=[]
    for locale,expected in [('fr-FR','fr'),('en-GB','en'),('nl-NL','en'),('de-DE','en')]:
        context=browser.new_context(locale=locale,reduced_motion='reduce')
        page=context.new_page();page.goto(BASE,wait_until='domcontentloaded')
        page.wait_for_function('lang=>document.documentElement.lang===lang',arg=expected)
        page.wait_for_load_state('domcontentloaded')
        assert page.evaluate('localStorage.getItem("beaver-language")')==expected
        print(locale+': browser detection and first-visit persistence pass',flush=True)
        context.close()
    for width in [320,390,768,1440]:
        for lang in ['fr','en']:
            context=browser.new_context(locale='en-GB',viewport={'width':width,'height':900},is_mobile=width<768,has_touch=width<768,reduced_motion='reduce')
            page=context.new_page();page.on('pageerror',lambda error:errors.append(str(error)))
            url=BASE+('en/' if lang=='en' else '?lang=fr')
            page.goto(url,wait_until='domcontentloaded')
            assert page.locator('html').get_attribute('lang')==lang
            assert page.locator('.language-switch').is_visible()
            assert page.locator('[data-language="'+lang+'"]').get_attribute('aria-current')=='page'
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,lang)
            assert page.locator('.vehicle').count()==4
            assert page.locator('.showcase-slide').count()==6
            assert 'PRÉPARE · EXPLORE · PARTAGE' in page.locator('header').inner_text()
            assert page.locator('.welcome-actions a').all_text_contents()==(['Découvrir l’application','Explorer'] if lang=='fr' else ['Discover the app','Explore'])
            assert page.locator('link[rel="alternate"][hreflang="fr"]').count()==1
            assert page.locator('link[rel="alternate"][hreflang="en"]').count()==1
            assert page.locator('meta[name="description"]').get_attribute('content')
            if lang=='en':
                assert page.locator('.showcase-carousel').get_attribute('aria-roledescription')=='carousel'
                assert 'ADVENTURE' in page.locator('.vehicle .info').first.evaluate('(n)=>getComputedStyle(n,"::before").content')
                assert page.locator('.phone-title').all_text_contents()==['Home','Garage','AI Copilot','Trails','Club','Profile']
                assert page.locator('.showcase-arrow.next').get_attribute('aria-label')=='Next preview'
                track=page.locator('.showcase-track')
                track.scroll_into_view_if_needed()
                track.evaluate('(n)=>n.scrollTo({left:0,behavior:"instant"})')
                page.wait_for_timeout(100)
                page.locator('.showcase-arrow.next').click()
                page.wait_for_timeout(100)
                assert track.evaluate('(n)=>n.scrollLeft')>0
                # Load every local image, including offscreen cards and original app captures.
                page.locator('img').evaluate_all('(imgs)=>imgs.filter(i=>new URL(i.src).origin===location.origin).forEach(i=>i.loading="eager")')
                assert page.locator('img').evaluate_all('async imgs=>{await Promise.all(imgs.filter(i=>new URL(i.src).origin===location.origin).map(i=>i.decode()));return true}')
            page.locator('.welcome-actions a[href="#fonctionnalites"]').click();page.wait_for_timeout(150)
            assert page.evaluate('location.hash')=='#fonctionnalites'
            other='en' if lang=='fr' else 'fr'
            page.locator('[data-language="'+other+'"]').click()
            page.wait_for_function('lang=>document.documentElement.lang===lang',arg=other)
            assert page.evaluate('location.hash')=='#fonctionnalites'
            assert page.evaluate('localStorage.getItem("beaver-language")')==other
            page.goto(BASE,wait_until='domcontentloaded')
            page.wait_for_function('lang=>document.documentElement.lang===lang',arg=other)
            print(f'{width}px {lang}: copy, responsive selector, assets, anchor switch and remembered choice pass',flush=True)
            context.close()
    for name in ['assistance.html','confidentialite.html']:
        for lang in ['fr','en']:
            context=browser.new_context(locale='en-GB',viewport={'width':320,'height':740},reduced_motion='reduce')
            page=context.new_page()
            path=('en/' if lang=='en' else '')+name+('?lang=fr' if lang=='fr' else '')
            page.goto(BASE+path,wait_until='domcontentloaded')
            assert page.locator('html').get_attribute('lang')==lang
            assert page.locator('.language-switch').is_visible()
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(name,lang)
            assert page.locator('link[rel="canonical"]').get_attribute('href').endswith(('en/' if lang=='en' else '/')+name)
            if lang=='en': assert page.locator('h2').inner_text() in ['Need help?','Privacy policy']
            print(name+' '+lang+': localized content, SEO and mobile layout pass',flush=True)
            context.close()
    # Explicit shared URLs take priority over stored preferences and browser language.
    context=browser.new_context(locale='fr-FR',reduced_motion='reduce');page=context.new_page()
    page.goto(BASE+'?lang=fr');page.goto(BASE+'en/');assert page.locator('html').get_attribute('lang')=='en'
    page.goto(BASE+'en/?lang=fr');page.wait_for_function('document.documentElement.lang==="fr"')
    assert '/en/' not in urlparse(page.url).path
    context.close()
    context=browser.new_context(locale='fr-FR',java_script_enabled=False)
    page=context.new_page();page.goto(BASE+'en/',wait_until='domcontentloaded')
    assert page.locator('html').get_attribute('lang')=='en'
    assert page.locator('.welcome-headline').inner_text()=='Off-road adventure.\nWith intelligence built in.'
    context.close()
    context=browser.new_context(locale='fr-FR',reduced_motion='reduce')
    page=context.new_page();page.goto(BASE+'?lang=en',wait_until='domcontentloaded');page.wait_for_function('document.documentElement.lang==="en"')
    context.close()
    # Storage failure must not prevent switching or retaining French on other pages.
    context=browser.new_context(locale='en-GB',reduced_motion='reduce');context.add_init_script('Storage.prototype.getItem=function(){throw new Error("blocked")};Storage.prototype.setItem=function(){throw new Error("blocked")};')
    page=context.new_page();page.goto(BASE+'?lang=fr');page.locator('a[href*="confidentialite.html"]').click();page.wait_for_load_state('domcontentloaded');assert page.locator('html').get_attribute('lang')=='fr'
    page.locator('[data-language="en"]').click();page.wait_for_function('document.documentElement.lang==="en"')
    context.close()
    assert not errors,errors
    print('Explicit links, blocked storage and zero JavaScript errors: pass',flush=True)
    browser.close()
