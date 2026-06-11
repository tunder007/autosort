# Module documentation template

Use this header at the top of every Python module and TypeScript source file.

## Python

```python
"""
module_name.py — one-line role (e.g. README step 1: scan folder).

What it does:
  Brief description of responsibility.

Input:
  name: Type — what callers pass in

Output:
  Type — what callers receive

Does not:
  List responsibilities that belong elsewhere.
"""
```

## TypeScript / TSX

```typescript
/**
 * fileName.ts — one-line role.
 *
 * What it does:
 *   Brief description.
 *
 * Input:
 *   (props, params, or "none" for pages)
 *
 * Output:
 *   UI, data, or side effects
 *
 * Does not:
 *   List out-of-scope behavior.
 */
```

## JSDoc for exported functions (web)

```typescript
/**
 * Short summary.
 *
 * @param jobId - Server job identifier
 * @returns Promise that resolves when download starts
 */
export async function downloadJob(jobId: number): Promise<void> { ... }
```

## Function docstrings (Python public API)

```python
def scan_folder(folder_path: Path) -> SortMatrix:
    """Scan top-level files only and group by detected type."""
```

Keep function bodies self-explanatory; only add comments for non-obvious logic.
