import React, { useState, useEffect } from 'react';
import { Toaster, toast } from 'react-hot-toast';
import { Plus, Trash2, Download, CheckSquare, Square } from 'lucide-react';

const API_BASE = 'http://localhost:8000/api';

interface Generation {
  id: string;
  positive_prompt: string;
  negative_prompt: string;
  final_title: string;
  cards: any;
  created_at: string;
}

function App() {
  const [title, setTitle] = useState('');
  const [about, setAbout] = useState('');
  const [desc, setDesc] = useState('');
  const [imageUrl, setImageUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState<Generation[]>([]);
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [output, setOutput] = useState<any>(null);

  useEffect(() => { loadHistory(); }, []);

  const loadHistory = async () => {
    try {
      const res = await fetch(`${API_BASE}/history`);
      const data = await res.json();
      setHistory(data.history || []);
    } catch (e) { console.error(e); }
  };
  const handleGenerate = async () => {
    if (!title.trim()) { toast.error('Enter product title'); return; }
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          product_title: title,
          about_this_product: about,
          product_description: desc,
          image_url: imageUrl
        })
      });
      const data = await res.json();
      setOutput(data);
      toast.success('Generated!');
      await loadHistory();
    } catch (e) { toast.error('Failed'); }
    finally { setLoading(false); }
  };

  const handleDelete = async () => {
    if (selected.size === 0) { toast.error('No items selected'); return; }
    for (const id of selected) {
      await fetch(`${API_BASE}/history/${id}`, { method: 'DELETE' });
    }
    setSelected(new Set());
    await loadHistory();
    toast.success(`Deleted ${selected.size} items`);
  };

  const handleDeleteAll = async () => {
    await fetch(`${API_BASE}/history`, { method: 'DELETE' });
    setSelected(new Set());
    await loadHistory();
    toast.success('All deleted');
  };

  const handleExport = () => {
    const data = history.filter(h => selected.has(h.id));
    if (data.length === 0) { toast.error('Nothing selected'); return; }
    const csv = ['ID,Timestamp,Title', ...data.map(h =>
      `${h.id},${new Date(h.created_at).toLocaleString()},${h.final_title}`
    )].join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `prompts_${Date.now()}.csv`;
    a.click();
    URL.revokeObjectURL(url);
    toast.success('Exported');
  };

  const toggleSelect = (id: string) => {
    const newSet = new Set(selected);
    if (newSet.has(id)) newSet.delete(id);
    else newSet.add(id);
    setSelected(newSet);
  };

  const toggleAll = () => {
    if (selected.size === history.length) setSelected(new Set());
    else setSelected(new Set(history.map(h => h.id)));
  };
  return (
    <div className="min-h-screen bg-dark text-white">
      <Toaster position="top-right" />
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        <h1 className="text-4xl font-bold text-primary text-center mb-8">
          🎬 TikTok-Prompt-Generator v4.0
        </h1>

        <div className="bg-card rounded-lg p-6 mb-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <input type="text" value={title} onChange={e => setTitle(e.target.value)}
              placeholder="Product Title *" className="px-3 py-2 bg-dark border border-gray-700 rounded-lg" />
            <input type="text" value={imageUrl} onChange={e => setImageUrl(e.target.value)}
              placeholder="Image URL" className="px-3 py-2 bg-dark border border-gray-700 rounded-lg" />
          </div>
          <textarea value={about} onChange={e => setAbout(e.target.value)}
            placeholder="About This Product" rows={2}
            className="w-full px-3 py-2 bg-dark border border-gray-700 rounded-lg mb-4" />
          <textarea value={desc} onChange={e => setDesc(e.target.value)}
            placeholder="Product Description" rows={3}
            className="w-full px-3 py-2 bg-dark border border-gray-700 rounded-lg mb-4" />
          <button onClick={handleGenerate} disabled={loading}
            className="w-full bg-primary hover:bg-orange-600 py-3 rounded-lg flex items-center justify-center gap-2">
            <Plus size={20} /> {loading ? 'Generating...' : 'Generate Prompt'}
          </button>
        </div>

        {output && (
          <div className="bg-card rounded-lg p-6 mb-8">
            <h2 className="text-xl font-semibold text-primary mb-4">Generated Output</h2>
            <div className="bg-dark p-3 rounded-lg mb-2"><strong>Final Title:</strong> {output.final_title}</div>
            <details className="bg-dark rounded-lg">
              <summary className="cursor-pointer p-3">View Full Prompt</summary>
              <pre className="p-3 text-sm overflow-x-auto">{output.positive_prompt}</pre>
            </details>
          </div>
        )}
        <div className="bg-card rounded-lg p-6">
          <div className="flex justify-between items-center mb-4 flex-wrap gap-2">
            <h2 className="text-xl font-semibold text-primary">History</h2>
            <div className="flex gap-2">
              <button onClick={handleExport} disabled={selected.size === 0}
                className="px-4 py-2 bg-green-600 rounded-lg disabled:opacity-50 flex gap-2"><Download size={16} /> Export</button>
              {selected.size > 0 && (
                <button onClick={handleDelete} className="px-4 py-2 bg-red-600 rounded-lg flex gap-2"><Trash2 size={16} /> Delete ({selected.size})</button>
              )}
              {history.length > 0 && (
                <button onClick={handleDeleteAll} className="px-4 py-2 bg-red-600/50 rounded-lg flex gap-2">Delete All</button>
              )}
            </div>
          </div>

          {history.length === 0 ? <div className="text-center text-gray-400 py-8">No history yet</div> : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-700">
                    <th className="py-3 px-2 w-12">
                      <button onClick={toggleAll} className="hover:text-primary">
                        {selected.size === history.length ? <CheckSquare size={18} /> : <Square size={18} />}
                      </button>
                    </th>
                    <th className="text-left py-3 px-2">Title</th>
                    <th className="text-left py-3 px-2">Date</th>
                    <th className="text-left py-3 px-2">Preview</th>
                  </tr>
                </thead>
                <tbody>
                  {history.map(item => (
                    <tr key={item.id} className="border-b border-gray-800">
                      <td className="py-3 px-2">
                        <button onClick={() => toggleSelect(item.id)}>{selected.has(item.id) ? <CheckSquare size={18} /> : <Square size={18} />}</button>
                      </td>
                      <td className="py-3 px-2">{item.final_title.substring(0, 50)}...</td>
                      <td className="py-3 px-2 text-sm">{new Date(item.created_at).toLocaleDateString()}</td>
                      <td className="py-3 px-2">
                        <details><summary className="text-primary text-sm cursor-pointer">View</summary>
                          <pre className="mt-2 p-2 bg-dark rounded text-xs">{item.positive_prompt.substring(0, 150)}...</pre>
                        </details>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
