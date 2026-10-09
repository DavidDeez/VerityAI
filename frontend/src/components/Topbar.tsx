"use client"
import { Search, Bell, ChevronDown } from 'lucide-react'

export default function Topbar() {
  return (
    <header className="h-14 flex-shrink-0 bg-surface border-b border-border flex items-center justify-between px-6">
      <div className="flex items-center gap-4 flex-1">
        <div className="relative w-64">
          <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 w-4 h-4 text-mutedText" />
          <input 
            type="text" 
            placeholder="Search traces, evaluations..." 
            className="input-field pl-9 h-8 bg-gray-50 focus:bg-white"
          />
        </div>
      </div>
      
      <div className="flex items-center gap-4">
        <div className="text-sm font-medium text-secondaryText flex items-center gap-1 cursor-pointer hover:text-primaryText">
          Project: default-env
          <ChevronDown className="w-3 h-3" />
        </div>
        <div className="w-px h-4 bg-border"></div>
        <button className="text-mutedText hover:text-primaryText transition-colors">
          <Bell className="w-4 h-4" />
        </button>
        <div className="w-7 h-7 rounded-full bg-accent text-white flex items-center justify-center text-xs font-semibold">
          JD
        </div>
      </div>
    </header>
  )
}
