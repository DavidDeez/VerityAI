"use client"
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { 
  LayoutDashboard, 
  Activity, 
  Database, 
  GitCompare, 
  ShieldCheck, 
  Settings, 
  FileCode,
  Box,
  Key
} from 'lucide-react'
import clsx from 'clsx'

export default function Sidebar() {
  const pathname = usePathname()

  const navGroups = [
    {
      title: "OBSERVABILITY",
      items: [
        { name: "Overview", href: "/dashboard", icon: LayoutDashboard },
        { name: "Traces", href: "/traces", icon: Activity },
      ]
    },
    {
      title: "EVALUATION",
      items: [
        { name: "Datasets", href: "/datasets", icon: Database },
        { name: "Evaluations", href: "/evaluations", icon: FileCode },
        { name: "Benchmarks", href: "/benchmarks", icon: GitCompare },
      ]
    },
    {
      title: "AI SECURITY",
      items: [
        { name: "Security Tests", href: "/security", icon: ShieldCheck },
      ]
    },
    {
      title: "DEVELOPER TOOLS",
      items: [
        { name: "API Keys", href: "/keys", icon: Key },
      ]
    }
  ]

  return (
    <aside className="w-[240px] flex-shrink-0 bg-sidebar border-r border-border flex flex-col h-full hidden md:flex">
      <div className="h-14 flex items-center px-6 border-b border-border">
        <div className="flex items-center gap-2">
          <Box className="w-5 h-5 text-accent" />
          <span className="font-semibold text-primaryText tracking-tight">VerityAI</span>
        </div>
      </div>
      
      <div className="px-4 py-4 flex flex-col gap-6 flex-1 overflow-y-auto">
        {navGroups.map(group => (
          <div key={group.title}>
            <div className="text-[11px] font-semibold text-mutedText tracking-wider mb-2 px-2">
              {group.title}
            </div>
            <div className="flex flex-col gap-0.5">
              {group.items.map(item => {
                const isActive = pathname.startsWith(item.href)
                return (
                  <Link 
                    key={item.name} 
                    href={item.href}
                    className={clsx(
                      "flex items-center gap-3 px-2 py-1.5 rounded-md text-sm transition-colors",
                      isActive 
                        ? "bg-white text-accent font-medium shadow-subtle border border-gray-100" 
                        : "text-secondaryText hover:text-primaryText hover:bg-gray-100 border border-transparent"
                    )}
                  >
                    <item.icon className={clsx("w-4 h-4", isActive ? "text-accent" : "text-mutedText")} />
                    {item.name}
                  </Link>
                )
              })}
            </div>
          </div>
        ))}
      </div>

      <div className="p-4 border-t border-border">
        <Link href="/settings" className="flex items-center gap-3 px-2 py-1.5 rounded-md text-sm text-secondaryText hover:text-primaryText hover:bg-gray-100 transition-colors">
          <Settings className="w-4 h-4 text-mutedText" />
          Settings
        </Link>
      </div>
    </aside>
  )
}
