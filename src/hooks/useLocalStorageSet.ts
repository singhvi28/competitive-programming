import React, { useState, useCallback } from 'react';

export function useLocalStorageSet(key: string, defaultFilename: string = 'export_data') {
  const [solvedSet, setSolvedSet] = useState<Set<string>>(() => {
    try {
      const stored = localStorage.getItem(key);
      if (stored) {
        const arr = JSON.parse(stored);
        if (Array.isArray(arr)) {
          return new Set<string>(arr.map(String));
        }
      }
    } catch (e) {
      console.warn(`Error reading localStorage key "${key}":`, e);
    }
    return new Set<string>();
  });

  const save = useCallback(
    (newSet: Set<string>) => {
      try {
        localStorage.setItem(key, JSON.stringify(Array.from(newSet)));
      } catch (e) {
        console.warn(`Error saving to localStorage key "${key}":`, e);
      }
    },
    [key]
  );

  const toggle = useCallback(
    (id: string | number) => {
      const strId = String(id);
      setSolvedSet((prev) => {
        const next = new Set(prev);
        if (next.has(strId)) {
          next.delete(strId);
        } else {
          next.add(strId);
        }
        save(next);
        return next;
      });
    },
    [save]
  );

  const has = useCallback(
    (id: string | number) => {
      return solvedSet.has(String(id));
    },
    [solvedSet]
  );

  const addMany = useCallback(
    (ids: (string | number)[]) => {
      setSolvedSet((prev) => {
        const next = new Set(prev);
        let changed = false;
        ids.forEach((id) => {
          const strId = String(id);
          if (!next.has(strId)) {
            next.add(strId);
            changed = true;
          }
        });
        if (changed) {
          save(next);
        }
        return next;
      });
    },
    [save]
  );

  const reset = useCallback(() => {
    const next = new Set<string>();
    setSolvedSet(next);
    save(next);
  }, [save]);

  const importArray = useCallback(
    (arr: (string | number)[]) => {
      const next = new Set<string>(arr.map(String));
      setSolvedSet(next);
      save(next);
      return next.size;
    },
    [save]
  );

  const exportJSON = useCallback(
    (customFilename?: string) => {
      const filename =
        customFilename || `${defaultFilename}_${new Date().toISOString().slice(0, 10)}.json`;
      const dataStr =
        'data:text/json;charset=utf-8,' +
        encodeURIComponent(JSON.stringify(Array.from(solvedSet)));
      const downloadAnchor = document.createElement('a');
      downloadAnchor.setAttribute('href', dataStr);
      downloadAnchor.setAttribute('download', filename);
      document.body.appendChild(downloadAnchor);
      downloadAnchor.click();
      downloadAnchor.remove();
    },
    [solvedSet, defaultFilename]
  );

  const importJSON = useCallback(
    (
      event: React.ChangeEvent<HTMLInputElement>,
      onSuccess?: (count: number) => void,
      onError?: () => void
    ) => {
      const file = event.target.files?.[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const imported = JSON.parse(e.target?.result as string);
          if (Array.isArray(imported)) {
            const count = importArray(imported);
            onSuccess?.(count);
          } else {
            onError?.();
          }
        } catch {
          onError?.();
        }
      };
      reader.readAsText(file);
      // Reset input value so same file can be reloaded if needed
      event.target.value = '';
    },
    [importArray]
  );

  return {
    solvedSet,
    setSolvedSet,
    has,
    toggle,
    addMany,
    reset,
    clear: reset,
    importArray,
    importJSON,
    exportJSON,
    count: solvedSet.size,
  };
}
