declare module '/pyodide/pyodide.mjs' {
  export function loadPyodide(config: { indexURL: string }): Promise<any>;
}