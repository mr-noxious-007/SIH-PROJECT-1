import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { TrendingUp, TrendingDown, Anchor, AlertTriangle } from 'lucide-react';

export default function Dashboard() {
    const [data, setData] = useState(null);
    const [chartData, setChartData] = useState([]);
    const [features, setFeatures] = useState([]);

    useEffect(() => {
        // Fetch dashboard stats from Backend
        axios.get('http://localhost:8000/api/dashboard')
            .then(res => setData(res.data))
            .catch(err => console.error(err));

        // Fetch chart data
        axios.get('http://localhost:8000/api/forecast/chart')
            .then(res => setChartData(res.data))
            .catch(err => console.error(err));

        axios.get('http://localhost:8000/api/features/importance')
            .then(res => setFeatures(res.data))
            .catch(err => console.error(err));
    }, []);

    if (!data) return <div className="p-10 text-center font-bold text-gray-500">Loading Market Data...</div>;

    return (
        <div className="p-8">
            <h1 className="text-3xl font-extrabold text-slate-800 mb-6">FreightIQ Control Tower</h1>

            {/* KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
                    <p className="text-sm font-medium text-gray-500 uppercase">Current Avg Freight</p>
                    <h2 className="text-3xl font-black text-slate-800 mt-2">${data.current_rate}</h2>
                    <p className="text-xs text-blue-600 mt-1 font-bold flex items-center"><TrendingUp size={14} className="mr-1" /> {data.trend} Market</p>
                </div>
                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 border-t-4 border-t-red-500">
                    <p className="text-sm font-medium text-gray-500 uppercase">30-Day Forecast</p>
                    <h2 className="text-3xl font-black text-red-600 mt-2">${data.forecast_30d}</h2>
                    <p className="text-xs text-gray-400 mt-1 font-semibold">Expected +17.6% Rise</p>
                </div>
                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
                    <p className="text-sm font-medium text-gray-500 uppercase">Paradip Congestion</p>
                    <h2 className="text-3xl font-black text-slate-800 mt-2">{data.congestion_paradip}</h2>
                    <p className="text-xs text-orange-600 mt-1 font-bold flex items-center"><AlertTriangle size={14} className="mr-1" /> Moderate Delays</p>
                </div>
                <div className="bg-gradient-to-br from-green-500 to-emerald-600 p-6 rounded-xl shadow-sm text-white">
                    <p className="text-sm font-medium text-green-100 uppercase">Estimated Savings Opp.</p>
                    <h2 className="text-3xl font-black mt-2">${data.savings_opportunity.toLocaleString()}</h2>
                    <p className="text-xs text-green-100 mt-1">vs Spot Contracts via AI Timing</p>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
                {/* Chart Section */}
                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 lg:col-span-2">
                    <h3 className="text-lg font-bold text-slate-800 mb-4">ML Freight Forecast Engine (30 Days)</h3>
                    <div className="h-80">
                        <ResponsiveContainer width="100%" height="100%">
                            <LineChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                                <CartesianGrid strokeDasharray="3 3" vertical={false} />
                                <XAxis dataKey="day" />
                                <YAxis domain={['auto', 'auto']} />
                                <Tooltip />
                                <Legend />
                                <Line type="monotone" dataKey="historical" stroke="#94a3b8" strokeWidth={3} name="Historical Trend" dot={false} />
                                <Line type="monotone" dataKey="forecast_7d" stroke="#3b82f6" strokeWidth={3} name="7-Day LSTM" activeDot={{ r: 8 }} />
                                <Line type="monotone" dataKey="forecast_14d" stroke="#8b5cf6" strokeWidth={3} name="14-Day XGBoost" />
                                <Line type="monotone" dataKey="forecast_30d" stroke="#ef4444" strokeWidth={3} name="30-Day ARIMA" />
                            </LineChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* Feature Importance & ML Risks */}
                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
                    <h3 className="text-lg font-bold text-slate-800 mb-4">XGBoost Feature Importance</h3>
                    <div className="space-y-4">
                        {features.map((f, i) => (
                            <div key={i}>
                                <div className="flex justify-between text-xs font-bold text-slate-600 mb-1">
                                    <span>{f.feature}</span>
                                    <span>{f.importance}%</span>
                                </div>
                                <div className="w-full bg-slate-100 rounded-full h-2">
                                    <div className="bg-blue-600 h-2 rounded-full" style={{ width: `${f.importance}%` }}></div>
                                </div>
                            </div>
                        ))}
                    </div>

                    <div className="mt-8 border-t pt-4">
                        <h3 className="text-sm font-bold text-slate-800 mb-2">Detected Market Risks (NLP)</h3>
                        <div className="bg-orange-50 border border-orange-200 text-orange-800 p-3 rounded text-sm mb-2 font-medium">
                            ⚠️ High congestion detected at destination ports.
                        </div>
                        <div className="bg-red-50 border border-red-200 text-red-800 p-3 rounded text-sm font-medium">
                            🚨 Freight rates expected to shock rise by 8.4% over 14 days.
                        </div>
                    </div>
                </div>
            </div>

            {/* Recommended Action */}
            <div className="bg-blue-900 border border-blue-950 p-6 rounded-xl text-white flex items-center justify-between">
                <div>
                    <h3 className="text-xs font-bold uppercase text-blue-300 tracking-wider mb-2">FreightIQ Automated Recommendation</h3>
                    <p className="text-2xl font-black mb-1">Enter 3-month multi-voyage contract immediately.</p>
                    <p className="text-blue-100 mt-2">Recommended optimized vessel class: <strong>Panamax</strong>. Expected savings vs single spot charters: <strong>$420,000</strong>.</p>
                </div>
                <div className="hidden lg:block text-5xl">⚓</div>
            </div>
        </div>
    );
}
