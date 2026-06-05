import { useState, useCallback } from 'react'
import type { ProcessingResult } from './types'
import DropZone from './components/DropZone'
import FileQueue from './components/FileQueue'
import ResultsPanel from './components/ResultsPanel'
import MissingDocsPanel from './components/MissingDocsPanel'

type AppState = 'idle' | 'processing' | 'done' | 'error'

export default function App() {
  const [queued, setQueued] = useState<File[]>([])
  const [state, setState] = useState<AppState>('idle')
  const [result, setResult] = useState<ProcessingResult | null>(null)
  const [errorMsg, setErrorMsg] = useState('')
  const [progress, setProgress] = useState('')

  const addFiles = useCallback((incoming: File[]) => {
    setQueued((prev) => {
      const names = new Set(prev.map((f) => f.name))
      return [...prev, ...incoming.filter((f) => !names.has(f.name))]
    })
  }, [])

  const removeFile = (index: number) => {
    setQueued((prev) => prev.filter((_, i) => i !== index))
  }

  const reset = () => {
    setQueued([])
    setState('idle')
    setResult(null)
    setErrorMsg('')
  }

  const process = async () => {
    if (queued.length === 0) return
    setState('processing')
    setProgress('Uploading files…')

    const form = new FormData()
    for (const f of queued) form.append('files', f)

    try {
      setProgress('Processing documents…')
      const res = await fetch('/api/process', { method: 'POST', body: form })

      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: res.statusText }))
        throw new Error(err.detail ?? 'Server error')
      }

      const data: ProcessingResult = await res.json()
      setResult(data)
      setState('done')
    } catch (e: unknown) {
      setErrorMsg(e instanceof Error ? e.message : 'Unknown error')
      setState('error')
    }
  }

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <header className="border-b border-slate-200 bg-white shadow-sm">
        <div className="mx-auto flex max-w-4xl items-center justify-between px-6 py-4">
          <div className="flex items-center gap-3">
            <div className="rounded-lg bg-brand-600 p-2">
              <svg className="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
              </svg>
            </div>
            <div>
              <h1 className="text-base font-bold text-slate-900">TC Doc Tool</h1>
              <p className="text-xs text-slate-500">Transaction File Organizer</p>
            </div>
          </div>
          {state !== 'idle' && (
            <button
              onClick={reset}
              className="rounded-lg border border-slate-200 px-3 py-1.5 text-xs font-medium text-slate-600 hover:bg-slate-100 transition-colors"
            >
              Start over
            </button>
          )}
        </div>
      </header>

      <main className="mx-auto max-w-4xl px-6 py-8">
        {/* Upload section — always visible until done */}
        {state !== 'done' && (
          <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="mb-4 text-sm font-semibold text-slate-700">Upload Transaction Files</h2>
            <DropZone onFiles={addFiles} disabled={state === 'processing'} />
            <FileQueue files={queued} onRemove={removeFile} />

            {state === 'error' && (
              <div className="mt-4 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
                <strong>Error:</strong> {errorMsg}
              </div>
            )}

            <div className="mt-5 flex items-center justify-between gap-4">
              <p className="text-xs text-slate-400">
                Supports: PDF, JPG, PNG, TIFF, DOCX, XLSX
              </p>
              <button
                onClick={process}
                disabled={queued.length === 0 || state === 'processing'}
                className="flex items-center gap-2 rounded-lg bg-brand-600 px-5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-brand-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {state === 'processing' ? (
                  <>
                    <Spinner />
                    {progress}
                  </>
                ) : (
                  <>
                    <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z" />
                    </svg>
                    Process {queued.length > 0 ? `${queued.length} file${queued.length !== 1 ? 's' : ''}` : 'Files'}
                  </>
                )}
              </button>
            </div>
          </div>
        )}

        {/* Results */}
        {state === 'done' && result && (
          <div className="space-y-5">
            {/* Missing docs — show at top so it's visible immediately */}
            <MissingDocsPanel missing={result.missing_docs} />

            <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
              <h2 className="mb-5 text-sm font-semibold text-slate-700">Processed Documents</h2>
              <ResultsPanel
                files={result.files}
                stats={result.stats}
                downloadToken={result.download_token}
              />
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

function Spinner() {
  return (
    <svg className="h-4 w-4 animate-spin" viewBox="0 0 24 24" fill="none">
      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z" />
    </svg>
  )
}
