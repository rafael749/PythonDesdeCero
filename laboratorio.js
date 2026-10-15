const byId = (id) => document.getElementById(id);
const activities = {
  1: { title: 'Buscar y reemplazar', description: 'Una lista entra. Una nueva lista sale. La original queda intacta.', concept: 'str.replace() devuelve un nuevo string. append() lo agrega a nueva_lista; las frases originales no cambian.' },
  2: { title: 'Validar un email', description: 'Cada condici\u00f3n puede detener la funci\u00f3n. Solo si pasan todas, devuelve True.', concept: 'return termina la funci\u00f3n inmediatamente. Si aparece return False, las condiciones que siguen ya no se ejecutan.' },
  3: { title: 'Analizar n\u00fameros', description: 'Comparar, ordenar y filtrar: tres funciones, una misma lista.', concept: 'El ordenamiento burbuja compara vecinos y los intercambia. temporal conserva un valor mientras se reemplaza su posici\u00f3n.' },
  4: { title: 'Adivinar la palabra', description: 'Una letra por turno. Cinco errores como m\u00e1ximo. Cada intento cambia el estado del juego.', concept: 'input() recibe texto; continue vuelve al inicio del while. Las entradas inv\u00e1lidas y las letras repetidas no suman errores.' }
};
let exercise = 1;
let sources = {};
let steps = [];
let position = 0;
let timer = null;
let guesses = [];
let gameFinished = false;
let busy = false;
let generation = 0;

function icons() { window.lucide?.createIcons(); }
function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}
function field(label, name, value, multiline = false) {
  const wrapper = element('div', 'field');
  const labelNode = element('label', '', label);
  labelNode.htmlFor = name;
  const input = element(multiline ? 'textarea' : 'input');
  input.id = name;
  input.name = name;
  if (!multiline) input.type = 'text';
  input.value = value;
  input.maxLength = name === 'phrases' ? 2000 : name === 'numbers' ? 500 : name === 'email' ? 254 : 100;
  input.autocomplete = 'off';
  input.spellcheck = false;
  wrapper.append(labelNode, input);
  return wrapper;
}
function stop() {
  clearInterval(timer);
  timer = null;
  byId('play').innerHTML = '<i data-lucide="play"></i>';
  byId('play').setAttribute('aria-label', 'Reproducir pasos');
  icons();
}
function configure(nextExercise) {
  generation += 1;
  stop();
  busy = false;
  exercise = nextExercise;
  guesses = [];
  gameFinished = false;
  steps = [];
  position = 0;
  byId('error').hidden = true;
  document.querySelectorAll('[data-exercise]').forEach((button) => {
    const selected = Number(button.dataset.exercise) === exercise;
    button.classList.toggle('active', selected);
    if (selected) button.setAttribute('aria-current', 'page');
    else button.removeAttribute('aria-current');
  });
  byId('exercise-label').textContent = `EJERCICIO 0${exercise} / 04`;
  byId('exercise-title').textContent = activities[exercise].title;
  byId('exercise-description').textContent = activities[exercise].description;
  byId('concept').textContent = activities[exercise].concept;
  const fields = byId('fields');
  fields.replaceChildren();
  if (exercise === 1) {
    fields.append(field('Frases \u00b7 una por l\u00ednea', 'phrases', 'Me gusta el Mate\nTomo mate\nNo tomo Mate', true));
    const row = element('div', 'field-row');
    row.append(field('Buscar', 'word', 'Mate'), field('Reemplazar por', 'replacement', 'cafe'));
    fields.append(row);
  } else if (exercise === 2) {
    fields.append(field('Email', 'email', 'juan@gmail.com'));
    const samples = element('div', 'sample-emails');
    for (const email of ['juan@gmail.com', 'juan@.com', 'juan@gmail.c']) {
      const button = element('button', '', email);
      button.type = 'button';
      button.addEventListener('click', () => { byId('email').value = email; run(); });
      samples.append(button);
    }
    fields.append(samples);
  } else if (exercise === 3) {
    fields.append(field('N\u00fameros \u00b7 separados por comas o espacios', 'numbers', '4, 7, 2, 9, 1, 5, 8, 3, 6', true));
  } else {
    const wrapper = element('div', 'field');
    const label = element('label', '', 'Palabra de pr\u00e1ctica');
    label.htmlFor = 'secret';
    const select = element('select');
    select.id = 'secret';
    for (const word of ['python', 'lista', 'bucle', 'variable']) {
      const option = element('option', '', word);
      option.value = word;
      select.append(option);
    }
    select.addEventListener('change', () => { guesses = []; gameFinished = false; run(true); });
    wrapper.append(label, select);
    fields.append(wrapper, field('Tu intento', 'letter', ''));
    byId('letter').maxLength = 50;
  }
  byId('run').innerHTML = `<i data-lucide="${exercise === 4 ? 'arrow-right' : 'play'}"></i><span>${exercise === 4 ? 'Probar letra' : 'Ejecutar Python'}</span>`;
  byId('run').disabled = false;
  byId('result').replaceChildren(element('p', 'empty', 'Preparando la ejecuci\u00f3n...'));
  icons();
  run(true);
}

