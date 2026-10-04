const { chromium } = require('playwright');
const fs=require('fs'),path=require('path');
const CACHE=path.join(__dirname,'fontcache');  // optional; see README
let FONT_MAP={}, FONT_CSS='';
try { for(const l of fs.readFileSync(path.join(CACHE,'map.txt'),'utf8').trim().split('\n')){const[u,f]=l.split(' ');if(u&&f)FONT_MAP[u]=path.join(CACHE,f);}
      FONT_CSS=fs.readFileSync(path.join(CACHE,'fonts.css'),'utf8'); } catch(e) { /* no cache: fonts fall back */ }
const STUB=Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==','base64');
const B='http://127.0.0.1:8099';
let pass=0, fail=0;
function ok(name,cond,extra){ if(cond){pass++;console.log('  PASS  '+name);} else {fail++;console.log('  FAIL  '+name+(extra?'  ['+extra+']':''));} }
async function ctx(b,w=1280,h=900,mobile=false,opts={}){
  const c=await b.newContext({viewport:{width:w,height:h},hasTouch:mobile,isMobile:mobile});
  ctx.weather=opts.weather||null;
  await c.route('**/*',async r=>{const u=r.request().url();
    if(u.startsWith('https://fonts.googleapis.com/'))return r.fulfill({status:200,contentType:'text/css',body:FONT_CSS});
    if(/api\.open-meteo\.com/.test(u)&&ctx.weather)return ctx.weather(r);
    if(FONT_MAP[u])return r.fulfill({status:200,contentType:'font/woff2',body:fs.readFileSync(FONT_MAP[u])});
    if(u.startsWith('https://fonts.gstatic.com/'))return r.fulfill({status:200,contentType:'font/woff2',body:Buffer.alloc(0)});
    if(/cloudinary|unsplash|googletagmanager|google-analytics/.test(u))return r.request().resourceType()==='image'?r.fulfill({status:200,contentType:'image/png',body:STUB}):r.fulfill({status:200,body:''});
    return r.continue();});
  return c;
}
(async()=>{
 const b=await chromium.launch();
 const errs=[];

 // ── Destination explorer
 console.log('\nDESTINATION EXPLORER  /discover-nashik/');
 { const c=await ctx(b); const p=await c.newPage();
   p.on('pageerror',e=>errs.push('discover: '+e.message));
   await p.goto(B+'/discover-nashik/',{waitUntil:'load'}); await p.waitForTimeout(600);
   const visible=async()=>p.$$eval('[data-filter-items] [data-tags]',els=>els.filter(e=>!e.hidden).length);
   ok('all 5 shown initially', await visible()===5, 'got '+await visible());
   await p.evaluate(()=>window.scrollTo(0,document.body.scrollHeight)); await p.waitForTimeout(900);
   await p.evaluate(()=>window.scrollTo(0,0)); await p.waitForTimeout(400);
   ok('all cards reveal after scrolling (was the opacity:0 blocker)', await p.$$eval('.dest-card',els=>els.every(e=>+getComputedStyle(e).opacity>0.9)),
      'opacities: '+(await p.$$eval('.dest-card',els=>els.map(e=>getComputedStyle(e).opacity).join(','))));
   await p.click('#cat-spiritual'); await p.waitForTimeout(200);
   ok('spiritual filters to 2', await visible()===2, 'got '+await visible());
   ok('aria-pressed set', await p.getAttribute('#cat-spiritual','aria-pressed')==='true');
   ok('count text updates', (await p.textContent('[data-filter-count]')).includes('2'));
   ok('status live region announces', (await p.textContent('[data-filter-status]')).includes('2 results'));
   await p.click('#cat-wine'); await p.waitForTimeout(200);
   ok('wine filters to 1', await visible()===1, 'got '+await visible());
   await p.click('[data-filter="all"]'); await p.waitForTimeout(200);
   ok('all restores 5', await visible()===5);
   await c.close(); }

 // ── Deep link from a destination page CTA
 console.log('\nCONTEXTUAL CTA DEEP LINK');
 { const c=await ctx(b); const p=await c.newPage();
   await p.goto(B+'/discover-nashik/#cat-wine',{waitUntil:'load'}); await p.waitForTimeout(700);
   const v=await p.$$eval('[data-filter-items] [data-tags]',els=>els.filter(e=>!e.hidden).length);
   ok('#cat-wine preselects the wine filter', v===1, 'got '+v);
   await c.close(); }

 // ── Trip planner
 console.log('\nTRIP PLANNER  /plan-your-trip/');
 { const c=await ctx(b); const p=await c.newPage();
   p.on('pageerror',e=>errs.push('planner: '+e.message));
   await p.goto(B+'/plan-your-trip/',{waitUntil:'load'}); await p.waitForTimeout(600);
   const shown=async()=>p.$$eval('[data-plan]',els=>els.filter(e=>!e.hidden).map(e=>e.id));
   ok('all 4 itineraries visible before interaction', (await shown()).length===4, (await shown()).join(','));
   await p.click('#day-2'); await p.waitForTimeout(200);
   ok('2 days -> only the two-day plan', JSON.stringify(await shown())==='["plan-2"]', (await shown()).join(','));
   await p.click('#day-1'); await p.waitForTimeout(200);
   ok('1 day -> both one-day variants', (await shown()).length===2, (await shown()).join(','));
   await p.click('[data-interest="wine"]'); await p.waitForTimeout(200);
   ok('1 day + wine -> the vineyard variant', JSON.stringify(await shown())==='["plan-1-wine"]', (await shown()).join(','));
   await p.click('[data-interest="wine"]'); await p.waitForTimeout(200);
   ok('deselecting interest widens again', (await shown()).length===2);
   await p.click('#day-3'); await p.waitForTimeout(200);
   ok('3 days -> the three-day plan', JSON.stringify(await shown())==='["plan-3"]');
   await c.close(); }

 // ── Guide index filter + search
 console.log('\nGUIDE INDEX  /blog/');
 { const c=await ctx(b); const p=await c.newPage();
   p.on('pageerror',e=>errs.push('blog: '+e.message));
   await p.goto(B+'/blog/',{waitUntil:'load'}); await p.waitForTimeout(600);
   const vis=async()=>p.$$eval('[data-filter-items] [data-tags]',els=>els.filter(e=>!e.hidden).length);
   const total=await p.$$eval('[data-filter-items] [data-tags]',e=>e.length);
   ok('all 22 guides participate in filtering', total===22, 'got '+total);
   await p.click('#cat-kumbh-mela'); await p.waitForTimeout(200);
   ok('Kumbh filter -> 9', await vis()===9, 'got '+await vis());
   await p.click('[data-filter="all"]');
   await p.fill('[data-filter-search]','vineyard'); await p.waitForTimeout(320);
   const n=await vis(); ok('search "vineyard" narrows', n>0 && n<22, 'got '+n);
   await p.fill('[data-filter-search]','zzzzqqq'); await p.waitForTimeout(320);
   ok('no-match shows empty state', await p.$eval('[data-filter-empty]',e=>!e.hidden) && await vis()===0);
   await c.close(); }

 // ── Nav + mobile menu + keyboard
 console.log('\nNAVIGATION');
 { const c=await ctx(b,390,800,true); const p=await c.newPage();
   p.on('pageerror',e=>errs.push('nav: '+e.message));
   await p.goto(B+'/',{waitUntil:'load'}); await p.waitForTimeout(400);
   ok('mobile menu closed initially', await p.$eval('#mobileMenu',e=>!e.classList.contains('open')));
   ok('closed menu is out of the tab order (visibility:hidden)', await p.$eval('#mobileMenu',e=>getComputedStyle(e).visibility==='hidden'));
   await p.click('#hamburger'); await p.waitForTimeout(350);
   ok('hamburger opens menu', await p.$eval('#mobileMenu',e=>e.classList.contains('open')));
   ok('aria-expanded=true', await p.getAttribute('#hamburger','aria-expanded')==='true');
   ok('body scroll locked', await p.$eval('body',e=>e.style.overflow==='hidden'));
   await p.keyboard.press('Escape'); await p.waitForTimeout(350);
   ok('Escape closes menu', await p.$eval('#mobileMenu',e=>!e.classList.contains('open')));
   await p.click('#hamburger'); await p.waitForTimeout(350);
   const tiles=await p.$$eval('.mm-tile',els=>els.map(e=>Math.round(e.getBoundingClientRect().height)));
   ok('menu leads with six priority tiles, each >= 44px tall', tiles.length===6 && tiles.every(h=>h>=44), tiles.join(','));
   await p.keyboard.press('Escape'); await p.waitForTimeout(350);
   ok('body scroll restored', await p.$eval('body',e=>e.style.overflow===''));
   await c.close(); }
 { const c=await ctx(b); const p=await c.newPage();
   await p.goto(B+'/blog/',{waitUntil:'load'}); await p.waitForTimeout(400);
   await p.click('.chevron-btn'); await p.waitForTimeout(250);
   ok('dropdown opens on chevron click', await p.$eval('.dropdown',e=>e.classList.contains('open')));
   ok('dropdown aria-expanded', await p.getAttribute('.chevron-btn','aria-expanded')==='true');
   await p.keyboard.press('Escape'); await p.waitForTimeout(250);
   ok('Escape closes dropdown', await p.$eval('.dropdown',e=>!e.classList.contains('open')));
   await c.close(); }

 // ── Sticky section nav active state
 console.log('\nSTICKY SECTION NAV  /discover-nashik/trimbakeshwar/');
 { const c=await ctx(b); const p=await c.newPage();
   p.on('pageerror',e=>errs.push('dest: '+e.message));
   await p.goto(B+'/discover-nashik/trimbakeshwar/',{waitUntil:'load'}); await p.waitForTimeout(500);
   await p.evaluate(()=>document.getElementById('tips').scrollIntoView()); await p.waitForTimeout(700);
   const cur=await p.$$eval('.dest-nav a.is-current',els=>els.map(e=>e.getAttribute('href')));
   ok('a section is marked current after scrolling', cur.length===1, cur.join(','));
   ok('quick facts rendered', await p.$$eval('.qf-item',e=>e.length)>=4);
   ok('plan-next CTA present', !!(await p.$('#plan-next .btn')));
   await c.close(); }


 // ── Search dialog
 console.log('\nSEARCH DIALOG');
 { const c=await ctx(b,390,800,true); const p=await c.newPage();
   p.on('pageerror',e=>errs.push('search: '+e.message));
   await p.goto(B+'/',{waitUntil:'load'}); await p.waitForTimeout(400);
   ok('header search is a real link to /search/ (works without JS)', await p.getAttribute('#searchOpen','href')==='/search/');
   await p.click('#searchOpen'); await p.waitForTimeout(300);
   ok('dialog opens', await p.$eval('#searchDialog',e=>e.open));
   ok('input is focused', await p.evaluate(()=>document.activeElement&&document.activeElement.id==='searchInput'));
   ok('popular searches are offered', (await p.$$('#searchTry a')).length>=8);
   await p.fill('#searchInput','Trimbakeshwar timing'); await p.waitForTimeout(700);
   const links=await p.$$eval('#searchBody .sr-item a',els=>els.map(e=>e.getAttribute('href')));
   ok('"Trimbakeshwar timing" finds the destination', links.some(h=>h.indexOf('/discover-nashik/trimbakeshwar/')===0), links.slice(0,4).join(' '));
   ok('result count announced in a live region', /result/.test(await p.textContent('#searchStatus')));
   await p.keyboard.press('ArrowDown'); await p.waitForTimeout(100);
   ok('ArrowDown moves focus to the first result', await p.evaluate(()=>!!document.activeElement.closest('.sr-item')));
   await p.keyboard.press('Escape'); await p.waitForTimeout(300);
   ok('Escape closes the dialog', await p.$eval('#searchDialog',e=>!e.open));
   ok('focus returns to the search control', await p.evaluate(()=>document.activeElement.id==='searchOpen'));
   await p.click('#searchOpen'); await p.fill('#searchInput','zzzzqq'); await p.waitForTimeout(600);
   ok('no match shows guidance, not a blank', /Nothing found/.test(await p.textContent('#searchBody')));
   await c.close(); }

 console.log('\nSEARCH PAGE  /search/?q=Kumbh+parking');
 { const c=await ctx(b); const p=await c.newPage();
   p.on('pageerror',e=>errs.push('search page: '+e.message));
   await p.goto(B+'/search/?q=Kumbh+parking',{waitUntil:'load'}); await p.waitForTimeout(900);
   const first=await p.$eval('#sp-results .sr-item a',e=>e.getAttribute('href')).catch(()=> '');
   ok('top result for "Kumbh parking" is the parking section', first.indexOf('/kumbh-mela-2027/#parking-roads')===0, first);
   ok('page is noindex', (await p.$eval('meta[name=robots]',e=>e.content)).indexOf('noindex')>-1);
   ok('browse-everything list is present', (await p.$$('#browse a')).length>20);
   await c.close(); }

 // ── Time-sensitive behaviour in the browser
 console.log('\nEXPIRY AND LIFECYCLE (client side)');
 { const c=await ctx(b); const p=await c.newPage();
   await p.route('**/updates/',async r=>{const resp=await r.fetch(); let body=await resp.text();
     body=body.replace(/data-status="changed"/,'data-status="changed" data-expires="2020-01-01T23:59:59+05:30"'); r.fulfill({response:resp,body});});
   await p.goto(B+'/updates/',{waitUntil:'load'}); await p.waitForTimeout(400);
   ok('an update past its expiry is shown as Archived without a rebuild', await p.$eval('.update-card',e=>e.getAttribute('data-status')==='archived' && /Archived/.test(e.querySelector('.st').textContent)));
   await c.close(); }
 for (const [when, wantBand, wantTop, wantReduced] of [['2026-10-04T10:00:00+05:30',false,true,false],['2027-08-02T10:00:00+05:30',true,true,false],['2028-08-05T10:00:00+05:30',false,false,true]]) {
   const c=await ctx(b); const p=await c.newPage();
   await p.clock.install({time:new Date(when)});
   await p.goto(B+'/',{waitUntil:'load'}); await p.waitForTimeout(400);
   const band=await p.$eval('[data-phase-flag="liveBand"]',e=>!e.hidden);
   const top=await p.$eval('[data-phase-id~="preparation"]',e=>!e.hidden);
   const red=await p.$eval('[data-phase-id~="post_kumbh"]',e=>!e.hidden);
   ok('phase for '+when.slice(0,10)+': live band '+(wantBand?'on':'off')+', Kumbh card '+(wantTop?'full':'reduced'), band===wantBand && top===wantTop && red===wantReduced, [band,top,red].join(','));
   await c.close(); }

 // ── Weather: success and graceful failure
 console.log('\nWEATHER');
 { const good=r=>r.fulfill({status:200,contentType:'application/json',body:JSON.stringify({current:{temperature_2m:27.4,apparent_temperature:29.1,relative_humidity_2m:61,precipitation:0,weather_code:2,wind_speed_10m:9},daily:{time:['2026-10-04','2026-10-05','2026-10-06','2026-10-07'],weather_code:[2,3,61,1],temperature_2m_max:[31,30,28,32],temperature_2m_min:[21,20,20,21],precipitation_probability_max:[10,30,70,5]}})});
   const c=await ctx(b,1280,900,false,{weather:good}); const p=await c.newPage();
   await p.goto(B+'/nashik-now/',{waitUntil:'load'}); await p.waitForTimeout(800);
   const t=await p.textContent('[data-weather]');
   ok('weather renders temperature, condition and a fetch time', /27°C/.test(t) && /Partly cloudy/.test(t) && /Fetched/.test(t), t.slice(0,80));
   ok('weather is labelled model-based with an IMD link', /not an official forecast/.test(t) && !!(await p.$('[data-weather] a[href*="imd.gov.in"]')));
   ok('no raw undefined/NaN/null shown', !/undefined|NaN|null/.test(t));
   await c.close(); }
 for (const [label,handler] of [['network failure',r=>r.abort()],['HTTP 500',r=>r.fulfill({status:500,body:'x'})],['malformed JSON',r=>r.fulfill({status:200,contentType:'application/json',body:'{"current":{}}'})]]) {
   const c=await ctx(b,1280,900,false,{weather:handler}); const p=await c.newPage();
   await p.goto(B+'/nashik-now/',{waitUntil:'load'}); await p.waitForTimeout(900);
   const t=await p.textContent('[data-weather]');
   ok('weather '+label+' falls back to a sentence with an IMD link', /not available/.test(t) && !/undefined|NaN|null/.test(t) && !!(await p.$('[data-weather] a[href*="imd.gov.in"]')), t.slice(0,80));
   await c.close(); }

 // ── Keyboard: skip link is first, focus is visible
 console.log('\nKEYBOARD');
 { const c=await ctx(b,1280,900); const p=await c.newPage();
   await p.goto(B+'/kumbh-mela-2027/',{waitUntil:'load'}); await p.waitForTimeout(300);
   await p.keyboard.press('Tab');
   ok('first Tab stop is the skip link', await p.evaluate(()=>document.activeElement.classList.contains('skip-link')));
   await p.keyboard.press('Enter'); await p.waitForTimeout(150);
   ok('skip link lands on <main>', await p.evaluate(()=>location.hash==='#main'));
   const out=await p.evaluate(()=>{document.querySelector('.faq-item summary').focus();const cs=getComputedStyle(document.activeElement);return cs.outlineStyle!=='none'&&parseFloat(cs.outlineWidth)>=2;});
   ok('focus indicator is visible on an FAQ control', out);
   await c.close(); }

 await b.close();
 if(errs.length){ console.log('\nPAGE ERRORS:'); errs.forEach(e=>console.log('  '+e)); }
 console.log('\n'+pass+' passed, '+fail+' failed, '+errs.length+' page errors');
 process.exit(fail||errs.length?1:0);
})();
