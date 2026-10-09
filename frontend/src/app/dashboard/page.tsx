"use client"
import { useState, useEffect } from 'react'
import { Activity, ShieldCheck, Clock, CheckCircle2, AlertTriangle, XCircle } from 'lucide-react'

export default function Dashboard() {
  const [metrics, setMetrics] = useState<any>(null)

  useEffect(() => {
    // Simulated fetch
    setMetrics({
      reliability_score: 92.5,
      total_requests: 12450,
      success_rate: 98.2,
      average_latency: 1.2,
      total_tokens: 1543200,
      estimated_cost: 4.52,
      hallucination_rate: 3.2,
      evaluation_pass_rate: 94.1
    })
  }, [])

  if (!metrics) return (
    <div className="flex h-64 items-center justify-center text-mutedText text-sm">
      Loading analytics...
    </div>
  )

  return (
    <div className="flex flex-col gap-8 max-w-6xl">
      <header className="flex flex-col gap-1">
        <h1 className="text-2xl font-semibold tracking-tight">Overview</h1>
        <p className="text-sm text-secondaryText">Monitor reliability, performance, and evaluation outcomes across your AI systems.</p>
      </header>
      
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <MetricCard title="Total Traces" value={metrics.total_requests.toLocaleString()} />
        <MetricCard title="Eval Pass Rate" value={`${metrics.evaluation_pass_rate}%`} />
        <MetricCard title="P95 Latency" value={`${metrics.average_latency}s`} trend="-0.3s" />
        <MetricCard title="Total Cost" value={`$${metrics.estimated_cost.toFixed(2)}`} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 card p-6 flex flex-col min-h-[320px]">
          <h2 className="text-sm font-semibold mb-4 flex items-center gap-2">
            <Activity className="w-4 h-4 text-mutedText" />
            Trace Volume (7 Days)
          </h2>
          <div className="flex-1 flex items-center justify-center border border-dashed border-border rounded bg-gray-50 text-mutedText text-sm">
            Chart Visualization (Placeholder)
          </div>
        </div>

        <div className="card p-6 flex flex-col">
          <h2 className="text-sm font-semibold mb-4 flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-mutedText" />
            Security & Regressions
          </h2>
          
          <div className="flex flex-col gap-3">
            <StatusRow icon={<CheckCircle2 className="w-4 h-4 text-success" />} title="Prompt Injection" status="Secure" value="98%" />
            <StatusRow icon={<CheckCircle2 className="w-4 h-4 text-success" />} title="Data Leakage" status="Secure" value="99%" />
            <StatusRow 
              icon={<AlertTriangle className="w-4 h-4 text-warning" />} 
              title="gpt-4-turbo latency" 
              status="Warning" 
              value="2.1s" 
              isWarning
            />
            <StatusRow 
              icon={<XCircle className="w-4 h-4 text-error" />} 
              title="Agent Task Success" 
              status="Failed" 
              value="74%" 
              isError
            />
          </div>
        </div>
      </div>
    </div>
  )
}

function MetricCard({ title, value, trend }: { title: string, value: string, trend?: string }) {
  return (
    <div className="card p-5 flex flex-col justify-between">
      <h3 className="text-[13px] font-medium text-secondaryText mb-3">{title}</h3>
      <div className="flex items-baseline justify-between">
        <span className="text-2xl font-semibold tracking-tight font-mono">{value}</span>
        {trend && (
          <span className={`text-[13px] font-medium ${trend.startsWith('-') ? 'text-success' : 'text-error'}`}>
            {trend}
          </span>
        )}
      </div>
    </div>
  )
}

function StatusRow({ icon, title, status, value, isWarning, isError }: { icon: any, title: string, status: string, value: string, isWarning?: boolean, isError?: boolean }) {
  return (
    <div className="flex items-center justify-between py-2 border-b border-border last:border-0">
      <div className="flex items-center gap-3">
        {icon}
        <span className="text-sm font-medium">{title}</span>
      </div>
      <div className="flex flex-col items-end">
        <span className="text-sm font-mono font-medium">{value}</span>
        <span className="text-[11px] text-mutedText">{status}</span>
      </div>
    </div>
  )
}