async function run(initial = false) {
  if (busy || (exercise === 4 && gameFinished && !initial)) return;
  stop();
  busy = true;
  const requestGeneration = generation;
  byId('run').disabled = true;
  byId('fields').querySelectorAll('input, textarea, select, button').forEach((control) => { control.disabled = true; });
  byId('error').hidden = true;
  byId('result-status').textContent = 'EJECUTANDO';
  const data = { exercise };
  let pendingGuesses = guesses;
  if (exercise === 1) ['phrases', 'word', 'replacement'].forEach((name) => { data[name] = byId(name).value; });
  if (exercise === 2) data.email = byId('email').value;
  if (exercise === 3) data.numbers = byId('numbers').value;
  if (exercise === 4) {
    data.secret = byId('secret').value;
    pendingGuesses = initial ? guesses : [...guesses, byId('letter').value];
    data.guesses = pendingGuesses;
  }
  const oldStepCount = steps.length;
  try {
    const response = await fetch('/api/run', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) });
    const payload = await response.json();
    if (requestGeneration !== generation) return;
    if (!response.ok) throw new Error(payload.error || 'No se pudo ejecutar el ejercicio.');
    steps = payload.steps;
    position = exercise === 4 && !initial ? Math.min(Math.max(oldStepCount - 1, 0), steps.length - 1) : 0;
    if (exercise === 4) {
      guesses = pendingGuesses;
      gameFinished = payload.result.finished;
      byId('letter').value = '';
      byId('letter').disabled = gameFinished;
    }
    renderResult(payload);
    byId('result-status').textContent = 'EJECUTADO';
    byId('trace-count').textContent = `${steps.length} pasos registrados`;
    renderStep();
  } catch (error) {
    if (requestGeneration !== generation) return;
    byId('error').textContent = error instanceof TypeError ? 'No hay conexi\u00f3n con Python. El servidor local debe seguir abierto.' : error.message;
    byId('error').hidden = false;
    byId('result-status').textContent = 'SIN RESULTADO';
    byId('result').replaceChildren(element('p', 'empty', 'La entrada no se pudo ejecutar.'));
    steps = [];
    position = 0;
    renderStep();
  } finally {
    if (requestGeneration === generation) {
      busy = false;
      byId('fields').querySelectorAll('input, textarea, select, button').forEach((control) => { control.disabled = false; });
      if (exercise === 4) byId('letter').disabled = gameFinished;
      byId('run').disabled = gameFinished;
      if (exercise === 4 && !initial && !gameFinished) byId('letter').focus();
    }
  }
}

function tiles(numbers) {
  const row = element('div', 'number-tiles');
  for (const number of numbers) row.append(element('span', `number-tile${number > 5 ? ' over-five' : ''}`, number));
  if (!numbers.length) row.append(element('span', 'result-label', '[]'));
  return row;
}
function renderResult(payload) {
  const area = byId('result');
  const result = payload.result;
  area.replaceChildren();
  if (exercise === 1) {
    area.append(element('p', 'result-label', 'nueva_lista'));
    const list = element('ol', 'result-list');
    result.new.forEach((phrase, index) => {
      const row = element('li');
      row.append(element('span', 'index', index), element('span', 'result-value', JSON.stringify(phrase)));
      list.append(row);
    });
    if (!result.new.length) list.append(element('li', 'result-value', '[]'));
    area.append(list, element('p', 'result-note', 'La lista original no se modific\u00f3.'), element('div', 'original-preview', `lista = ${JSON.stringify(result.original)}`));
  } else if (exercise === 2) {
    area.append(element('div', `boolean${result ? '' : ' invalid'}`, result ? 'True' : 'False'), element('div', 'boolean-label', result ? 'Cumple las 7 reglas' : 'No cumple todas las reglas'));
    const last = steps.findLast((step) => step.function === 'validar_email' && step.event === 'return');
    area.append(element('div', 'return-expression', `validar_email(${JSON.stringify(byId('email').value)})`));
    if (last) area.append(element('p', 'result-note', `La funci\u00f3n termin\u00f3 en la l\u00ednea ${last.line}, con return ${last.returnValue}.`));
  } else if (exercise === 3) {
    const metrics = element('div', 'metrics');
    for (const [label, value] of [['M\u00e1s alto', result.largest], ['M\u00e1s bajo', result.smallest]]) {
      const metric = element('div', 'metric');
      metric.append(element('small', '', label), element('strong', '', value));
      metrics.append(metric);
    }
    area.append(metrics, element('div', 'result-label', 'Ordenada de menor a mayor'), tiles(result.sorted), element('div', 'result-label', 'Mayores a 5 \u00b7 en su orden original'), tiles(result.filtered));
  } else {
    area.append(element('p', 'result-label', 'palabra_secreta \u00b7 progreso'));
    const word = element('div', 'word-progress');
    word.setAttribute('aria-label', `Palabra: ${result.progress}`);
    for (const letter of result.progress.split(' ')) word.append(element('span', 'letter-tile', letter));
    const meter = element('div', 'error-meter');
    for (let index = 0; index < 5; index += 1) meter.append(element('span', index < result.errors ? 'used' : ''));
    meter.append(element('strong', '', `${result.errors} / 5 errores`));
    area.append(word, meter, element('div', 'game-status', result.finished ? result.won ? '\u00a1Ganaste! Palabra completa.' : `Perdiste. La palabra era: ${byId('secret').value}` : 'Partida en curso'));
    area.append(element('p', 'result-note', `Letras intentadas: ${result.letters.join(', ') || 'ninguna'}`));
    const history = element('div', 'game-history', payload.output);
    history.setAttribute('aria-label', 'Mensajes originales del juego');
    area.append(history);
    history.scrollTop = history.scrollHeight;
  }
}

