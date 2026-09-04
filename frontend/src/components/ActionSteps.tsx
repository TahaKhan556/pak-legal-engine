import { CheckCircle } from 'lucide-react'

interface ActionStepsProps {
  steps: string[]
}

export function ActionSteps({ steps }: ActionStepsProps) {
  return (
    <ol className="space-y-3">
      {steps.map((step, index) => (
        <li key={index} className="flex items-start gap-3">
          <CheckCircle className="h-5 w-5 text-primary-600 mt-0.5 flex-shrink-0" />
          <span className="text-gray-700">{step}</span>
        </li>
      ))}
    </ol>
  )
}
