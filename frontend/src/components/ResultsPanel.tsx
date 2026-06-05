import type { ProcessedFile, ProcessingStats } from '../types'

interface Props {
  files: ProcessedFile[]
  stats: ProcessingStats
  downloadToken: string
}

const FOLDER_LABELS: Record<string, string> = {
  '01_Contract': 'Contract',
  '02_Disclosures': 'Disclosures',
  '03_Inspections': 'Inspections',
  '04_Financing': 'Financing',
  '05_Title_Escrow': 'Title & Escrow',
  '06_HOA': 'HOA',
  '07_Misc': 'Misc',
}

const CONFIDENCE_STYLES: Record<string, string> = {
  high: 'bg-emerald-100 text-emerald-700',
  medium: 'bg-amber-100 text-amber-700',
  low: 'bg-slate-100 text-slate-500',
}

const FOLDER_COLORS: Record<string, string> = {
  '01_Contract': 'bg-blue-100 text-blue-700',
  '02_Disclosures': 'bg-purple-100 text-purple-700',
  '03_Inspections': 'bg-orange-100 text-orange-700',
  '04_Financing': 'bg-green-100 text-green-700',
  '05_Title_Escrow': 'bg-cyan-100 text-cyan-700',
  '06_HOA': 'bg-pink-100 text-pink-700',
  '07_Misc': 'bg-slate-100 text-slate-600',
}

export default function ResultsPanel({ files, stats, downloadToken }: Props) {
  const grouped = groupByFolder(files)

  return (
    <div className="space-y-6">
      {/* Stats bar */}
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
        <Stat label="Files uploaded" value={stats.total_uploaded} />
        <Stat label="Documents out" value={stats.total_output} />
        <Stat label="Packets split" value={stats.splits_performed} />
        <Stat label="OCR applied" value={stats.ocr_applied} />
      </div>

      {/* Download button */}
      <a
        href={`/api/download/${downloadToken}`}
        download="transaction_files.zip"
        className="flex w-full items-center justify-center gap-2 rounded-lg bg-brand-600 px-4 py-3 text-sm font-semibold text-white shadow-sm hover:bg-brand-700 transition-colors"
      >
        <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" />
        </svg>
        Download Organized ZIP
      </a>

      {/* File list grouped by folder */}
      {Object.entries(grouped).map(([folder, folderFiles]) => (
        <div key={folder}>
          <div className="mb-2 flex items-center gap-2">
            <span className={`rounded px-2 py-0.5 text-xs font-semibold ${FOLDER_COLORS[folder] ?? 'bg-slate-100 text-slate-600'}`}>
              {folder}
            </span>
            <span className="text-xs text-slate-400">{FOLDER_LABELS[folder] ?? folder}</span>
          </div>
          <ul className="space-y-1.5">
            {folderFiles.map((f, i) => (
              <FileRow key={i} file={f} />
            ))}
          </ul>
        </div>
      ))}
    </div>
  )
}

function FileRow({ file }: { file: ProcessedFile }) {
  return (
    <li className={`flex items-start gap-3 rounded-lg border px-3 py-2.5 ${file.error ? 'border-amber-200 bg-amber-50' : 'border-slate-200 bg-white'}`}>
      <div className={`mt-0.5 shrink-0 rounded p-1 ${file.error ? 'bg-amber-100' : 'bg-slate-100'}`}>
        <svg className={`h-3.5 w-3.5 ${file.error ? 'text-amber-500' : 'text-slate-500'}`} viewBox="0 0 16 16" fill="currentColor">
          <path d="M4 1.75A.75.75 0 014.75 1h4.69a.75.75 0 01.53.22l3.06 3.06a.75.75 0 01.22.53V13.25A.75.75 0 0112.5 14h-7.75A.75.75 0 014 13.25V1.75z" />
        </svg>
      </div>
      <div className="min-w-0 flex-1">
        <div className="flex items-center gap-2 flex-wrap">
          <span className="text-sm font-medium text-slate-800 truncate">{file.new_name}</span>
          {file.error ? (
            <span className="rounded bg-amber-100 px-1.5 py-0.5 text-xs font-medium text-amber-700">
              partial
            </span>
          ) : (
            <span className={`rounded px-1.5 py-0.5 text-xs font-medium ${CONFIDENCE_STYLES[file.confidence]}`}>
              {file.confidence}
            </span>
          )}
          {file.was_ocr && (
            <span className="rounded bg-violet-100 px-1.5 py-0.5 text-xs font-medium text-violet-700">
              OCR
            </span>
          )}
        </div>
        <p className="mt-0.5 text-xs text-slate-400 truncate">
          From: {file.original_name} · {file.pages}p · {file.doc_type_display}
        </p>
        {file.error && (
          <p className="mt-0.5 text-xs text-amber-600 truncate">
            {file.error}
          </p>
        )}
      </div>
    </li>
  )
}

function Stat({ label, value }: { label: string; value: number }) {
  return (
    <div className="rounded-lg border border-slate-200 bg-white px-4 py-3 text-center">
      <p className="text-2xl font-bold text-brand-600">{value}</p>
      <p className="mt-0.5 text-xs text-slate-500">{label}</p>
    </div>
  )
}

function groupByFolder(files: ProcessedFile[]): Record<string, ProcessedFile[]> {
  const order = ['01_Contract', '02_Disclosures', '03_Inspections', '04_Financing', '05_Title_Escrow', '06_HOA', '07_Misc']
  const result: Record<string, ProcessedFile[]> = {}
  for (const folder of order) {
    const group = files.filter((f) => f.folder === folder)
    if (group.length > 0) result[folder] = group
  }
  return result
}
