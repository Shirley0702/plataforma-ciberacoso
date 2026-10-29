export interface DiagnosticOption {
  id: number
  label: string
}

export interface DiagnosticQuestion {
  id: number
  text: string
  options: DiagnosticOption[]
}
