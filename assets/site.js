
(function(){
  const mobileNav = document.querySelector('.topnav__mobile');
  if (mobileNav) {
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && mobileNav.open) {
        mobileNav.open = false;
        mobileNav.querySelector('summary').focus();
      }
    });
    document.addEventListener('click', e => {
      if (!mobileNav.contains(e.target) || e.target.closest('a')) mobileNav.open = false;
    });
    window.matchMedia('(min-width:1200px)').addEventListener('change', e => {
      if (e.matches) mobileNav.open = false;
    });
  }
  document.querySelectorAll('.navdrop').forEach(dd => {
    const btn = dd.querySelector('.navdrop__btn');
    const close = () => { dd.classList.remove('is-open'); btn.setAttribute('aria-expanded', 'false'); };
    btn.addEventListener('click', e => { e.stopPropagation(); const open = !dd.classList.contains('is-open'); dd.classList.toggle('is-open', open); btn.setAttribute('aria-expanded', String(open)); });
    document.addEventListener('click', e => { if (!dd.contains(e.target)) close(); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape' && dd.classList.contains('is-open')) { close(); btn.focus(); } });
  });
  const css = getComputedStyle(document.documentElement);
  const T = n => css.getPropertyValue(n).trim();
  const C = { accent:T('--oe-accent'), accentSoft:T('--oe-bluette-200'), deep:T('--oe-bg-dark'), mid:T('--oe-bluette-400'),
    gray:T('--oe-gray-400'), gray2:T('--oe-gray-300'), ink:T('--oe-gray-800'), soft:T('--oe-gray-700'), grid:T('--oe-gray-200'),
    white:T('--oe-white'), pop:T('--oe-pop'), up:T('--oe-lime-700'), down:T('--oe-magenta-700') };
  const fmt = (v,d=0) => new Intl.NumberFormat('it-IT',{minimumFractionDigits:d,maximumFractionDigits:d,useGrouping:'always'}).format(v);

  /* ---------- data ---------- */
  const MUNI = [["Rieti",42.4056,12.8506,45083,-1.8,9,94],["Fara in Sabina",42.1864,12.6969,13885,1.1,63,78],["Cittaducale",42.3871,12.967,6397,-1.6,11,96],["Poggio Mirteto",42.2634,12.6706,6065,-1.4,41,80],["Montopoli di Sabina",42.2254,12.667,4098,0.4,44,77],["Borgorose",42.1921,13.2623,4213,-1.1,19,91],["Contigliano",42.4184,12.7617,3670,-2.7,12,95],["Magliano Sabina",42.3592,12.4878,3452,-2.1,17,80],["Scandriglia",42.1564,12.8589,3278,4.5,53,81],["Forano",42.2838,12.6055,3268,8.1,49,74],["Poggio Moiano",42.197,12.8834,2811,1.7,37,82],["Poggio Nativo",42.2131,12.7873,2557,1.8,42,79],["Cantalice",42.4797,12.9244,2414,-2.7,10,103],["Antrodoco",42.3991,13.1245,2258,-4.8,7,105],["Stimigliano",42.296,12.5623,2211,0.0,46,72],["Amatrice",42.6262,13.2925,2181,-6.0,10,133],["Leonessa",42.5681,13.0003,2051,-4.2,12,129],["Poggio Bustone",42.504,12.8894,1971,-0.8,8,107],["Cantalupo in Sabina",42.3027,12.6412,1657,1.4,39,79],["Pescorocchiano",42.2143,13.1421,1806,-6.2,20,98],["Collevecchio",42.3248,12.5316,1611,6.9,30,82],["Greccio",42.45,12.7547,1459,-2.2,11,98],["Tarano",42.3384,12.5839,1375,-0.5,37,82],["Torricella in Sabina",42.2738,12.8701,1290,-5.4,38,85],["Torri in Sabina",42.3608,12.6279,1216,1.7,28,82],["Monteleone Sabino",42.2249,12.8686,1124,-5.1,36,82],["Poggio Catino",42.2928,12.685,1307,5.4,43,83],["Casperia",42.3455,12.6845,1197,-1.1,33,83],["Rivodutri",42.5216,12.8669,1123,-1.3,7,107],["Castel Sant'Angelo",42.3982,13.0183,1182,-2.2,12,100],["Toffia",42.2058,12.7595,1070,1.2,45,80],["Fiamignano",42.2997,13.1574,1162,-4.4,19,101],["Selci",42.3134,12.6188,1135,5.0,39,79],["Borgo Velino",42.4031,13.0549,903,-3.3,9,104],["Petrella Salto",42.3081,13.063,1026,-2.8,15,105],["Castelnuovo di Farfa",42.2332,12.7314,983,-1.1,45,79],["Montebuono",42.3739,12.5753,837,-4.0,28,83],["Frasso Sabino",42.2229,12.8145,734,1.0,37,79],["Rocca Sinibalda",42.2616,12.9464,801,2.3,29,94],["Belmonte in Sabina",42.3248,12.8809,633,-0.6,23,92],["Monte San Giovanni in Sabina",42.3154,12.7743,664,2.5,17,99],["Casaprota",42.2482,12.808,675,-3.4,42,84],["Configni",42.4321,12.6369,567,-2.7,9,93],["Posta",42.5171,13.0811,535,-9.2,12,116],["Poggio San Lorenzo",42.2507,12.8448,553,5.9,32,81],["Borbona",42.4934,13.1349,577,-2.0,11,120],["Accumoli",42.6953,13.2441,503,-9.4,3,138],["Salisano",42.2759,12.7433,474,-7.8,46,87],["Roccantica",42.3214,12.7008,526,-4.7,33,83],["Cottanello",42.4209,12.6976,529,-0.4,15,93],["Mompeo",42.2586,12.7711,519,5.1,30,93],["Colli sul Velino",42.4984,12.7796,461,-0.9,9,104],["Collalto Sabino",42.155,13.0519,383,-3.0,38,92],["Longone Sabino",42.3035,12.9496,513,-7.2,23,105],["Orvinio",42.1274,12.9375,387,-0.8,44,91],["Labro",42.5198,12.798,346,-7.7,5,108],["Cittareale",42.6026,13.148,374,-9.9,14,126],["Montasola",42.3785,12.685,396,3.7,34,92],["Morro Reatino",42.5282,12.8401,335,-2.6,12,110],["Colle di Tora",42.1992,12.9354,349,-2.8,24,98],["Concerviano",42.3066,12.9692,280,-0.7,21,104],["Montenero Sabino",42.2872,12.8123,265,-4.7,31,89],["Castel di Tora",42.2091,12.9695,273,2.2,22,96],["Pozzaglia Sabina",42.1572,12.9668,305,-3.2,48,93],["Turania",42.132,13.0089,238,4.4,48,88],["Vacone",42.3912,12.6414,223,-1.3,22,92],["Ascrea",42.2219,12.9725,203,-4.7,31,96],["Nespolo",42.1552,13.0718,205,7.3,32,92],["Varco Sabino",42.2423,13.0294,151,-14.7,32,114],["Paganico Sabino",42.181,13.0047,161,3.9,36,92],["Collegiove",42.1728,13.0306,129,-4.4,64,97],["Micigliano",42.4533,13.0483,120,5.3,30,117],["Marcetelli",42.2164,13.0432,53,-30.3,26,117]]; // [nome, lat, lon, residenti 2025, variazione % 2021-25, % lavoratori verso prov. Roma, minuti auto da Roma]
  const D = {
    bands:{labels:['Entro 55 km','55–85 km','Oltre 85 km'],vals:[1.10,-2.07,-5.68],extra:[['Comuni',[27,39,7]],['Residenti',[57585,85840,6341]],['Anziani ogni 100 giovani',[234,283,445]]]},
    emp:{labels:['2022','2023','2024','2025'],series:[['Rieti',[58.4,61.8,62.7,60.8]],['Lazio',[61.8,63.2,64.0,64.2]],['Italia',[60.1,61.5,62.2,62.5]]]},
    commute:{labels:['Entro 55 km','55–85 km','Oltre 85 km'],series:[['Nel proprio comune',[26.7,54.5,61.3]],['Nel comune di Rieti',[5.2,13.8,11.1]],['In altri comuni reatini',[18.6,13.7,11.0]],['In provincia di Roma',[45.5,12.1,10.8]],['In altre province',[4.0,5.9,5.6]]]},
    va:{labels:['Rieti','Viterbo','Frosinone','Terni',"L'Aquila",'Italia','Lazio'],vals:[24245,24285,24815,25539,29056,33348,39120]},
    exp:{labels:['2024','2025'],series:[['Farmaceutica',[405.8,703.6]],['Altri beni',[185.9,174.8]]]},
    energy:{labels:['Idroelettrico','Fotovoltaico','Bioenergie','Non rinnovabile'],vals:[220.7,49.2,20.6,7.4]},
    pv:{labels:['Rieti','Frosinone','Terni','Viterbo'],vals:[0.35,0.61,0.81,5.14]},
    grad:{labels:['Rieti','Frosinone','Terni',"L'Aquila",'Viterbo','Italia','Lazio'],vals:[-32.8,-29.6,-23.5,-18.1,-12.9,-6.2,5.0]},
    // Grouped by the local sector each profile serves: 0 pharma-chemical, 1 mechanics / Pump Valley, 2 other.
    profiles:{labels:['Specialisti in scienze chimiche, fisiche e naturali','Laureati in chimica e farmaceutica','Tecnici dei processi produttivi','Operai della meccanica di precisione','Meccanici, montatori e manutentori','Diplomati in meccanica, meccatronica ed energia','Diplomati in elettronica ed elettrotecnica','Tecnici della salute','Ingegneri','Tecnici in campo ingegneristico'],
      vals:[98.2,84.2,65.2,84.7,75.6,68.3,64.2,63.4,52.6,34.0],hires:[110,60,70,60,190,220,120,210,80,100],group:[0,0,0,1,1,1,1,2,2,2],
      groups:['Farmaceutica e chimica','Meccanica e Pump Valley','Altri profili']},
    conc:{labels:['2021','2022','2023','2024','2025'],pharma:[387.3,385.3,358.2,405.8,703.6],other:[146.3,171.6,183.9,185.9,174.8],share:[72.6,69.2,66.1,68.6,80.1]},
    share:{labels:['Rieti, 2025','Lazio, 2024','Italia, 2024'],vals:[80.1,48,9.1]}
  };

  /* ---------- data tables (accessible view of every chart) ---------- */
  function table(head, rows){ return '<table class="oe-table"><thead><tr>'+head.map((h,i)=>'<th'+(i?' class="num"':'')+'>'+h+'</th>').join('')+'</tr></thead><tbody>'+rows.map(r=>'<tr>'+r.map((c,i)=>'<td'+(i?' class="num"':'')+'>'+c+'</td>').join('')+'</tr>').join('')+'</tbody></table>'; }
  const TB = {
    bands: table(['Fascia','Variazione %'].concat(D.bands.extra.map(e=>e[0])), D.bands.labels.map((l,i)=>[l, fmt(D.bands.vals[i],1)+'%'].concat(D.bands.extra.map(e=>fmt(e[1][i]))))),
    emp: table(['Anno'].concat(D.emp.series.map(s=>s[0])), D.emp.labels.map((l,i)=>[l].concat(D.emp.series.map(s=>fmt(s[1][i],1)+'%')))),
    commute: table(['Destinazione'].concat(D.commute.labels), D.commute.series.map(s=>[s[0]].concat(s[1].map(v=>fmt(v,1)+'%')))),
    va: table(['Territorio','Euro per abitante'], D.va.labels.map((l,i)=>[l, fmt(D.va.vals[i])])),
    exp: table(['Anno'].concat(D.exp.series.map(s=>s[0]),['Totale']), D.exp.labels.map((l,i)=>[l].concat(D.exp.series.map(s=>fmt(s[1][i],1)),[fmt(D.exp.series[0][1][i]+D.exp.series[1][1][i],1)]))),
    energy: table(['Fonte','GWh'], D.energy.labels.map((l,i)=>[l, fmt(D.energy.vals[i],1)])),
    pv: table(['Provincia','kW per abitante'], D.pv.labels.map((l,i)=>[l, fmt(D.pv.vals[i],2)])),
    grad: table(['Territorio','Per mille laureati'], D.grad.labels.map((l,i)=>[l, fmt(D.grad.vals[i],1)])),
    profiles: table(['Profilo','Comparto','Entrate previste','Difficile reperimento'], D.profiles.labels.map((l,i)=>[l, D.profiles.groups[D.profiles.group[i]], fmt(D.profiles.hires[i]), fmt(D.profiles.vals[i],1)+'%'])),
    conc: table(['Anno','Farmaceutica, mln €','Altri beni, mln €','Quota farmaceutica'], D.conc.labels.map((l,i)=>[l, fmt(D.conc.pharma[i],1), fmt(D.conc.other[i],1), fmt(D.conc.share[i],1)+'%'])),
    share: table(['Territorio','Quota della farmaceutica sull\'export'], D.share.labels.map((l,i)=>[l, fmt(D.share.vals[i],1)+'%']))
  };
  document.querySelectorAll('[data-table]').forEach(el=>{ el.innerHTML = TB[el.getAttribute('data-table')] || ''; });

  /* ---------- maps ---------- */
  const tip = document.getElementById('tip');
  function showTip(e, html){ tip.innerHTML = html; tip.hidden = false; const x = Math.min(e.clientX + 14, window.innerWidth - 280); tip.style.left = x + 'px'; tip.style.top = (e.clientY + 14) + 'px'; }
  function hideTip(){ tip.hidden = true; }
  const lat0 = 42.41, k = Math.cos(lat0*Math.PI/180);
  const lons = MUNI.map(m=>m[2]), lats = MUNI.map(m=>m[1]);
  const minX = Math.min(...lons)*k, maxX = Math.max(...lons)*k, minY = Math.min(...lats), maxY = Math.max(...lats);
  function project(W,H,pad){ const s = Math.min((W-2*pad)/(maxX-minX),(H-2*pad)/(maxY-minY)); const ox = (W-(maxX-minX)*s)/2, oy = (H-(maxY-minY)*s)/2; return m => [ox+(m[2]*k-minX)*s, oy+(maxY-m[1])*s]; }
  const rOf = (pop,f) => Math.max(3, Math.sqrt(pop)/f);
  const NS = 'http://www.w3.org/2000/svg';
  function circle(svg, cx, cy, r, fill, stroke, sw){ const c = document.createElementNS(NS,'circle'); c.setAttribute('cx',cx.toFixed(1)); c.setAttribute('cy',cy.toFixed(1)); c.setAttribute('r',r.toFixed(1)); c.setAttribute('fill',fill); c.setAttribute('stroke',stroke); c.setAttribute('stroke-width',sw); svg.appendChild(c); return c; }
  const order = MUNI.map((m,i)=>i).sort((a,b)=>MUNI[b][3]-MUNI[a][3]); // big first, small on top

  // hero map (decorative)
  (function(){ const svg = document.getElementById('heroMap'); if (!svg) return; const P = project(520,440,30);
    order.forEach(i=>{ const m = MUNI[i], p = P(m); const cap = m[0]==='Rieti'; circle(svg,p[0],p[1],rOf(m[3],7.5), cap?C.pop:'rgba(255,255,255,.82)', cap?C.pop:'rgba(255,255,255,.35)', 1); }); })();

  function mapInto(id, legId, colorOf, legend, tipHtml){
    const svg = document.getElementById(id); if (!svg) return; const P = project(560,470,24);
    order.forEach(i=>{ const m = MUNI[i], p = P(m); const c = circle(svg,p[0],p[1],rOf(m[3],6.2), colorOf(m), C.white, 1.5);
      c.style.cursor='pointer'; c.setAttribute('tabindex','0'); c.setAttribute('aria-label', m[0]);
      c.addEventListener('mousemove', e=>showTip(e, tipHtml(m))); c.addEventListener('mouseleave', hideTip);
      c.addEventListener('focus', ()=>{ const b = c.getBoundingClientRect(); showTip({clientX:b.right, clientY:b.top}, tipHtml(m)); }); c.addEventListener('blur', hideTip);
      if (m[3] > 9000){ const t = document.createElementNS(NS,'text'); t.setAttribute('x',(p[0]+rOf(m[3],6.2)+5).toFixed(1)); t.setAttribute('y',(p[1]+5).toFixed(1)); t.setAttribute('fill',C.ink); t.setAttribute('font-size','14'); t.setAttribute('font-family',T('--oe-font-sans')); t.setAttribute('font-weight','600'); t.setAttribute('stroke',C.white); t.setAttribute('stroke-width','4'); t.setAttribute('paint-order','stroke'); t.setAttribute('stroke-linejoin','round'); t.textContent = m[0]; t.style.pointerEvents='none'; svg.appendChild(t); }
    });
    document.getElementById(legId).innerHTML = legend;
  }
  // Map 1: diverging (decline magenta · stable gray · growth lime-dark)
  function popColor(v){ if (v <= -5) return C.down; if (v < -1) return T('--oe-magenta-400'); if (v <= 1) return C.gray2; if (v < 4) return T('--oe-lime-500'); return C.up; }
  const legRow = (col,lab) => '<div class="legend__row"><span class="legend__sw" style="background:'+col+'"></span>'+lab+'</div>';
  mapInto('mapPop','legPop', m=>popColor(m[4]),
    '<div class="legend__t">Variazione residenti</div>'+legRow(C.up,'+4% e oltre')+legRow(T('--oe-lime-500'),'da +1% a +4%')+legRow(C.gray2,'stabile, ±1%')+legRow(T('--oe-magenta-400'),'da −1% a −5%')+legRow(C.down,'−5% e oltre'),
    m=>'<b>'+m[0]+'</b><br>'+fmt(m[3])+' residenti<br>Variazione 2021–2025: '+(m[4]>0?'+':'')+fmt(m[4],1)+'%');
  // Map 2: sequential bluette
  const ramp = [T('--oe-bluette-050'),T('--oe-bluette-200'),T('--oe-bluette-400'),T('--oe-bluette-600'),T('--oe-bluette-900')];
  function romeColor(v){ return v < 10 ? ramp[0] : v < 20 ? ramp[1] : v < 30 ? ramp[2] : v < 45 ? ramp[3] : ramp[4]; }
  mapInto('mapRome','legRome', m=>romeColor(m[5]),
    '<div class="legend__t">Lavoratori verso la provincia di Roma</div>'+legRow(ramp[4],'45% e oltre')+legRow(ramp[3],'30–45%')+legRow(ramp[2],'20–30%')+legRow(ramp[1],'10–20%')+legRow(ramp[0],'meno del 10%'),
    m=>'<b>'+m[0]+'</b><br>'+fmt(m[5])+'% dei lavoratori verso la provincia di Roma<br>'+fmt(m[6])+' minuti d\'auto dal centro di Roma');

  /* ---------- charts ---------- */
  const mk = (id, cfg) => { const el = document.getElementById(id); if (el) new Chart(el, cfg); };
  if (typeof Chart !== 'undefined') (function(){
  if (window.ChartDataLabels) Chart.register(ChartDataLabels);
  Chart.defaults.font.family = T('--oe-font-mono'); Chart.defaults.font.size = 13; Chart.defaults.color = C.soft; Chart.defaults.borderColor = C.grid;
  Chart.defaults.plugins.legend.labels.boxWidth = 12; Chart.defaults.plugins.legend.labels.boxHeight = 12;
  Chart.defaults.elements.bar.borderRadius = 0; Chart.defaults.maintainAspectRatio = false;
  Chart.defaults.plugins.tooltip.backgroundColor = C.deep; Chart.defaults.plugins.tooltip.titleFont = {family:T('--oe-font-sans'),weight:'600',size:14}; Chart.defaults.plugins.tooltip.bodyFont = {family:T('--oe-font-sans'),size:14}; Chart.defaults.plugins.tooltip.padding = 10; Chart.defaults.plugins.tooltip.cornerRadius = 0;
  Chart.defaults.plugins.datalabels = Object.assign(Chart.defaults.plugins.datalabels||{}, {display:false});
  const labelFont = {family:T('--oe-font-sans'), weight:'600', size:14};
  const hl = (labels, name) => labels.map(l => l===name ? C.accent : C.gray2);

  mk('chBands',{type:'bar',data:{labels:D.bands.labels,datasets:[{data:D.bands.vals,backgroundColor:D.bands.vals.map(v=>v>=0?C.accent:C.accentSoft),borderColor:C.white,borderWidth:{top:0,bottom:0,left:0,right:2},barThickness:34}]},
    options:{indexAxis:'y',layout:{padding:{right:70,left:4}},plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>' '+(c.raw>0?'+':'')+fmt(c.raw,1)+'%'}},datalabels:{display:true,anchor:c=>c.dataset.data[c.dataIndex]>=0?'end':'start',align:c=>c.dataset.data[c.dataIndex]>=0?'end':'start',color:C.ink,font:labelFont,formatter:v=>(v>0?'+':'')+fmt(v,1)+'%'}},
      scales:{x:{suggestedMin:-7,suggestedMax:2,grid:{color:c=>c.tick.value===0?C.ink:C.grid},ticks:{callback:v=>fmt(v)+'%'}},y:{grid:{display:false},ticks:{font:{family:T('--oe-font-sans'),size:15},color:C.ink}}}}});

  const empColors = [C.accent, C.gray, C.soft];
  mk('chEmp',{type:'line',data:{labels:D.emp.labels,datasets:D.emp.series.map((s,i)=>({label:s[0],data:s[1],borderColor:empColors[i],backgroundColor:empColors[i],borderWidth:i?2:3,borderDash:i===2?[6,4]:[],pointRadius:i?3:5,pointHoverRadius:7,pointBorderColor:C.white,pointBorderWidth:2,tension:0}))},
    options:{interaction:{mode:'index',intersect:false},layout:{padding:{right:104,top:10}},plugins:{legend:{position:'top',align:'start'},tooltip:{callbacks:{label:c=>' '+c.dataset.label+': '+fmt(c.raw,1)+'%'}},
      datalabels:{display:c=>c.dataIndex===c.dataset.data.length-1,align:'right',anchor:'end',offset:6,color:C.ink,font:{family:T('--oe-font-sans'),weight:'600',size:13},formatter:(v,c)=>c.dataset.label+' '+fmt(v,1)}},
      scales:{y:{suggestedMin:56,suggestedMax:66,ticks:{callback:v=>fmt(v)+'%'},grid:{color:C.grid}},x:{grid:{display:false}}}}});

  const commCols = [T('--oe-bluette-900'),T('--oe-bluette-600'),T('--oe-bluette-300'),T('--oe-lime-500'),C.gray2];
  mk('chCommute',{type:'bar',data:{labels:D.commute.labels,datasets:D.commute.series.map((s,i)=>({label:s[0],data:s[1],backgroundColor:commCols[i],borderColor:C.white,borderWidth:{right:2,left:0,top:0,bottom:0},barThickness:38}))},
    options:{indexAxis:'y',plugins:{legend:{position:'top',align:'start'},tooltip:{callbacks:{label:c=>' '+c.dataset.label+': '+fmt(c.raw,1)+'%'}},
      datalabels:{display:c=>c.dataset.data[c.dataIndex]>=9,color:c=>c.datasetIndex<2?C.white:C.ink,font:{family:T('--oe-font-sans'),weight:'600',size:13},formatter:v=>fmt(v)+'%'}},
      scales:{x:{stacked:true,max:100,ticks:{callback:v=>fmt(v)+'%'},grid:{color:C.grid}},y:{stacked:true,grid:{display:false},ticks:{font:{family:T('--oe-font-sans'),size:15},color:C.ink}}}}});

  mk('chVa',{type:'bar',data:{labels:D.va.labels,datasets:[{data:D.va.vals,backgroundColor:hl(D.va.labels,'Rieti'),barThickness:26}]},
    options:{indexAxis:'y',layout:{padding:{right:74}},plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>' '+fmt(c.raw)+' €'}},datalabels:{display:true,anchor:'end',align:'end',color:C.ink,font:labelFont,formatter:v=>fmt(v)+' €'}},
      scales:{x:{beginAtZero:true,ticks:{callback:v=>fmt(v/1000)+' mila'},grid:{color:C.grid}},y:{grid:{display:false},ticks:{font:{family:T('--oe-font-sans'),size:15},color:C.ink}}}}});

  mk('chExp',{type:'bar',data:{labels:D.exp.labels,datasets:D.exp.series.map((s,i)=>({label:s[0],data:s[1],backgroundColor:i?C.accentSoft:C.accent,borderColor:C.white,borderWidth:{top:2,bottom:0,left:0,right:0},barThickness:70}))},
    options:{plugins:{legend:{position:'top',align:'start'},tooltip:{callbacks:{label:c=>' '+c.dataset.label+': '+fmt(c.raw,1)+' mln €'}},
      datalabels:{display:true,color:c=>c.datasetIndex?C.ink:C.white,font:labelFont,formatter:v=>fmt(v)}},
      scales:{y:{stacked:true,beginAtZero:true,ticks:{callback:v=>fmt(v)},grid:{color:C.grid},title:{display:true,text:'milioni di euro'}},x:{stacked:true,grid:{display:false},ticks:{font:{family:T('--oe-font-sans'),size:15},color:C.ink}}}}});

  mk('chEnergy',{type:'bar',data:{labels:D.energy.labels,datasets:[{data:D.energy.vals,backgroundColor:[C.accent,C.accent,C.accent,C.gray2],barThickness:26}]},
    options:{indexAxis:'y',layout:{padding:{right:60}},plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>' '+fmt(c.raw,1)+' GWh'}},datalabels:{display:true,anchor:'end',align:'end',color:C.ink,font:labelFont,formatter:v=>fmt(v,1)}},
      scales:{x:{beginAtZero:true,grid:{color:C.grid},ticks:{callback:v=>fmt(v)}},y:{grid:{display:false},ticks:{font:{family:T('--oe-font-sans'),size:15},color:C.ink}}}}});

  mk('chPv',{type:'bar',data:{labels:D.pv.labels,datasets:[{data:D.pv.vals,backgroundColor:hl(D.pv.labels,'Rieti'),barThickness:26}]},
    options:{indexAxis:'y',layout:{padding:{right:50}},plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>' '+fmt(c.raw,2)+' kW per abitante'}},datalabels:{display:true,anchor:'end',align:'end',color:C.ink,font:labelFont,formatter:v=>fmt(v,2)}},
      scales:{x:{beginAtZero:true,grid:{color:C.grid},ticks:{callback:v=>fmt(v,1)}},y:{grid:{display:false},ticks:{font:{family:T('--oe-font-sans'),size:15},color:C.ink}}}}});

  mk('chGrad',{type:'bar',data:{labels:D.grad.labels,datasets:[{data:D.grad.vals,backgroundColor:hl(D.grad.labels,'Rieti'),barThickness:30}]},
    options:{layout:{padding:{top:28,bottom:4}},plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>' '+fmt(c.raw,1)+' per mille laureati'}},
      datalabels:{display:true,anchor:c=>c.dataset.data[c.dataIndex]<0?'start':'end',align:c=>c.dataset.data[c.dataIndex]<0?'bottom':'top',color:C.ink,font:labelFont,formatter:v=>(v>0?'+':'')+fmt(v,1)}},
      scales:{y:{suggestedMin:-40,suggestedMax:10,grid:{color:c=>c.tick.value===0?C.ink:C.grid},ticks:{callback:v=>fmt(v)}},x:{grid:{display:false},ticks:{font:{family:T('--oe-font-sans'),size:15},color:C.ink}}}}});

  // Export by year: pharmaceutical vs other goods; the label above each bar is the pharmaceutical share.
  mk('chConc',{type:'bar',data:{labels:D.conc.labels,datasets:[
      {label:'Farmaceutica',data:D.conc.pharma,backgroundColor:C.accent,borderColor:C.white,borderWidth:{top:2,bottom:0,left:0,right:0},barThickness:56},
      {label:'Altri beni',data:D.conc.other,backgroundColor:C.accentSoft,borderColor:C.white,borderWidth:{top:2,bottom:0,left:0,right:0},barThickness:56}]},
    options:{layout:{padding:{top:30}},plugins:{legend:{position:'top',align:'start'},tooltip:{callbacks:{label:c=>' '+c.dataset.label+': '+fmt(c.raw,1)+' mln €',footer:items=>'Quota farmaceutica: '+fmt(D.conc.share[items[0].dataIndex],1)+'%'}},
      datalabels:{display:true,
        anchor:c=>c.datasetIndex?'end':'center',align:c=>c.datasetIndex?'top':'center',
        color:c=>c.datasetIndex?C.ink:C.white,font:labelFont,
        formatter:(v,c)=>c.datasetIndex?fmt(D.conc.share[c.dataIndex])+'% farmaceutica':fmt(v)}},
      scales:{y:{stacked:true,beginAtZero:true,ticks:{callback:v=>fmt(v)},grid:{color:C.grid},title:{display:true,text:'milioni di euro'}},x:{stacked:true,grid:{display:false},ticks:{font:{family:T('--oe-font-sans'),size:15},color:C.ink}}}}});

  mk('chShare',{type:'bar',data:{labels:D.share.labels,datasets:[{data:D.share.vals,backgroundColor:D.share.labels.map(l=>l.startsWith('Rieti')?C.accent:C.gray2),barThickness:28}]},
    options:{indexAxis:'y',layout:{padding:{right:70}},plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>' '+fmt(c.raw,1)+'% dell\'export'}},
      datalabels:{display:true,anchor:'end',align:'end',color:C.ink,font:labelFont,formatter:v=>fmt(v,1)+'%'}},
      scales:{x:{min:0,max:100,ticks:{callback:v=>fmt(v)+'%'},grid:{color:C.grid}},y:{grid:{display:false},ticks:{font:{family:T('--oe-font-sans'),size:15},color:C.ink}}}}});

  const wrap = (txt, n) => txt.split(' ').reduce((lines, w) => { const l = lines[lines.length - 1]; if ((l + ' ' + w).trim().length > n) lines.push(w); else lines[lines.length - 1] = (l + ' ' + w).trim(); return lines; }, ['']);
  const profCols = [C.accent, T('--oe-magenta-700'), C.gray2];
  mk('chProfiles',{type:'bar',data:{labels:D.profiles.labels,datasets:D.profiles.groups.map((g,gi)=>({label:g,grouped:false,barThickness:22,backgroundColor:profCols[gi],
      data:D.profiles.vals.map((v,i)=>D.profiles.group[i]===gi?v:null)}))},
    options:{indexAxis:'y',layout:{padding:{right:150}},plugins:{legend:{position:'top',align:'start'},
      tooltip:{callbacks:{title:items=>wrap(items[0].label,32),label:c=>' '+fmt(c.raw,1)+'% difficile · '+fmt(D.profiles.hires[c.dataIndex])+' entrate previste'}},
      datalabels:{display:c=>c.dataset.data[c.dataIndex]!=null,anchor:'end',align:'end',color:C.ink,font:{family:T('--oe-font-sans'),weight:'600',size:13},formatter:(v,c)=>fmt(v)+'% · '+fmt(D.profiles.hires[c.dataIndex])+' entrate'}},
      scales:{x:{min:0,max:100,ticks:{callback:v=>fmt(v)+'%'},grid:{color:C.grid}},y:{grid:{display:false},ticks:{font:{family:T('--oe-font-sans'),size:14},color:C.ink,autoSkip:false,callback:function(v){const l=this.getLabelForValue(v);return l.length>34?wrap(l,34):l;}}}}}});

  })();

  /* ---------- second-level nav: built from section[data-label]; only the bar scrolls sideways ---------- */
  const sub = document.getElementById('subnav');
  const secs = [...document.querySelectorAll('section[id][data-label]')];
  if (sub && secs.length){
    const bar = document.createElement('div'); bar.className = 'subnav__in';
    secs.forEach(s=>{ const a = document.createElement('a'); a.href = '#'+s.id; a.textContent = s.dataset.label; a.dataset.for = s.id; bar.appendChild(a); });
    sub.appendChild(bar); sub.hidden = false; document.documentElement.classList.add('has-sub');
    const links = [...bar.querySelectorAll('a')]; let current = null;
    const activate = id => { const a = links.find(l=>l.dataset.for===id); if (!a || a===current) return; if (current) current.classList.remove('is-active'); a.classList.add('is-active'); current = a;
      const left = a.offsetLeft - bar.offsetLeft, right = left + a.offsetWidth; if (left < bar.scrollLeft || right > bar.scrollLeft + bar.clientWidth) bar.scrollLeft = Math.max(0, left - 16); };
    const io = new IntersectionObserver(es=>es.forEach(e=>{ if (e.isIntersecting) activate(e.target.id); }),{rootMargin:'-40% 0px -55% 0px'});
    secs.forEach(s=>io.observe(s));
  }
})();
