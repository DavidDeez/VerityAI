import Link from 'next/link'

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <h1 className="text-4xl font-bold mb-4">VerityAI</h1>
      <p className="text-lg text-gray-600 mb-8">AI Observability and Evaluation</p>
      
      <div className="flex gap-4">
        <Link href="/dashboard" className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
          Go to Dashboard
        </Link>
        <Link href="/traces" className="px-4 py-2 bg-slate-200 text-slate-800 rounded hover:bg-slate-300">
          Trace Explorer
        </Link>
      </div>
    </main>
  )
}
