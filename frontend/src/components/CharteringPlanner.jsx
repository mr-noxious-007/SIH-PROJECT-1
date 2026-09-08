import React, { useState } from 'react';
import axios from 'axios';
import { Ship, CheckCircle, XCircle } from 'lucide-react';

export default function CharteringPlanner() {
    const [formData, setFormData] = useState({
        commodity: "Coal",
        cargo_quantity: 70000,
        origin: "Australia",
        loading_port: "Newcastle",
        destination: "Paradip",
        contract_type: "Multi-voyage",
        voyages: 4
    });

    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleSubmit = (e) => {
        e.preventDefault();
        setLoading(true);
        axios.post('http://localhost:8000/api/chartering/recommend', formData)
            .then(res => {
                setResult(res.data);
                setLoading(false);
            })
            .catch(err => {
                alert("Error contacting backend running on port 8000. Is Uvicorn running?");
                setLoading(false);
            });
    };

    return (
        <div className="p-8">
            <h1 className="text-3xl font-extrabold text-slate-800 mb-6">Chartering Planner</h1>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* FORM */}
                <div className="bg-white p-8 rounded-xl shadow-sm border border-gray-200">
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label className="block text-sm font-semibold mb-1">Commodity</label>
                                <input type="text" className="w-full border p-2.5 rounded-lg bg-gray-50 focus:ring-2 focus:ring-blue-500" value={formData.commodity} onChange={e => setFormData({ ...formData, commodity: e.target.value })} />
                            </div>
                            <div>
                                <label className="block text-sm font-semibold mb-1">Cargo Quantity (Tonnes)</label>
                                <input type="number" className="w-full border p-2.5 rounded-lg bg-gray-50 focus:ring-2 focus:ring-blue-500" value={formData.cargo_quantity} onChange={e => setFormData({ ...formData, cargo_quantity: Number(e.target.value) })} />
                            </div>
                            <div>
                                <label className="block text-sm font-semibold mb-1">Loading Port (Origin)</label>
                                <select className="w-full border p-2.5 rounded-lg bg-gray-50 focus:ring-2 focus:ring-blue-500" value={formData.loading_port} onChange={e => setFormData({ ...formData, loading_port: e.target.value })}>
                                    <option>Newcastle</option><option>Port Hedland</option><option>Hampton Roads</option><option>Maputo</option><option>Taboneo</option>
                                </select>
                            </div>
                            <div>
                                <label className="block text-sm font-semibold mb-1">Destination Port (India)</label>
                                <select className="w-full border p-2.5 rounded-lg bg-gray-50 focus:ring-2 focus:ring-blue-500" value={formData.destination} onChange={e => setFormData({ ...formData, destination: e.target.value })}>
                                    <option>Paradip</option><option>Visakhapatnam</option><option>Gangavaram</option><option>Haldia</option>
                                </select>
                            </div>
                            <div>
                                <label className="block text-sm font-semibold mb-1">Contract Strategy</label>
                                <select className="w-full border p-2.5 rounded-lg bg-gray-50 focus:ring-2 focus:ring-blue-500" value={formData.contract_type} onChange={e => setFormData({ ...formData, contract_type: e.target.value })}>
                                    <option>Spot</option>
                                    <option>Short-term</option>
                                    <option>Multi-voyage</option>
                                </select>
                            </div>
                            <div>
                                <label className="block text-sm font-semibold mb-1">Number of Voyages</label>
                                <input type="number" className="w-full border p-2.5 rounded-lg bg-gray-50 focus:ring-2 focus:ring-blue-500" value={formData.voyages} onChange={e => setFormData({ ...formData, voyages: Number(e.target.value) })} />
                            </div>
                        </div>
                        <button type="submit" disabled={loading} className="w-full mt-6 bg-slate-900 hover:bg-slate-800 text-white font-bold p-4 rounded-lg shadow-lg transition flex items-center justify-center">
                            {loading ? "ANALYZING..." : "GENERATE CHARTERING RECOMMENDATION"}
                        </button>
                    </form>
                </div>

                {/* RESULTS */}
                {result && (
                    <div className="bg-gradient-to-b from-blue-900 to-slate-900 p-8 rounded-xl shadow-2xl text-white">
                        <h2 className="text-xl uppercase font-bold tracking-wider text-blue-300 mb-6 border-b border-blue-700 pb-3 flex items-center">
                            <Ship className="mr-2" /> AI Chartering Recommendation
                        </h2>

                        <div className="space-y-4">
                            <div className="flex justify-between items-center bg-blue-800/30 p-4 rounded-lg border border-blue-600/30">
                                <span className="text-blue-100 font-medium tracking-wide text-sm uppercase">Recommended Vessel Type</span>
                                <span className="text-3xl font-black text-white">{result.recommended_vessel_type}</span>
                            </div>

                            <div className="flex justify-between items-center pb-2 border-b border-blue-800/50">
                                <span className="text-gray-300">Market Entry Timing:</span>
                                <span className="font-bold text-red-300 animate-pulse">{result.entry_recommendation}</span>
                            </div>

                            <div className="flex justify-between items-center pb-2 border-b border-blue-800/50">
                                <span className="text-gray-300">Confidence Metric:</span>
                                <span className="font-bold text-emerald-400">{result.confidence_percent}%</span>
                            </div>

                            <div className="grid grid-cols-2 gap-4">
                                <div className="bg-black/30 p-4 rounded-lg">
                                    <p className="text-xs text-gray-400 mb-1">Weather Risk</p>
                                    <p className="text-lg font-bold">{result.features?.weather_risk_index?.value || "N/A"}</p>
                                    <p className="text-[10px] text-gray-500 mt-1 uppercase text-right border-t border-gray-700 pt-1">
                                        {result.features?.weather_risk_index?.status} - {result.features?.weather_risk_index?.source}
                                    </p>
                                </div>
                                <div className="bg-black/30 p-4 rounded-lg">
                                    <p className="text-xs text-gray-400 mb-1">Port Congestion (Dest)</p>
                                    <p className="text-lg font-bold">{result.features?.port_congestion_index?.value}%</p>
                                    <p className="text-[10px] text-gray-500 mt-1 uppercase text-right border-t border-gray-700 pt-1">
                                        {result.features?.port_congestion_index?.status} - {result.features?.port_congestion_index?.source}
                                    </p>
                                </div>
                            </div>

                            <div className="grid grid-cols-2 gap-4">
                                <div className="bg-black/30 p-4 rounded-lg">
                                    <p className="text-xs text-gray-400 mb-1">Global GDP Data</p>
                                    <p className="text-lg font-bold">{result.features?.global_gdp_growth?.value}% Growth</p>
                                    <p className="text-[10px] text-gray-500 mt-1 uppercase text-right border-t border-gray-700 pt-1">
                                        {result.features?.global_gdp_growth?.status} - {result.features?.global_gdp_growth?.source}
                                    </p>
                                </div>
                            </div>

                            <div className="bg-gradient-to-r from-emerald-600 to-green-600 border border-green-500 p-6 rounded-xl my-4 text-center shadow-lg">
                                <p className="text-sm text-green-100 uppercase tracking-widest mb-1">Est. Voyage Cost (Powered by live Fuel Price proxies)</p>
                                <p className="text-5xl font-black text-white">${(result.total_voyage_cost_usd || 0).toLocaleString()}</p>
                                <p className="text-xs text-green-200 mt-2">Fuel calculation methodology based on {result.voyage_details?.cost_source}</p>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
