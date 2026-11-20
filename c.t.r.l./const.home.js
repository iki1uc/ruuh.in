const HOME = 40;
let field = Array(81).fill(false);
let depth = Array.from({length:9},()=>Array(81).fill(false));

// CTRL.LER verwaltet die Freigabe für CTRL.
let ctrlApproved = false;

function setApproval(approved, message){
  ctrlApproved = approved;

  ['first3', 'clearField', 'activateDepth'].forEach(id => {
    $('#' + id).disabled = !approved;
  });

  const gate = $('#executionGate');
  gate.innerHTML = `
    <b>CTRL.LER · ${approved ? 'FREIGEGEBEN' : 'GESPERRT'}</b>
    <p class="muted">${message}</p>
  `;
  gate.className = 'metric ' + (approved ? 'good' : 'warn');
}

function checkOrder(){
  const order = $('#auftrag').value.trim();

  if(!order){
    setApproval(false, 'Kein Auftrag vorhanden. CTRL darf nicht ausführen.');
    return;
  }

  setApproval(
    true,
    `Auftrag geprüft: „${order}“. Die sichtbaren Modellaktionen sind für CTRL freigegeben.`
  );
}

function showTab(name){
  $$('.view').forEach(v=>v.hidden=v.id!==name);
  $$('nav button').forEach(b=>
    b.classList.toggle('active',b.dataset.tab===name)
  );
  if(name==='checker') refreshChecks();
}

$$('nav button').forEach(b=>
  b.addEventListener('click',()=>showTab(b.dataset.tab))
);

function renderCells(){
  const root=$('#cells');
  root.innerHTML='';

  field.forEach((on,i)=>{
    const b=document.createElement('button');
    b.className='cell'+(on?' on':'');
    b.title=`Zelle ${i+1}: ${on?'aktiviert':'nicht aktiviert'}`;
    b.setAttribute('aria-label',b.title);
    b.setAttribute('aria-pressed',String(on));
    b.disabled=!ctrlApproved;

    b.addEventListener('click',()=>{
      if(!ctrlApproved) return;
      field[i]=!field[i];
      renderCells();
    });

    root.appendChild(b);
  });

  const n=field.filter(Boolean).length;
  $('#fieldCount').textContent=`${n}/81 Zellen aktiviert`;
  $('#fieldBar').style.width=(n/81*100)+'%';
}

function updateDepth(){
  const n=depth.flat().filter(Boolean).length;
  $('#depthCount').textContent=`${n}/729 Zellen aktiviert`;
  $('#depthBar').style.width=(n/729*100)+'%';
}

function updateFigure(){
  const n=$$('.element').filter(x=>x.checked).length;
  const b=n/3;
  const l=1-b;

  $('#figureStatus').textContent =
    b===1
      ? 'MODELLSTATUS: VOLLSTÄNDIG — Alle drei Modellbedingungen erfüllt'
      : `MODELLSTATUS: OFFEN — B=${b.toFixed(2)}, L=${l.toFixed(2)}`;

  $('#figureStatus').className=b===1?'good':'warn';
}

function bounded(){
  const x=Number($('#rawValue').value);

  if(!Number.isFinite(x)){
    $('#boundedResult').textContent=
      'Bitte einen gültigen Zahlenwert eingeben.';
    return;
  }

  $('#boundedResult').textContent=
    `Ausgabewert: ${Math.min(x,HOME)} · Ursprungswert: ${x}`;
}

function checksData(){
  const active=field.filter(Boolean).length;
  const d=depth.flat().filter(Boolean).length;
  const elems=$$('.element').filter(x=>x.checked).length;

  return [
    ['Freigabe CTRL', ctrlApproved ? 'freigegeben' : 'gesperrt',
      'CTRL.LER entscheidet vor der Ausführung'],
    ['Feldgröße', '81 Zellen angelegt', '81'],
    ['Feldstatus', `${active}/81 aktiviert`, `${active} von 81`],
    ['Figur', `${elems}/3 Elemente aktiviert',
      '3 von 3 für VOLLSTÄNDIG'],
    ['Tiefe', `${depth.length} Layer · ${d}/729 aktiviert`,
      '9 Layer à 81 Zellen'],
    ['Wertbegrenzung', 'f(x) = min(x, 40)', 'HOME = 40']
  ];
}

function refreshChecks(){
  $('#checks').innerHTML=checksData()
    .map(([a,b,c])=>`
      <div class="metric">
        <small>${a}</small>
        <strong style="font-size:18px">${b}</strong>
        <small>${c}</small>
      </div>
    `).join('');
}

function statusReport(){
  const x=Number($('#rawValue').value);

  return [
    `AUFTRAG: ${$('#auftrag').value || '(kein Auftragstext)'}`,
    `CTRL.LER-FREIGABE: ${ctrlApproved ? 'freigegeben' : 'gesperrt'}`,
    `FELD: ${field.filter(Boolean).length}/81 Zellen aktiviert`,
    `FIGUR: ${$$('.element').filter(x=>x.checked).length}/3 Elemente aktiviert`,
    `TIEFE: ${depth.flat().filter(Boolean).length}/729 Zellen aktiviert`,
    `WERT: Ursprungswert ${x}; Ausgabe ${
      Number.isFinite(x) ? Math.min(x,HOME) : 'ungültig'
    }`,
    `PRÜFSTATUS: Werte erfasst; externe Bedeutung nicht bewertet.`
  ].join('\\n');
}

$('#checkOrder').addEventListener('click',checkOrder);

$('#auftrag').addEventListener('input',()=>{
  // Eine Änderung am Auftrag hebt die frühere Freigabe auf.
  setApproval(false,'Der Auftrag wurde geändert und muss erneut geprüft werden.');
});

$('#first3').addEventListener('click',()=>{
  if(!ctrlApproved) return;
  for(let i=0;i<3;i++) field[i]=true;
  renderCells();
});

$('#clearField').addEventListener('click',()=>{
  if(!ctrlApproved) return;
  field.fill(false);
  renderCells();
});

$('#activateDepth').addEventListener('click',()=>{
  if(!ctrlApproved) return;
  for(let i=0;i<3;i++) depth[0][i]=true;
  updateDepth();
});

$$('.element').forEach(x=>
  x.addEventListener('change',updateFigure)
);

$('#rawValue').addEventListener('input',bounded);
$('#refreshChecks').addEventListener('click',refreshChecks);
$('#runSummary').addEventListener('click',()=>{
  $('#executionLog').textContent=statusReport();
});
$('#makeReport').addEventListener('click',()=>{
  $('#report').textContent=statusReport();
  $('#feedbackStatus').textContent='Rückmeldung: Statusbericht erstellt';
  $('#feedbackStatus').className='good';
});

renderCells();
updateDepth();
updateFigure();
bounded();
refreshChecks();
setApproval(false,'Noch keine Prüfung durchgeführt. CTRL ist gesperrt.');