function renderStep() {
  const step = steps[position];
  byId('timeline').max = Math.max(steps.length - 1, 0);
  byId('timeline').value = position;
  byId('timeline').disabled = !steps.length;
  byId('step-position').textContent = `${steps.length ? position + 1 : 0} / ${steps.length}`;
  byId('first').disabled = !position;
  byId('prev').disabled = !position;
  byId('next').disabled = !steps.length || position === steps.length - 1;
  byId('play').disabled = !steps.length;
  byId('trace-count').textContent = `${steps.length} pasos registrados`;
  const filename = step?.file || `ejercicio_0${exercise}.py`;
  byId('source-name').textContent = filename;
  byId('function-name').textContent = step?.function || '';
  byId('step-explanation').textContent = !step ? 'Sin pasos registrados.' : step.event === 'return'
    ? `Salida de ${step.function}(). Valor de retorno: ${step.returnValue}.`
    : step.event === 'input' ? 'input() espera la siguiente letra. El juego todav\u00eda no termin\u00f3.'
    : `Antes de ejecutar la l\u00ednea ${step.line}. Estos son los valores actuales.`;
  const source = byId('source');
  const scroll = source.scrollTop;
  source.replaceChildren();
  for (const line of sources[filename] || []) {
    const row = element('div', `code-line${line.text.trim().startsWith('#') ? ' comment' : ''}${line.number === step?.line ? ' active' : ''}`);
    row.append(element('span', 'line-number', line.number), element('span', '', line.text));
    source.append(row);
  }
  source.scrollTop = scroll;
  const active = source.querySelector('.active');
  if (active) {
    const offset = active.getBoundingClientRect().top - source.getBoundingClientRect().top;
    if (offset < 0 || offset > source.clientHeight - active.clientHeight) source.scrollTop += offset - source.clientHeight / 2;
  }
  const variables = byId('variables');
  variables.replaceChildren();
  const previous = steps[position - 1];
  for (const [name, value] of Object.entries(step?.variables || {})) {
    const row = element('div');
    const changed = previous?.function === step.function && previous.variables[name] !== value;
    row.append(element('dt', '', name), element('dd', changed ? 'changed' : '', value));
    variables.append(row);
  }
}

byId('exercise-form').addEventListener('submit', (event) => { event.preventDefault(); run(); });
byId('exercise-nav').addEventListener('click', (event) => {
  const button = event.target.closest('[data-exercise]');
  if (button) configure(Number(button.dataset.exercise));
});
byId('reset').addEventListener('click', () => configure(exercise));
byId('first').addEventListener('click', () => { stop(); position = 0; renderStep(); });
byId('prev').addEventListener('click', () => { stop(); position = Math.max(0, position - 1); renderStep(); });
byId('next').addEventListener('click', () => { stop(); position = Math.min(steps.length - 1, position + 1); renderStep(); });
byId('timeline').addEventListener('input', (event) => { stop(); position = Number(event.target.value); renderStep(); });
function startPlayback() {
  if (position >= steps.length - 1) position = 0;
  byId('play').innerHTML = '<i data-lucide="pause"></i>';
  byId('play').setAttribute('aria-label', 'Pausar pasos');
  icons();
  renderStep();
  timer = setInterval(() => {
    if (position >= steps.length - 1) { stop(); return; }
    position += 1;
    renderStep();
  }, Number(byId('speed').value));
}
byId('play').addEventListener('click', () => { if (timer) stop(); else startPlayback(); });
byId('speed').addEventListener('change', () => { if (timer) { stop(); startPlayback(); } });
async function initialize() {
  icons();
  try {
    const response = await fetch('/api/code');
    if (!response.ok) throw new Error('No se pudo leer el c\u00f3digo de los ejercicios.');
    sources = await response.json();
    byId('connection').innerHTML = '<span class="dot"></span>Python local conectado';
    configure(1);
  } catch (error) {
    byId('connection').textContent = 'Python desconectado';
    byId('error').textContent = 'No se pudo conectar con el servidor local de Python. Abre la direcci\u00f3n del servidor, no el archivo HTML directamente.';
    byId('error').hidden = false;
    byId('run').disabled = true;
  }
}
initialize();