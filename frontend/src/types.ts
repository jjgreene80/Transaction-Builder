export interface ProcessedFile {
  original_name: string
  new_name: string
  doc_type: string
  doc_type_display: string
  folder: string
  pages: number
  was_ocr: boolean
  confidence: 'high' | 'medium' | 'low'
  error: string | null
}

export interface MissingDoc {
  key: string
  display: string
}

export interface ProcessingStats {
  total_uploaded: number
  total_output: number
  splits_performed: number
  ocr_applied: number
}

export interface ProcessingResult {
  files: ProcessedFile[]
  missing_docs: MissingDoc[]
  download_token: string
  stats: ProcessingStats
}
