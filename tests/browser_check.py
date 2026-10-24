from playwright.sync_api import sync_playwright
import json
import os
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH', '/usr/bin/chromium'),headless=True,args=['--no-sandbox'])
 errors=[]
 for width,height in [(320,740),(375,812),(390,844),(430,932),(768,1024),(1440,900),(844,390)]:
  page=browser.new_page(viewport={'width':width,'height':height},is_mobile=width<800,has_touch=True)
  page.on('pageerror',lambda e: errors.append(str(e)))
  page.goto(os.environ.get('BASE_URL', 'http://127.0.0.1:8000'),wait_until='domcontentloaded')
  page.wait_for_timeout(3000)
  assert page.locator('.vehicle').count()==7
  assert page.locator('.explore-scene').count()==6
  assert page.locator('.is-placeholder').count()==0
  for image in page.locator('.vehicle img,.showcase-track img,.explore-media img').all():
   image.scroll_into_view_if_needed()
   image.evaluate('(img)=>img.decode()')
   assert image.evaluate('(img)=>img.naturalWidth > 0')
  assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),f'overflow {width}'
  for a in page.locator('a[href^="#"]').all():
   href=a.get_attribute('href');assert page.locator(href).count()==1,href
  track=page.locator('.showcase-track')
  track.scroll_into_view_if_needed()
  track.evaluate('(e)=>e.scrollTo({left:0,behavior:"instant"})')
  page.wait_for_timeout(100)
  if track.evaluate('(e)=>e.scrollWidth>e.clientWidth+2'):
   page.locator('.showcase-arrow.next').click()
   page.wait_for_timeout(800)
   assert track.evaluate('(e)=>e.scrollLeft')>0
  else:
   assert page.locator('.showcase-arrow.next').is_disabled()
  for scene in page.locator('.explore-scene').all():
   scene.scroll_into_view_if_needed();page.wait_for_timeout(100)
   assert 'explore-pending' not in (scene.get_attribute('class') or '')
  for path in ['confidentialite.html','assistance.html']:
   assert page.request.get(os.environ.get('BASE_URL','http://127.0.0.1:8000')+'/'+path).status==200
  print(json.dumps({'viewport':[width,height],'horizontalOverflow':False,'scenes':6,'vehicles':7,'carouselNext':'pass'}))
  page.close()
 page=browser.new_page(viewport={'width':390,'height':844},reduced_motion='reduce')
 page.goto(os.environ.get('BASE_URL', 'http://127.0.0.1:8000'),wait_until='domcontentloaded')
 assert page.locator('.intro').evaluate('(e)=>getComputedStyle(e).display')=='none'
 assert page.locator('.explore-pending').count()==0
 print('Reduced motion: pass; JS errors:',errors)
 assert not errors
 browser.close()
