import React from 'react';
import Plot from 'react-plotly.js';

export default function ResultsDashboard() {
    return (
        <div className="bg-gray-100 min-h-screen p-6">
            <div className="max-w-7xl mx-auto space-y-6">

                {/* SECTION 1: Top Summary Card */}
                <div className="bg-gradient-to-r from-blue-900 to-indigo-800 text-white p-8 rounded-2xl shadow-xl flex flex-col md:flex-row justify-between items-center">
                    <div>
                        <h2 className="text-xl font-bold uppercase tracking-wider text-blue-200 mb-1">Recommended:</h2>
                        <h1 className="text-5xl font-black mb-2">Supramax</h1>
                        <p className="text-lg">Confidence: <span className="font-bold text-green-400">87%</span> | Savings: <span className="font-bold text-green-400">28%</span></p>
                    </div>
                    <div className="mt-4 md:mt-0 bg-white/20 p-4 rounded-xl text-center backdrop-blur-sm border border-white/30">
                        <p className="text-sm uppercase tracking-wide">Best Entry Window</p>
                        <p className="text-2xl font-bold">Next 7-10 days</p>
                    </div>
                </div>

                {/* SECTION 2: 50/50 Layout */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {/* LEFT COLUMN */}
                    <div className="space-y-6">
                        <div className="bg-white p-6 rounded-xl shadow">
                            <h3 className="text-lg font-bold text-gray-800 border-b pb-2 mb-4">Rate Forecast (Next 30 Days)</h3>
                            <Plot
                                data={[
                                    { x: Array.from({ length: 30 }, (_, i) => i), y: Array.from({ length: 30 }, (_, i) => 9.5 - (i * 0.02) + (Math.random() * 0.2)), type: 'scatter', name: 'Predicted High', line: { color: 'red' } },
                                    { x: Array.from({ length: 30 }, (_, i) => i), y: Array.from({ length: 30 }, (_, i) => 8.8 - (i * 0.015) + (Math.random() * 0.2)), type: 'scatter', name: 'Predicted Low', line: { color: 'green' }, fill: 'tonexty' }
                                ]}
                                layout={{ height: 280, margin: { t: 10, l: 40, r: 10, b: 30 }, xaxis: { title: 'Days' }, yaxis: { title: 'USD / ton' } }}
                                useResizeHandler={true} style={{ width: '100%' }}
                            />
                        </div>
                        <div className="bg-white p-6 rounded-xl shadow">
                            <h3 className="text-lg font-bold text-gray-800 border-b pb-2 mb-4">Port Compatibility Check</h3>
                            <div className="grid grid-cols-2 text-sm text-gray-600 mb-4">
                                <p>Destination: <span className="font-bold text-gray-900">Paradip</span></p>
                                <p>Vessel: <span className="font-bold text-gray-900">Supramax</span></p>
                            </div>
                            <ul className="space-y-2 font-mono text-sm">
                                <li className="flex text-green-700 bg-green-50 p-2 rounded">✓ Draft: 9.0m ≤ 10.5m (OK)</li>
                                <li className="flex text-green-700 bg-green-50 p-2 rounded">✓ LOA: 189m ≤ 225m (OK)</li>
                                <li className="flex text-green-700 bg-green-50 p-2 rounded">✓ Beam: 30m ≤ 32m (OK)</li>
                            </ul>
                            <div className="mt-4">
                                <p className="text-sm font-bold text-gray-700 mb-1">Compatibility Score: 98/100</p>
                                <div className="w-full bg-gray-200 rounded-full h-2.5"><div className="bg-green-600 h-2.5 rounded-full" style={{ width: '98%' }}></div></div>
                            </div>
                            <p className="mt-3 text-sm text-gray-500">Avg Turnaround: 4 days</p>
                        </div>
                    </div>

                    {/* RIGHT COLUMN */}
                    <div className="bg-white p-6 rounded-xl shadow h-full flex flex-col">
                        <h3 className="text-lg font-bold text-gray-800 border-b pb-2 mb-4">Cost Analysis & Savings</h3>
                        <div className="space-y-4 flex-grow text-gray-700 text-sm">
                            <div className="flex justify-between border-b pb-2"><span className="text-gray-500">Current Spot Price:</span> <span className="font-bold">$15.00/ton</span></div>
                            <div className="flex justify-between border-b pb-2"><span className="text-gray-500">Total Cargo:</span> <span className="font-bold">65,000 tons</span></div>
                            <div className="flex justify-between border-b pb-2 text-red-600"><span className="font-bold">Spot Cost:</span> <span className="font-black">$975,000</span></div>
                            <div className="flex justify-between border-b pb-2"><span className="text-gray-500">Forecast Price:</span> <span className="font-bold">$9.10/ton</span></div>
                            <div className="flex justify-between border-b pb-2 text-blue-600"><span className="font-bold">Predicted Freight Cost:</span> <span className="font-black">$591,500</span></div>
                            <div className="flex justify-between border-b pb-2 bg-green-50 p-2 rounded text-green-700"><span className="font-bold">Potential Savings (Freight):</span> <span className="font-black">$383,500 (39%)</span></div>
                            <div className="flex justify-between border-b pb-2"><span className="text-gray-500">Daily Operating Cost:</span> <span className="font-bold">$18,000</span></div>
                            <div className="flex justify-between border-b pb-2"><span className="text-gray-500">Days at Sea:</span> <span className="font-bold">25</span></div>
                            <div className="flex justify-between border-b pb-2"><span className="text-gray-500">Positioning Cost:</span> <span className="font-bold">$150,000</span></div>
                            <div className="flex justify-between border-b pb-2 text-indigo-700"><span className="font-bold">Total Voyage Cost:</span> <span className="font-black">$741,500</span></div>
                            <div className="flex justify-between items-center p-4 bg-green-100 rounded-lg shadow-inner mt-4 border border-green-300">
                                <span className="text-lg font-bold text-green-900">Net Savings vs Spot:</span>
                                <span className="text-2xl font-black text-green-700">$233,500 (24%)</span>
                            </div>
                        </div>
                    </div>
                </div>

                {/* SECTION 3: Vessel Comparison Table */}
                <div className="bg-white p-6 rounded-xl shadow overflow-hidden">
                    <h3 className="text-lg font-bold text-gray-800 border-b pb-2 mb-4">Vessel Comparison Table</h3>
                    <table className="w-full text-left text-sm">
                        <thead className="bg-gray-50 text-gray-600">
                            <tr>
                                <th className="px-4 py-2">Vessel Type</th><th className="px-4 py-2">Capacity</th><th className="px-4 py-2">Cost</th><th className="px-4 py-2">Score</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr className="border-b bg-green-50"><td className="px-4 py-3 font-bold text-green-800">Supramax (Recommended)</td><td className="px-4 py-3">62,000t</td><td className="px-4 py-3">$741K</td><td className="px-4 py-3 text-yellow-500">★★★★★</td></tr>
                            <tr className="border-b"><td className="px-4 py-3 font-semibold text-gray-800">Handysize</td><td className="px-4 py-3">35,000t</td><td className="px-4 py-3">$640K</td><td className="px-4 py-3 text-yellow-500">★★★★☆</td></tr>
                            <tr className="border-b"><td className="px-4 py-3 font-semibold text-gray-800">Panamax</td><td className="px-4 py-3">80,000t</td><td className="px-4 py-3">$820K</td><td className="px-4 py-3 text-yellow-500">★★★☆☆</td></tr>
                            <tr><td className="px-4 py-3 font-semibold text-red-600">Capesize (Too big)</td><td className="px-4 py-3 text-gray-500">180,000t</td><td className="px-4 py-3 text-gray-500">$1.2M</td><td className="px-4 py-3 text-yellow-500">★★☆☆☆</td></tr>
                        </tbody>
                    </table>
                </div>

                {/* SECTION 4: Action Buttons */}
                <div className="flex flex-wrap gap-4 pt-4">
                    <button className="bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-6 rounded-lg flex items-center shadow">✓ Accept Recommendation</button>
                    <button className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 px-6 rounded-lg shadow">Compare Vessels</button>
                    <button className="bg-gray-600 hover:bg-gray-700 text-white font-bold py-3 px-6 rounded-lg shadow">New Analysis</button>
                    <button className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg shadow">Export Report (PDF)</button>
                </div>
            </div>
        </div>
    );
}
