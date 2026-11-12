import { useEffect, useRef, useCallback } from 'react';
import { useBoardStore } from '../store/boardStore';
import type { BoardData } from '../types/board';

export function useBoardWorker() {
  const workerRef = useRef<Worker | null>(null);

  const { 
    workerStatus: status, 
    setWorkerStatus: setStatus, 
    setWorkerError: setError, 
    setBoardData 
  } = useBoardStore();

  useEffect(() => {
    workerRef.current = new Worker(new URL('../workers/pyodideWorker.ts', import.meta.url), {
      type: 'module' 
    });

    workerRef.current.onmessage = (event) => {
      const { type, status, payload, message } = event.data;

      if (type === 'STATUS') {
        setStatus(status);

      } else if (type === 'RESULT') {
        setStatus('idle');

        if (payload.boardData) {
          setBoardData(payload.boardData as BoardData);
        }
      } else if (type === 'ERROR') {
        setStatus('error');
        setError(message);
        console.error("Pyodide worker error:", message);
      }
    };

    workerRef.current.onerror = (error) => {
      console.error(`Pyodide CRITICAL error:`, error.message);
      setStatus('error');
    };

    workerRef.current.onmessageerror = (error) => {
      console.error("Pyodide deserializing error", error);
      setStatus('error');
    };

    return () => {
      workerRef.current?.terminate();
    };
  }, [setBoardData, setStatus, setError]);


  const processFiles = useCallback((files: FileList) => {
    if (workerRef.current && (status === 'idle' || status === 'error')) {
      setStatus('loading_pyodide');
      setError(null);
      
      workerRef.current.postMessage({ 
        type: 'PROCESS_FILES', 
        files: Array.from(files)
      });
    }
  }, [status, setStatus, setError]);

  return { status, processFiles };
}