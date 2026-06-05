interface Props {
  files: File[]
  onRemove: (index: number) => void
}

export default function FileQueue({ files, onRemove }: Props) {
  if (files.length === 0) return null

  return (
    <div className="mt-4 space-y-1.5">
      <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
        {files.length} file{files.length !== 1 ? 's' : ''} queued
      </p>
      <ul className="max-h-48 overflow-y-auto rounded-lg border border-slate-200 bg-white divide-y divide-slate-100">
        {files.map((f, i) => (
          <li key={i} className="flex items-center justify-between px-3 py-2 text-sm">
            <div className="flex items-center gap-2 min-w-0">
              <FileIcon name={f.name} />
              <span className="truncate text-slate-700">{f.name}</span>
              <span className="shrink-0 text-xs text-slate-400">{formatBytes(f.size)}</span>
            </div>
            <button
              onClick={() => onRemove(i)}
              className="ml-2 shrink-0 rounded p-0.5 text-slate-400 hover:bg-slate-100 hover:text-slate-600"
              aria-label="Remove"
            >
              <svg className="h-3.5 w-3.5" viewBox="0 0 16 16" fill="currentColor">
                <path d="M4.28 3.22a.75.75 0 00-1.06 1.06L6.94 8l-3.72 3.72a.75.75 0 101.06 1.06L8 9.06l3.72 3.72a.75.75 0 101.06-1.06L9.06 8l3.72-3.72a.75.75 0 00-1.06-1.06L8 6.94 4.28 3.22z" />
              </svg>
            </button>
          </li>
        ))}
      </ul>
    </div>
  )
}

function FileIcon({ name }: { name: string }) {
  const ext = name.split('.').pop()?.toLowerCase() ?? ''
  const colors: Record<string, string> = {
    pdf: 'text-red-500',
    docx: 'text-blue-500',
    xlsx: 'text-green-600',
    jpg: 'text-amber-500',
    jpeg: 'text-amber-500',
    png: 'text-purple-500',
    tiff: 'text-orange-500',
    tif: 'text-orange-500',
  }
  return (
    <svg className={`h-4 w-4 shrink-0 ${colors[ext] ?? 'text-slate-400'}`} viewBox="0 0 16 16" fill="currentColor">
      <path d="M4 1.75A.75.75 0 014.75 1h4.69a.75.75 0 01.53.22l3.06 3.06a.75.75 0 01.22.53V13.25A.75.75 0 0112.5 14h-7.75A.75.75 0 014 13.25V1.75z" />
    </svg>
  )
}

function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(0)} KB`
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}
