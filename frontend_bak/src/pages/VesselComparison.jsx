import React from 'react';

export default function VesselComparison() {
    return (
        <div className="min-h-screen bg-gray-50 p-6 md:p-12">
            <h1 className="text-3xl font-extrabold text-gray-800 mb-8 border-b pb-4">Vessel Class Comparison & Compatibility</h1>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
                {/* Column 1: Supramax */}
                <div className="bg-white p-8 rounded-2xl shadow-lg border-t-8 border-green-500">
                    <h2 className="text-2xl font-black text-gray-900 mb-4">Supramax 🏆</h2>
                    <ul className="space-y-3 text-gray-700">
                        <li className="flex justify-between border-b pb-1"><span>Capacity:</span> <span className="font-bold">62,000 tons</span></li>
                        <li className="flex justify-between border-b pb-1"><span>Draft:</span> <span className="font-bold">9.0m</span></li>
                        <li className="flex justify-between border-b pb-1"><span>LOA:</span> <span className="font-bold">189m</span></li>
                        <li className="flex justify-between border-b pb-1 border-gray-400"><span>Daily Cost (Opex):</span> <span className="font-bold">$18,000</span></li>
                        <li className="flex justify-between border-b pb-1 text-red-600"><span>Fuel / day:</span> <span className="font-bold">38 tons</span></li>
                        <li className="pt-2 text-indigo-700 bg-indigo-50 p-2 rounded text-sm"><strong>Suitable for:</strong> All ports except Haldia</li>
                    </ul>
                    <div className="mt-6 flex divide-x">
                        <div className="w-1/2 pr-4 text-green-700"><p className="text-xs font-bold uppercase mb-1">Pros</p><p className="text-sm">Good balance, very fuel efficient for Indian East Coast.</p></div>
                        <div className="w-1/2 pl-4 text-red-700"><p className="text-xs font-bold uppercase mb-1">Cons</p><p className="text-sm">Draft slightly too deep for minor ports like Haldia.</p></div>
                    </div>
                </div>

                {/* Column 2: Handysize */}
                <div className="bg-white p-8 rounded-2xl shadow-lg border-t-8 border-blue-500">
                    <h2 className="text-2xl font-black text-gray-900 mb-4">Handysize</h2>
                    <ul className="space-y-3 text-gray-700">
                        <li className="flex justify-between border-b pb-1"><span>Capacity:</span> <span className="font-bold">35,000 tons</span></li>
                        <li className="flex justify-between border-b pb-1"><span>Draft:</span> <span className="font-bold">8.2m</span></li>
                        <li className="flex justify-between border-b pb-1"><span>LOA:</span> <span className="font-bold">178m</span></li>
                        <li className="flex justify-between border-b pb-1 border-gray-400"><span>Daily Cost (Opex):</span> <span className="font-bold">$14,000</span></li>
                        <li className="flex justify-between border-b pb-1 text-red-600"><span>Fuel / day:</span> <span className="font-bold">28 tons</span></li>
                        <li className="pt-2 text-green-700 bg-green-50 p-2 rounded text-sm"><strong>Suitable for:</strong> All ports including Haldia</li>
                    </ul>
                    <div className="mt-6 flex divide-x">
                        <div className="w-1/2 pr-4 text-green-700"><p className="text-xs font-bold uppercase mb-1">Pros</p><p className="text-sm">Lowest cost, unrestricted all-port coastal access.</p></div>
                        <div className="w-1/2 pl-4 text-red-700"><p className="text-xs font-bold uppercase mb-1">Cons</p><p className="text-sm">Smaller capacity; needs 2 trips for loads &gt; 40k tons.</p></div>
                    </div>
                </div>
            </div>

            <div className="bg-white p-6 rounded-2xl shadow-md overflow-x-auto">
                <h3 className="text-xl font-bold mb-4 text-gray-800">Complete Master Specifications</h3>
                <table className="w-full text-left text-sm text-gray-600">
                    <thead className="bg-gray-100 text-gray-700">
                        <tr><th className="p-3">Vessel Class</th><th className="p-3">Typ. Capacity</th><th className="p-3">Draft (m)</th><th className="p-3">LOA (m)</th><th className="p-3">Beam (m)</th><th className="p-3">Cost/Day</th><th className="p-3">Fuel (t/d)</th></tr>
                    </thead>
                    <tbody>
                        <tr className="border-b"><td className="p-3 font-bold">Handysize</td><td className="p-3">35,000</td><td className="p-3">8.2</td><td className="p-3">178</td><td className="p-3">26</td><td className="p-3">$14,000</td><td className="p-3">28</td></tr>
                        <tr className="border-b bg-green-50"><td className="p-3 font-bold text-green-900">Supramax</td><td className="p-3">62,000</td><td className="p-3">9.0</td><td className="p-3">189</td><td className="p-3">30</td><td className="p-3">$18,000</td><td className="p-3">38</td></tr>
                        <tr className="border-b"><td className="p-3 font-bold">Panamax</td><td className="p-3">80,000</td><td className="p-3">10.5</td><td className="p-3">225</td><td className="p-3">32</td><td className="p-3">$24,000</td><td className="p-3">52</td></tr>
                        <tr className=""><td className="p-3 font-bold">Capesize</td><td className="p-3">180,000</td><td className="p-3">14.0</td><td className="p-3">289</td><td className="p-3">45</td><td className="p-3">$38,000</td><td className="p-3">95</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
    );
}
