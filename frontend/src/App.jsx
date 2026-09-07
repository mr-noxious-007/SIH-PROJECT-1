import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import CharteringPlanner from './components/CharteringPlanner';
import { Ship, LayoutDashboard } from 'lucide-react';

export default function App() {
    return (
        <Router>
            <div className="flex h-screen bg-gray-100 font-sans">
                {/* Sidebar */}
                <div className="w-64 bg-slate-900 text-white flex flex-col">
                    <div className="p-6 font-black text-2xl tracking-widest text-blue-400 border-b border-slate-700 flex items-center">
                        <Ship className="mr-3" /> FreightIQ
                    </div>
                    <nav className="flex-1 p-4 space-y-2">
                        <Link to="/" className="flex items-center p-3 rounded hover:bg-slate-800 transition text-sm font-medium">
                            <LayoutDashboard size={18} className="mr-2" />
                            Control Tower
                        </Link>
                        <Link to="/planner" className="flex items-center p-3 rounded hover:bg-slate-800 transition text-sm font-medium">
                            <Ship size={18} className="mr-2" />
                            Chartering Planner
                        </Link>
                    </nav>
                    <div className="p-4 bg-slate-800 text-xs text-slate-400">
                        Smart India Hackathon 2026<br />
                        Local Demo Environment
                    </div>
                </div>
                {/* Main Content */}
                <div className="flex-1 overflow-auto">
                    <Routes>
                        <Route path="/" element={<Dashboard />} />
                        <Route path="/planner" element={<CharteringPlanner />} />
                    </Routes>
                </div>
            </div>
        </Router>
    );
}
