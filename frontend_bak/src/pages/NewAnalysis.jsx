import React, { useState } from 'react';

export default function NewAnalysis() {
    const [formData, setFormData] = useState({ duration: 90 });

    const handleSubmit = (e) => {
        e.preventDefault();
        alert("Running analysis for: " + JSON.stringify(formData));
    };

    return (
        <div className="min-h-screen bg-gray-100 flex items-center justify-center py-12">
            <div className="bg-white shadow-2xl rounded-2xl w-full" style={{ maxWidth: '600px', padding: '40px' }}>
                <h2 className="text-3xl font-extrabold text-gray-900 mb-8 text-center border-b pb-4">
                    Get Freight Rate Forecast & Recommendations
                </h2>
                <form onSubmit={handleSubmit} className="space-y-6">
                    <div className="grid grid-cols-2 gap-6">
                        <div>
                            <label className="block text-sm font-semibold text-gray-700">Select Cargo Type</label>
                            <select className="mt-1 w-full bg-gray-50 border border-gray-300 rounded-lg p-2.5">
                                <option>Coal</option><option>Iron Ore</option><option>Grain</option><option>Other</option>
                            </select>
                        </div>
                        <div>
                            <label className="block text-sm font-semibold text-gray-700">Cargo Volume (tons)</label>
                            <input type="number" min="1000" max="500000" placeholder="e.g., 65000" className="mt-1 w-full bg-gray-50 border border-gray-300 rounded-lg p-2.5" />
                        </div>
                    </div>

                    <div className="grid grid-cols-2 gap-6">
                        <div>
                            <label className="block text-sm font-semibold text-gray-700">Origin Port</label>
                            <select className="mt-1 w-full bg-gray-50 border border-gray-300 rounded-lg p-2.5">
                                <option>Australia</option><option>US</option><option>Mozambique</option><option>Indonesia</option><option>Russia</option>
                            </select>
                        </div>
                        <div>
                            <label className="block text-sm font-semibold text-gray-700">Destination Port (India)</label>
                            <select className="mt-1 w-full bg-gray-50 border border-gray-300 rounded-lg p-2.5">
                                <option>Paradip</option><option>Vizag</option><option>Gangavaram</option><option>Gopalpur</option><option>Dhamra</option><option>Haldia</option>
                            </select>
                        </div>
                    </div>

                    <div className="grid grid-cols-2 gap-6">
                        <div>
                            <label className="block text-sm font-semibold text-gray-700">Preferred Vessel (Optional)</label>
                            <select className="mt-1 w-full bg-gray-50 border border-gray-300 rounded-lg p-2.5">
                                <option>Any</option><option>Handysize</option><option>Supramax</option><option>Panamax</option><option>Capesize</option>
                            </select>
                        </div>
                        <div>
                            <label className="block text-sm font-semibold text-gray-700">Budget (USD)</label>
                            <input type="number" placeholder="e.g., 2500000" className="mt-1 w-full bg-gray-50 border border-gray-300 rounded-lg p-2.5" />
                        </div>
                    </div>

                    <div>
                        <label className="block text-sm font-semibold text-gray-700">Contract Duration (days): {formData.duration}</label>
                        <input type="range" min="30" max="365" value={formData.duration} onChange={(e) => setFormData({ ...formData, duration: e.target.value })} className="w-full mt-2" />
                    </div>

                    <div>
                        <label className="block text-sm font-semibold text-gray-700">Special Notes</label>
                        <textarea placeholder="Any specific requirements..." rows="3" className="mt-1 w-full bg-gray-50 border border-gray-300 rounded-lg p-2.5"></textarea>
                    </div>

                    <button type="submit" className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-4 rounded-xl text-lg transition shadow-lg flex items-center justify-center">
                        <span className="mr-2">🔍</span> Analyze & Get Recommendations
                    </button>
                </form>
            </div>
        </div>
    );
}
