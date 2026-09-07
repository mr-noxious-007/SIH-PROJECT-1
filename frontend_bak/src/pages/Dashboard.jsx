import React from 'react';

export default function Dashboard() {
    return (
        <div className="min-h-screen bg-gray-50 flex flex-col items-center">
            {/* Hero Section */}
            <div className="w-full bg-blue-900 text-white py-16 px-6 text-center shadow-lg">
                <h1 className="text-4xl md:text-5xl font-extrabold mb-4">Freight Rate Forecasting System</h1>
                <p className="text-xl md:text-2xl font-light mb-8 text-blue-200">Smart vessel chartering for India's East Coast</p>
                <button className="bg-green-500 hover:bg-green-600 text-white text-lg font-bold py-3 px-8 rounded-full shadow-lg transition transform hover:-translate-y-1">
                    Start Analysis
                </button>
            </div>

            <div className="max-w-6xl w-full px-6 py-12">
                {/* 3 Quick Stats Cards */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
                    <div className="bg-white p-6 rounded-xl shadow border-l-4 border-blue-500">
                        <h3 className="text-gray-500 uppercase text-sm font-bold tracking-wider mb-2">Total Routes Tracked</h3>
                        <p className="text-4xl font-black text-gray-800">12</p>
                    </div>
                    <div className="bg-white p-6 rounded-xl shadow border-l-4 border-indigo-500">
                        <h3 className="text-gray-500 uppercase text-sm font-bold tracking-wider mb-2">Avg Forecast Accuracy</h3>
                        <p className="text-4xl font-black text-gray-800">87%</p>
                    </div>
                    <div className="bg-white p-6 rounded-xl shadow border-l-4 border-green-500">
                        <h3 className="text-gray-500 uppercase text-sm font-bold tracking-wider mb-2">Potential Savings</h3>
                        <p className="text-4xl font-black text-green-600">28-35%</p>
                    </div>
                </div>

                {/* Recent Activity Table */}
                <div className="bg-white rounded-xl shadow-md overflow-hidden">
                    <div className="px-6 py-4 border-b border-gray-200 bg-gray-50">
                        <h2 className="text-xl font-bold text-gray-800">Recent Activity</h2>
                    </div>
                    <div className="overflow-x-auto">
                        <table className="w-full text-left text-gray-600">
                            <thead className="bg-gray-100 text-gray-500 text-sm uppercase">
                                <tr>
                                    <th className="px-6 py-3">Date</th>
                                    <th className="px-6 py-3">Origin</th>
                                    <th className="px-6 py-3">Destination</th>
                                    <th className="px-6 py-3">Recommendation</th>
                                    <th className="px-6 py-3">Savings</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr className="border-b hover:bg-gray-50">
                                    <td className="px-6 py-4">2024-06-25</td>
                                    <td className="px-6 py-4">Australia</td>
                                    <td className="px-6 py-4">Paradip</td>
                                    <td className="px-6 py-4 font-semibold text-blue-600">Supramax</td>
                                    <td className="px-6 py-4 font-bold text-green-600">$233,500</td>
                                </tr>
                                <tr className="border-b hover:bg-gray-50">
                                    <td className="px-6 py-4">2024-06-24</td>
                                    <td className="px-6 py-4">Mozambique</td>
                                    <td className="px-6 py-4">Vizag</td>
                                    <td className="px-6 py-4 font-semibold text-blue-600">Panamax</td>
                                    <td className="px-6 py-4 font-bold text-green-600">$180,000</td>
                                </tr>
                                <tr className="border-b hover:bg-gray-50">
                                    <td className="px-6 py-4">2024-06-23</td>
                                    <td className="px-6 py-4">US</td>
                                    <td className="px-6 py-4">Haldia</td>
                                    <td className="px-6 py-4 font-semibold text-blue-600">Handysize</td>
                                    <td className="px-6 py-4 font-bold text-green-600">$45,000</td>
                                </tr>
                                <tr className="border-b hover:bg-gray-50">
                                    <td className="px-6 py-4">2024-06-22</td>
                                    <td className="px-6 py-4">Indonesia</td>
                                    <td className="px-6 py-4">Gopalpur</td>
                                    <td className="px-6 py-4 font-semibold text-blue-600">Handysize</td>
                                    <td className="px-6 py-4 font-bold text-green-600">$12,500</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    );
}

