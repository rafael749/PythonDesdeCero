const get = (id) => document.getElementById(id);
const storageKey = 'python-desde-cero-v1';
let lessons = [];
let current = 0;
let activeFile = 'solucion.py';
let revealed = 0;
let worker = null;
let deadline = null;
let busy = false;
let savedState = { drafts: {}, completed: {}, selected: 1 };
let storageAvailable = true;

function node(tag, className, text) {
  const item = document.createElement(tag);
  if (className) item.className = className;
  if (text !== undefined) item.textContent = text;
  return item;
}
function icons() { window.lucide?.createIcons(); }
function notice(text) { get('notice').textContent = text; get('notice').hidden = !text; }
function lesson() { return lessons[current]; }
function draft() { return savedState.drafts[lesson().id]; }
function fingerprint() { return JSON.stringify(draft().files); }
function completed(item) {
  return typeof savedState.completed[item.id] === 'string' &&
    savedState.completed[item.id] === JSON.stringify(savedState.drafts[item.id]?.files);
}
function persist() {
  try {
    localStorage.setItem(storageKey, JSON.stringify(savedState));
    get('saved').textContent = 'Guardado en este navegador';
  } catch {
    storageAvailable = false;
    get('saved').textContent = 'Sin guardar';
    notice('El navegador no permite guardar el progreso. No cierres esta pagina sin conservar tu codigo.');
  }
}
function saveEditor() {
  if (!lesson()) return;
  draft().files[activeFile] = get('editor').value;
  draft().inputs = get('stdin').value;
  persist();
  updateProgress();
}
function updateProgress() {
  const count = lessons.filter(completed).length;
  get('progress').value = count;
  get('progress').max = lessons.length;
  get('progress-label').textContent = `${count} / ${lessons.length} completados`;
  get('lesson-state').textContent = completed(lesson()) ? 'Completado' : 'Por resolver';
  document.querySelectorAll('[data-lesson]').forEach((button) => {
    const item = lessons[Number(button.dataset.lesson)];
    button.querySelector('.completion').textContent = completed(item) ? '\u2713' : '';
  });
}
function cursor() {
  const editor = get('editor');
  const count = editor.value.split('\n').length;
  get('line-numbers').textContent = Array.from({ length: count }, (_, index) => index + 1).join('\n');
  get('line-numbers').scrollTop = editor.scrollTop;
  get('cursor').textContent = `Linea ${editor.value.slice(0, editor.selectionStart).split('\n').length}`;
}
function fileTabs() {
  get('file-tabs').replaceChildren();
  for (const name of Object.keys(draft().files)) {
    const button = node('button', '', name);
    button.setAttribute('role', 'tab');
    button.setAttribute('aria-selected', String(name === activeFile));
    button.addEventListener('click', () => {
      saveEditor();
      activeFile = name;
      get('editor').value = draft().files[name];
      fileTabs();
      cursor();
    });
    get('file-tabs').append(button);
  }
}
function clearFeedback() {
  get('feedback-summary').textContent = 'Tu solucion todavia no fue evaluada.';
  get('feedback-badge').textContent = 'SIN INTENTOS';
  get('checks').replaceChildren();
  get('error-detail').hidden = true;
  get('output').textContent = 'Sin ejecucion.';
  get('output-label').textContent = 'Salida de Python';
  get('memory-section').hidden = true;
  document.querySelector('.feedback-area').classList.remove('success', 'failure');
}
function selectLesson(index) {
  stopExecution(false);
  current = Math.max(0, Math.min(index, lessons.length - 1));
  const item = lesson();
  savedState.selected = item.id;
  if (!savedState.drafts[item.id]) savedState.drafts[item.id] = { files: { ...item.files }, inputs: item.inputs };
  activeFile = 'solucion.py';
  revealed = 0;
  get('lesson-title').textContent = item.title;
  get('lesson-group').textContent = item.group;
  get('lesson-counter').textContent = `${item.id} / ${lessons.length}`;
  get('theory').replaceChildren(...item.theory.map((paragraph) => node('p', '', paragraph)));
  get('example').textContent = item.example;
  get('task').textContent = item.task;
  get('hints').replaceChildren();
  get('hint-count').textContent = `${item.hints.length} pistas disponibles`;
  get('hint').disabled = false;
  get('previous').disabled = current === 0;
  get('following').disabled = current === lessons.length - 1;
  get('editor').value = draft().files[activeFile];
  get('stdin').value = draft().inputs;
  document.querySelectorAll('[data-lesson]').forEach((button) => {
    const selected = Number(button.dataset.lesson) === current;
    button.classList.toggle('active', selected);
    if (selected) button.setAttribute('aria-current', 'step'); else button.removeAttribute('aria-current');
  });
  fileTabs();
  clearFeedback();
  cursor();
  persist();
  updateProgress();
  document.querySelector('.route').open = !matchMedia('(max-width:760px)').matches;
  icons();
}
function setBusy(value) {
  busy = value;
  get('execute').disabled = value;
  get('validate').disabled = value;
  get('editor').readOnly = value;
  get('stdin').readOnly = value;
  get('restore').disabled = value;
  get('stop').hidden = !value;
  document.querySelector('.feedback-area').setAttribute('aria-busy', String(value));
}
function stopExecution(showMessage = true) {
  if (worker) worker.terminate();
  worker = null;
  clearTimeout(deadline);
  setBusy(false);
  get('runtime-status').textContent = 'Python en el navegador';
  if (showMessage) {
    get('feedback-badge').textContent = 'DETENIDO';
    get('feedback-summary').textContent = 'Ejecucion detenida. Tu codigo se conserva. Si habia un while, revisa que su condicion pueda llegar a ser falsa.';
  }
}
function describeError(error, parent) {
  const location = error.line ? ` \u00b7 ${error.file || activeFile}, linea ${error.line}` : '';
  parent.append(node('strong', '', `${error.type}${location}`), node('pre', '', error.message), node('p', '', error.explanation));
}
function showResult(payload, mode, codeFingerprint) {
  get('output-label').textContent = mode === 'run' ? 'Salida de Python' : 'Salida del ultimo caso de prueba';
  get('output').textContent = payload.output || '(Sin salida: print() no mostro texto.)';
  get('output-section').open = true;
  const feedback = document.querySelector('.feedback-area');
  if (payload.error) {
    get('error-detail').replaceChildren();
    describeError(payload.error, get('error-detail'));
    get('error-detail').hidden = false;
    get('feedback-badge').textContent = 'REVISAR';
    get('feedback-summary').textContent = 'Python encontro un error. Revisa la linea indicada y volve a probar.';
    feedback.classList.add('failure');
  } else if (mode === 'run') {
    get('feedback-badge').textContent = 'EJECUTADO';
    get('feedback-summary').textContent = 'El programa termino sin errores de ejecucion. Esto no asegura que cumpla la consigna: falta validar los casos de prueba.';
    const variables = Object.entries(payload.variables || {});
    get('memory-section').hidden = !variables.length;
    get('memory').replaceChildren();
    for (const [name, value] of variables) {
      const row = node('div');
      row.append(node('dt', '', name), node('dd', '', value));
      get('memory').append(row);
    }
  } else {
    const passed = payload.checks.filter((check) => check.passed).length;
    get('feedback-badge').textContent = `${passed} / ${payload.checks.length} PRUEBAS`;
    get('feedback-summary').textContent = payload.passed
      ? 'Tu solucion supera todos los casos de esta practica. Lee por que pasan y proba cambiar algun dato antes de avanzar. Estas pruebas no demuestran todos los casos posibles.'
      : 'Hay partes por revisar. Compara lo esperado con lo obtenido; cada prueba explica que condicion esta comprobando.';
    feedback.classList.add(payload.passed ? 'success' : 'failure');
    for (const check of payload.checks) {
      const details = node('details', `check${check.passed ? '' : ' failed'}`);
      details.open = !check.passed;
      const summary = node('summary');
      summary.append(node('span', '', check.title), node('span', 'check-state', check.passed ? 'BIEN' : 'REVISAR'));
      details.append(summary, node('p', '', check.explanation), node('pre', '', `Esperado: ${check.expected}\nObtenido: ${check.actual}`));
      if (check.error) describeError(check.error, details);
      get('checks').append(details);
    }
    if (payload.passed) savedState.completed[lesson().id] = codeFingerprint;
    else delete savedState.completed[lesson().id];
    persist();
    updateProgress();
  }
}
function execute(mode) {
  if (busy || !lesson()) return;
  saveEditor();
  if (Object.values(draft().files).some((code) => code.length > 20000)) {
    notice('Cada archivo de practica admite hasta 20000 caracteres.');
    return;
  }
  if (storageAvailable) notice('');
  clearFeedback();
  setBusy(true);
  const codeFingerprint = fingerprint();
  const request = { mode, files: { ...draft().files }, inputs: draft().inputs.split('\n'), lesson: lesson() };
  get('runtime-status').textContent = 'Preparando Python. La primera carga descarga el interprete y necesita Internet.';
  get('feedback-summary').textContent = 'Preparando la ejecucion...';
  const instance = new Worker('/python-worker.js');
  worker = instance;
  const fail = (message) => {
    stopExecution(false);
    get('feedback-summary').textContent = message;
    get('feedback-badge').textContent = 'SIN COMPLETAR';
  };
  deadline = setTimeout(() => fail('Python no pudo cargar en 90 segundos. Revisa Internet y volve a intentar; tu borrador esta guardado.'), 90000);
  instance.onerror = () => fail('No se pudo iniciar Python. Revisa la conexion a Internet o las restricciones del navegador y volve a intentar.');
  instance.onmessage = (event) => {
    if (worker !== instance) return;
    const message = event.data;
    if (message.type === 'ready') {
      clearTimeout(deadline);
      get('runtime-status').textContent = mode === 'run' ? 'Ejecutando tu codigo...' : 'Comprobando los casos de la consigna...';
      deadline = setTimeout(() => fail('Se detuvo el programa tras 6 segundos. Puede haber un bucle infinito o demasiado trabajo. Revisa que el while cambie la variable de su condicion.'), 6000);
      instance.postMessage(request);
    } else if (message.type === 'result') {
      stopExecution(false);
      showResult(message.payload, mode, codeFingerprint);
    } else if (message.type === 'failure') fail(message.message);
  };
}

