"use client"
import { useState, useEffect } from 'react'
import { Search, Filter, Clock, CheckCircle2, XCircle, MoreHorizontal } from 'lucide-react'

export default function TraceExplorer() {
  const [traces, setTraces] = useState<any[]>([])

  useEffect(() => {
    setTraces([
      {
        id: "trc_9a8b7c6d5e",
        model: "gpt-4-turbo",
        status: "success",
        latency: 1.24,
        total_tokens: 450,
        input: "Extract the names and organizations...",
        timestamp: new Date(Date.now() - 1000 * 60 * 5).toISOString()
      },
      {
        id: "trc_3f2e1d0c9b",
        model: "llama-3-8b-instruct",
        status: "error",
        latency: 0.42,
        total_tokens: 120,
        input: "Write a SQL query to find...",
        timestamp: new Date(Date.now() - 1000 * 60 * 15).toISOString()
      },
      {
        id: "trc_1a2b3c4d5e",
        model: "gpt-3.5-turbo",
        status: "success",
        latency: 0.89,
        total_tokens: 890,
        input: "Translate the following document...",
        timestamp: new Date(Date.now() - 1000 * 60 * 45).toISOString()
      }
    ])
  }, [])

  return (
    <div className="flex flex-col gap-6 max-w-7xl h-full">
      <header className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Traces</h1>
          <p className="text-sm text-secondaryText mt-1">Explore and debug individual model executions.</p>
        </div>
      </header>
      
      <div className="card flex flex-col flex-1 min-h-0 overflow-hidden">
        {/* Toolbar */}
        <div className="px-4 py-3 border-b border-border flex items-center justify-between bg-gray-50/50">
          <div className="flex items-center gap-3">
            <div className="relative w-72">
              <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 w-4 h-4 text-mutedText" />
              <input 
                type="text" 
                placeholder="Search trace ID or content..." 
                className="input-field pl-9 h-8 bg-white"
              />
            </div>
            <button className="btn-secondary h-8 px-3 text-[13px] gap-2">
              <Filter className="w-3.5 h-3.5" />
              Filter
            </button>
          </div>
          <div className="text-[13px] text-mutedText font-medium">
            Showing {traces.length} traces
          </div>
        </div>

        {/* Table */}
        <div className="flex-1 overflow-auto">
          <table className="w-full text-left border-collapse">
            <thead className="bg-gray-50/80 text-[11px] font-semibold text-mutedText uppercase tracking-wider sticky top-0 backdrop-blur-sm z-10 border-b border-border">
              <tr>
                <th className="px-4 py-3 font-medium">Trace ID</th>
                <th className="px-4 py-3 font-medium">Time</th>
                <th className="px-4 py-3 font-medium">Model</th>
                <th className="px-4 py-3 font-medium text-right">Latency</th>
                <th className="px-4 py-3 font-medium text-right">Tokens</th>
                <th className="px-4 py-3 font-medium">Status</th>
                <th className="px-4 py-3 font-medium w-10"></th>
              </tr>
            </thead>
            <tbody className="text-[13px] divide-y divide-border">
              {traces.map(trace => (
                <tr key={trace.id} className="hover:bg-gray-50/50 group cursor-pointer transition-colors">
                  <td className="px-4 py-3">
                    <span className="font-mono text-primaryText font-medium">{trace.id}</span>
                  </td>
                  <td className="px-4 py-3 text-secondaryText flex items-center gap-1.5">
                    <Clock className="w-3.5 h-3.5 text-mutedText" />
                    {new Date(trace.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit', second:'2-digit'})}
                  </td>
                  <td className="px-4 py-3">
                    <span className="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-medium bg-gray-100 text-gray-700 border border-gray-200">
                      {trace.model}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-right font-mono text-secondaryText">
                    {trace.latency.toFixed(2)}s
                  </td>
                  <td className="px-4 py-3 text-right font-mono text-secondaryText">
                    {trace.total_tokens}
                  </td>
                  <td className="px-4 py-3">
                    {trace.status === 'success' ? (
                      <span className="flex items-center gap-1.5 text-success font-medium">
                        <CheckCircle2 className="w-4 h-4" />
                        Success
                      </span>
                    ) : (
                      <span className="flex items-center gap-1.5 text-error font-medium">
                        <XCircle className="w-4 h-4" />
                        Error
                      </span>
                    )}
                  </td>
                  <td className="px-4 py-3 text-right">
                    <button className="text-mutedText hover:text-primaryText opacity-0 group-hover:opacity-100 transition-opacity">
                      <MoreHorizontal className="w-4 h-4" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
