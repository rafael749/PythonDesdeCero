importScripts('https://cdn.jsdelivr.net/pyodide/v0.27.7/full/pyodide.js');

let runtime;
async function prepare() {
  try {
    const response = await fetch('/practica_motor.py');
    if (!response.ok) throw new Error('No se pudo cargar el corrector.');
    const source = await response.text();
    runtime = await loadPyodide({ indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.27.7/full/' });
    runtime.runPython(source);
    self.postMessage({ type: 'ready' });
  } catch (error) {
    self.postMessage({ type: 'failure', message: `No se pudo iniciar Python. Revisa la conexion a Internet y volve a intentar. ${error.message}` });
  }
}
self.onmessage = (event) => {
  try {
    runtime.globals.set('request_json', JSON.stringify(event.data));
    const response = runtime.runPython('json.dumps(evaluar(json.loads(request_json)), ensure_ascii=False)');
    self.postMessage({ type: 'result', payload: JSON.parse(response) });
  } catch (error) {
    self.postMessage({ type: 'failure', message: `Python se detuvo: ${error.message}` });
  }
};
prepare();