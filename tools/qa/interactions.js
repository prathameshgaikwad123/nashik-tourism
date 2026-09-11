const { chromium } = require('playwright');
const fs=require('fs'),path=require('path');
const CACHE=path.join(__dirname,'fontcache');  // optional; see README
const FONT_MAP={}; for(const l of fs.readFileSync(path.join(CACHE,'map.txt'),'utf8').trim().split('\n')){const[u,f]=l.split(' ');if(u&&f)FONT_MAP[u]=path.join(CACHE,f);}
const FONT_CSS=fs.readFileSync(path.join(CACHE,'fonts.css'),'utf8');
const STUB=Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==','base64');
const B='http://127.0.0.1:8099';
let pass=0, fail=0;
function ok(name,cond,extra){ if(cond){pass++;console.log('  PASS  '+name);} else {fail++;console.log('  FAIL  '+name+(extra?'  ['+extra+']':''));} }
async function ctx(b,w=1280,h=900,mobile=false){
  const c=await b.newContext({viewport:{width:w,height:h},hasTouch:mobile,isMobile:mobile});
  await c.route('**/*',async r=>{const u=r.request().url();
    if(u.startsWith('https://fonts.googleapis.com/'))return r.fulfill({status:200,contentType:'text/css',body:FONT_CSS});
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
   await p.click('#hamburger'); await p.waitForTimeout(350);
   ok('hamburger opens menu', await p.$eval('#mobileMenu',e=>e.classList.contains('open')));
   ok('aria-expanded=true', await p.getAttribute('#hamburger','aria-expanded')==='true');
   ok('body scroll locked', await p.$eval('body',e=>e.style.overflow==='hidden'));
   await p.keyboard.press('Escape'); await p.waitForTimeout(350);
   ok('Escape closes menu', await p.$eval('#mobileMenu',e=>!e.classList.contains('open')));
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

 await b.close();
 if(errs.length){ console.log('\nPAGE ERRORS:'); errs.forEach(e=>console.log('  '+e)); }
 console.log('\n'+pass+' passed, '+fail+' failed, '+errs.length+' page errors');
 process.exit(fail||errs.length?1:0);
})();