get('editor').addEventListener('input', () => {
  saveEditor();
  cursor();
  if (get('feedback-badge').textContent !== 'SIN INTENTOS') {
    clearFeedback();
    get('feedback-summary').textContent = 'Codigo modificado. La devolucion anterior ya no corresponde a este borrador.';
  }
});
get('editor').addEventListener('scroll', cursor);
get('editor').addEventListener('click', cursor);
get('editor').addEventListener('keyup', cursor);
get('editor').addEventListener('keydown', (event) => {
  const editor = get('editor');
  if (editor.readOnly || event.ctrlKey || event.metaKey || event.altKey) return;
  if (event.key === 'Tab' && !event.shiftKey) {
    event.preventDefault();
    editor.setRangeText('    ', editor.selectionStart, editor.selectionEnd, 'end');
    editor.dispatchEvent(new Event('input'));
  } else if (event.key === 'Enter') {
    event.preventDefault();
    const line = editor.value.slice(0, editor.selectionStart).split('\n').at(-1);
    const indent = line.match(/^ */)[0] + (line.trimEnd().endsWith(':') ? '    ' : '');
    editor.setRangeText('\n' + indent, editor.selectionStart, editor.selectionEnd, 'end');
    editor.dispatchEvent(new Event('input'));
  }
});
get('stdin').addEventListener('input', saveEditor);
get('execute').addEventListener('click', () => execute('run'));
get('validate').addEventListener('click', () => execute('validate'));
get('stop').addEventListener('click', () => stopExecution());
get('hint').addEventListener('click', () => {
  if (revealed < lesson().hints.length) get('hints').append(node('li', '', lesson().hints[revealed++]));
  get('hint-count').textContent = `${revealed} / ${lesson().hints.length} pistas`;
  get('hint').disabled = revealed === lesson().hints.length;
});
get('previous').addEventListener('click', () => selectLesson(current - 1));
get('following').addEventListener('click', () => selectLesson(current + 1));
matchMedia('(max-width:760px)').addEventListener('change', (event) => {
  document.querySelector('.route').open = !event.matches;
});
window.addEventListener('resize', () => {
  if (window.innerWidth > 760) document.querySelector('.route').open = true;
});
get('restore').addEventListener('click', () => {
  if (!confirm('Restablecer los archivos de esta practica? Se reemplazara tu borrador actual.')) return;
  delete savedState.drafts[lesson().id];
  delete savedState.completed[lesson().id];
  selectLesson(current);
});
async function initialize() {
  get('execute').disabled = true;
  get('validate').disabled = true;
  try {
    const raw = JSON.parse(localStorage.getItem(storageKey) || 'null');
    if (raw && typeof raw.drafts === 'object' && raw.drafts && typeof raw.completed === 'object' && raw.completed) savedState = raw;
  } catch { notice('No se pudo recuperar el borrador guardado. El recorrido empezara desde el inicio.'); }
  try {
    const response = await fetch('/api/curso');
    if (!response.ok) throw new Error('No se pudo cargar el recorrido.');
    lessons = await response.json();
    let group = '';
    lessons.forEach((item, index) => {
      if (item.group !== group) { get('lessons').append(node('h3', '', item.group)); group = item.group; }
      const button = node('button', 'lesson-button');
      button.dataset.lesson = index;
      button.append(node('span', 'lesson-number', String(item.id).padStart(2, '0')), node('span', '', item.title), node('span', 'completion'));
      button.addEventListener('click', () => selectLesson(index));
      get('lessons').append(button);
      const stored = savedState.drafts[item.id];
      if (stored && (!stored.files || Object.keys(item.files).some((name) => typeof stored.files[name] !== 'string') || typeof stored.inputs !== 'string')) delete savedState.drafts[item.id];
    });
    const selected = lessons.findIndex((item) => item.id === savedState.selected);
    selectLesson(selected < 0 ? 0 : selected);
  } catch (error) { notice(`${error.message} Mantene el servidor local abierto y recarga la pagina.`); }
  icons();
}
initialize();