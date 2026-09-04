import { useState, FormEvent } from 'react'
import { api } from '../services/api'
import { Send, CheckCircle } from 'lucide-react'

export function Contribute() {
  const [step, setStep] = useState(1)
  const [submitted, setSubmitted] = useState(false)
  const [form, setForm] = useState({
    name: '',
    email: '',
    phone: '',
    organization: '',
    document_type: '',
    title: '',
    content: '',
  })

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    api.post('/api/v1/contribute', {
      contributor: {
        name: form.name,
        email: form.email,
        phone: form.phone,
        organization: form.organization,
      },
      document_type: form.document_type,
      title: form.title,
      content: form.content,
    }).then(() => {
      setSubmitted(true)
    }).catch(() => {
      alert('Error submitting. Please try again.')
    })
  }

  if (submitted) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="card text-center max-w-md">
          <CheckCircle className="h-16 w-16 text-primary-600 mx-auto mb-4" />
          <h2 className="text-2xl font-bold mb-2">Thank You!</h2>
          <p className="text-gray-600">Your contribution has been submitted for review.</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4 max-w-2xl">
        <h1 className="text-2xl font-bold mb-6">Contribute Legal Content</h1>

        <div className="card">
          <div className="flex items-center justify-between mb-6">
            {[1, 2, 3].map((s) => (
              <div
                key={s}
                className={`w-8 h-8 rounded-full flex items-center justify-center ${
                  step >= s ? 'bg-primary-600 text-white' : 'bg-gray-200 text-gray-600'
                }`}
              >
                {s}
              </div>
            ))}
          </div>

          <form onSubmit={handleSubmit}>
            {step === 1 && (
              <div className="space-y-4">
                <h3 className="font-semibold mb-4">Your Information</h3>
                <input
                  type="text"
                  placeholder="Full Name *"
                  required
                  className="input-field"
                  value={form.name}
                  onChange={(e) => setForm({ ...form, name: e.target.value })}
                />
                <input
                  type="email"
                  placeholder="Email *"
                  required
                  className="input-field"
                  value={form.email}
                  onChange={(e) => setForm({ ...form, email: e.target.value })}
                />
                <input
                  type="tel"
                  placeholder="Phone (optional)"
                  className="input-field"
                  value={form.phone}
                  onChange={(e) => setForm({ ...form, phone: e.target.value })}
                />
                <input
                  type="text"
                  placeholder="Organization (optional)"
                  className="input-field"
                  value={form.organization}
                  onChange={(e) => setForm({ ...form, organization: e.target.value })}
                />
              </div>
            )}

            {step === 2 && (
              <div className="space-y-4">
                <h3 className="font-semibold mb-4">Document Details</h3>
                <select
                  className="input-field"
                  value={form.document_type}
                  onChange={(e) => setForm({ ...form, document_type: e.target.value })}
                >
                  <option value="">Select Document Type</option>
                  <option value="federal_act">Federal Act</option>
                  <option value="provincial_act">Provincial Act</option>
                  <option value="ordinance">Ordinance</option>
                  <option value="rules">Rules</option>
                  <option value="notification">Notification</option>
                </select>
                <input
                  type="text"
                  placeholder="Title *"
                  required
                  className="input-field"
                  value={form.title}
                  onChange={(e) => setForm({ ...form, title: e.target.value })}
                />
              </div>
            )}

            {step === 3 && (
              <div className="space-y-4">
                <h3 className="font-semibold mb-4">Content</h3>
                <textarea
                  placeholder="Paste the legal text or describe the law..."
                  rows={10}
                  className="input-field"
                  value={form.content}
                  onChange={(e) => setForm({ ...form, content: e.target.value })}
                />
              </div>
            )}

            <div className="flex justify-between mt-6">
              {step > 1 && (
                <button
                  type="button"
                  onClick={() => setStep(step - 1)}
                  className="btn-secondary"
                >
                  Back
                </button>
              )}
              {step < 3 ? (
                <button
                  type="button"
                  onClick={() => setStep(step + 1)}
                  className="btn-primary ml-auto"
                >
                  Next
                </button>
              ) : (
                <button type="submit" className="btn-primary ml-auto flex items-center">
                  <Send className="h-4 w-4 mr-2" /> Submit
                </button>
              )}
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}
