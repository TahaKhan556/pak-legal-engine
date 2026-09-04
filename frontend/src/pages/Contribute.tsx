import { useState, FormEvent } from 'react'
import { api } from '../services/api'
import { Send, CheckCircle, ArrowLeft, ArrowRight } from 'lucide-react'

export function Contribute() {
  const [step, setStep] = useState(1)
  const [submitted, setSubmitted] = useState(false)
  const [form, setForm] = useState({
    name: '', email: '', phone: '', organization: '',
    document_type: '', title: '', content: '',
  })

  const update = (field: string, value: string) => setForm({ ...form, [field]: value })

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    api.post('/api/v1/contribute', {
      contributor: { name: form.name, email: form.email, phone: form.phone, organization: form.organization },
      document_type: form.document_type,
      title: form.title,
      content: form.content,
    }).then(() => setSubmitted(true))
      .catch(() => alert('Error submitting. Please try again.'))
  }

  if (submitted) {
    return (
      <div className="min-h-screen bg-kanun-50/50 flex items-center justify-center px-4">
        <div className="card text-center max-w-md">
          <div className="w-16 h-16 bg-kanun-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <CheckCircle className="h-8 w-8 text-kanun-600" />
          </div>
          <h2 className="text-xl font-bold text-gray-900 mb-2">Thank You!</h2>
          <p className="text-gray-500 mb-6">Your contribution has been submitted for review.</p>
          <button onClick={() => { setSubmitted(false); setStep(1); setForm({ name: '', email: '', phone: '', organization: '', document_type: '', title: '', content: '' }); }} className="btn-primary">
            Submit Another
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-kanun-50/50 py-8">
      <div className="max-w-2xl mx-auto px-4">
        <h1 className="text-heading text-gray-900 mb-2">Contribute Legal Content</h1>
        <p className="text-gray-500 mb-6">Help expand the legal database for all Pakistanis.</p>

        <div className="flex items-center gap-3 mb-8">
          {[1, 2, 3].map((s) => (
            <div key={s} className="flex items-center gap-3 flex-1">
              <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 transition-all ${
                step > s ? 'bg-kanun-600 text-white' : step === s ? 'bg-kanun-700 text-white ring-4 ring-kanun-100' : 'bg-gray-200 text-gray-500'
              }`}>
                {step > s ? <CheckCircle className="h-4 w-4" /> : <span className="text-sm font-bold">{s}</span>}
              </div>
              {s < 3 && <div className={`flex-1 h-0.5 ${step > s ? 'bg-kanun-600' : 'bg-gray-200'}`}></div>}
            </div>
          ))}
        </div>

        <div className="card">
          <form onSubmit={handleSubmit}>
            {step === 1 && (
              <div className="space-y-4">
                <h3 className="font-semibold text-gray-900 mb-4">Your Information</h3>
                <input type="text" placeholder="Full Name *" required className="input-field" value={form.name} onChange={(e) => update('name', e.target.value)} />
                <input type="email" placeholder="Email *" required className="input-field" value={form.email} onChange={(e) => update('email', e.target.value)} />
                <input type="tel" placeholder="Phone (optional)" className="input-field" value={form.phone} onChange={(e) => update('phone', e.target.value)} />
                <input type="text" placeholder="Organization (optional)" className="input-field" value={form.organization} onChange={(e) => update('organization', e.target.value)} />
              </div>
            )}
            {step === 2 && (
              <div className="space-y-4">
                <h3 className="font-semibold text-gray-900 mb-4">Document Details</h3>
                <select className="input-field" value={form.document_type} onChange={(e) => update('document_type', e.target.value)}>
                  <option value="">Select Document Type</option>
                  <option value="federal_act">Federal Act</option>
                  <option value="provincial_act">Provincial Act</option>
                  <option value="ordinance">Ordinance</option>
                  <option value="rules">Rules</option>
                  <option value="notification">Notification</option>
                </select>
                <input type="text" placeholder="Title *" required className="input-field" value={form.title} onChange={(e) => update('title', e.target.value)} />
              </div>
            )}
            {step === 3 && (
              <div className="space-y-4">
                <h3 className="font-semibold text-gray-900 mb-4">Content</h3>
                <textarea placeholder="Paste the legal text or describe the law..." rows={10} className="input-field resize-none" value={form.content} onChange={(e) => update('content', e.target.value)} />
              </div>
            )}

            <div className="flex justify-between mt-6 pt-4 border-t border-gray-100">
              {step > 1 ? (
                <button type="button" onClick={() => setStep(step - 1)} className="btn-secondary">
                  <ArrowLeft className="h-4 w-4" /> Back
                </button>
              ) : <div />}
              {step < 3 ? (
                <button type="button" onClick={() => setStep(step + 1)} className="btn-primary">
                  Next <ArrowRight className="h-4 w-4" />
                </button>
              ) : (
                <button type="submit" className="btn-primary">
                  <Send className="h-4 w-4" /> Submit
                </button>
              )}
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}
