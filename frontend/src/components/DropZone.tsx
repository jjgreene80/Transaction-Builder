import { useCallback, useRef, useState } from 'react'

interface Props {
  onFiles: (files: File[]) => void
  disabled: boolean
}

const ACCEPTED = '.pdf,.jpg,.jpeg,.png,.tiff,.tif,.docx,.xlsx'

export default function DropZone({ onFiles, disabled }: Props) {
  const [dragging, setDragging] = useState(false)
  const inputRef = useRef<HTMLInputElement>(null)

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault()
      setDragging(false)
      if (disabled) return
      const files = Array.from(e.dataTransfer.files)
      if (files.length) onFiles(files)
    },
    [disabled, onFiles],
  )

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files ?? [])
    if (files.length) onFiles(files)
    e.target.value = ''
  }

  return (
    <div
      onDragOver={(e) => { e.preventDefault(); if (!disabled) setDragging(true) }}
      onDragLeave={() => setDragging(false)}
      onDrop={handleDrop}
      onClick={() => !disabled && inputRef.current?.click()}
      className={[
        'relative flex flex-col items-center justify-center gap-3 rounded-xl border-2 border-dashed px-8 py-14 text-center transition-colors cursor-pointer select-none',
        dragging
          ? 'border-brand-500 bg-brand-50'
          : disabled
          ? 'border-slate-200 bg-slate-100 cursor-not-allowed opacity-60'
          : 'border-slate-300 bg-white hover:border-brand-400 hover:bg-brand-50',
      ].join(' ')}
    >
      <input
        ref={inputRef}
        type="file"
        multiple
        accept={ACCEPTED}
        className="sr-only"
        onChange={handleChange}
        disabled={disabled}
      />

      {/* Upload icon */}
      <div className={`rounded-full p-4 ${dragging ? 'bg-brand-100' : 'bg-slate-100'}`}>
        <svg className={`h-8 w-8 ${dragging ? 'text-brand-600' : 'text-slate-400'}`} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5" />
        </svg>
      </div>

      <div>
        <p className="text-sm font-semibold text-slate-700">
          Drop transaction files here or <span className="text-brand-600">browse</span>
        </p>
        <p className="mt-1 text-xs text-slate-400">
          PDF · JPG · PNG · TIFF · DOCX · XLSX — multiple files OK
        </p>
      </div>
    </div>
  )
}
