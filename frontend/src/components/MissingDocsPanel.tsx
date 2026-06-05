import type { MissingDoc } from '../types'

interface Props {
  missing: MissingDoc[]
}

export default function MissingDocsPanel({ missing }: Props) {
  if (missing.length === 0) {
    return (
      <div className="flex items-center gap-3 rounded-lg border border-emerald-200 bg-emerald-50 px-4 py-3">
        <svg className="h-5 w-5 shrink-0 text-emerald-500" viewBox="0 0 20 20" fill="currentColor">
          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z" clipRule="evenodd" />
        </svg>
        <div>
          <p className="text-sm font-semibold text-emerald-800">All required documents present</p>
          <p className="text-xs text-emerald-600">File is ready for broker review.</p>
        </div>
      </div>
    )
  }

  return (
    <div className="rounded-lg border border-red-200 bg-red-50">
      <div className="flex items-center gap-3 border-b border-red-200 px-4 py-3">
        <svg className="h-5 w-5 shrink-0 text-red-500" viewBox="0 0 20 20" fill="currentColor">
          <path fillRule="evenodd" d="M8.485 2.495c.673-1.167 2.357-1.167 3.03 0l6.28 10.875c.673 1.167-.17 2.625-1.516 2.625H3.72c-1.347 0-2.189-1.458-1.515-2.625L8.485 2.495zM10 5a.75.75 0 01.75.75v3.5a.75.75 0 01-1.5 0v-3.5A.75.75 0 0110 5zm0 9a1 1 0 100-2 1 1 0 000 2z" clipRule="evenodd" />
        </svg>
        <p className="text-sm font-semibold text-red-800">
          {missing.length} required document{missing.length !== 1 ? 's' : ''} missing
        </p>
      </div>
      <ul className="divide-y divide-red-100">
        {missing.map((doc) => (
          <li key={doc.key} className="flex items-center gap-2 px-4 py-2">
            <svg className="h-3.5 w-3.5 shrink-0 text-red-400" viewBox="0 0 16 16" fill="currentColor">
              <path d="M8 1a7 7 0 100 14A7 7 0 008 1zm-.75 4.75a.75.75 0 011.5 0v3.5a.75.75 0 01-1.5 0v-3.5zm.75 7a.75.75 0 110-1.5.75.75 0 010 1.5z" />
            </svg>
            <span className="text-sm text-red-700">{doc.display}</span>
          </li>
        ))}
      </ul>
      <div className="px-4 py-2.5">
        <p className="text-xs text-red-500">Obtain missing documents before submitting for broker review.</p>
      </div>
    </div>
  )
}
