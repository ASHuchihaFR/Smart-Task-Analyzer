import React, { useState } from "react";
import { TrendingUp, Calendar, Clock } from "lucide-react";

const TaskAnalyzer = () => {
  const [tasks, setTasks] = useState([]);
  const [analyzedTasks, setAnalyzedTasks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [apiConnected, setApiConnected] = useState(false);

  const [formData, setFormData] = useState({
    title: "",
    due_date: "",
    estimated_hours: 1,
    importance: 5,
  });

  // ADD TASK (WORKING PERFECTLY)
  const handleSubmit = () => {
    if (!formData.title || !formData.due_date) {
      alert("Please enter a title and due date.");
      return;
    }

    const newTask = {
      ...formData,
      id: Date.now(),
      estimated_hours: parseFloat(formData.estimated_hours),
      importance: parseInt(formData.importance),
    };

    setTasks([...tasks, newTask]); // Instantly adds to UI
    setFormData({ title: "", due_date: "", estimated_hours: 1, importance: 5 });
  };

  // ANALYZE - BACKEND API
  const analyzeTasks = async () => {
    if (tasks.length === 0) {
      alert("⚠ Add tasks before analyzing!");
      return;
    }

    setLoading(true);
    try {
      const response = await fetch("http://127.0.0.1:8000/api/prioritize/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(tasks),
      });

      if (!response.ok) throw new Error("API Error");
      const data = await response.json();

      setAnalyzedTasks(data.tasks || data);
      setApiConnected(true);
    } catch (error) {
      alert("⚠ Backend not responding, using local scoring.");
      setApiConnected(false);

      const localScored = tasks.map((t) => ({
        ...t,
        priority_score:
          t.importance * 8 + // more impact from importance
          (10 - t.estimated_hours) * 2 + // lower effort = better
          (t.due_date ? 10 : 0), // bonus for deadline
      }));

      setAnalyzedTasks(localScored.sort((a, b) => b.priority_score - a.priority_score));
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="max-w-5xl mx-auto">

        {/* HEADER */}
        <div className="bg-white rounded-lg shadow p-6 mb-6 text-center">
          <h1 className="text-4xl font-bold text-gray-800 flex justify-center gap-2 items-center">
            <TrendingUp className="w-8 h-8 text-indigo-600" />
            Smart Task Analyzer
          </h1>
          <p className="text-gray-600 mt-1">
            Analyze urgency, importance, effort & productivity value.
          </p>
        </div>

        {/* MAIN LAYOUT */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

          {/* ADD TASK */}
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-4">➕ Add Task</h2>
            <input
              className="w-full p-2 border rounded mb-3"
              placeholder="Task Title"
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            />
            <input
              type="date"
              className="w-full p-2 border rounded mb-3"
              value={formData.due_date}
              onChange={(e) => setFormData({ ...formData, due_date: e.target.value })}
            />
            <input
              type="number"
              min="1"
              className="w-full p-2 border rounded mb-3"
              value={formData.estimated_hours}
              onChange={(e) => setFormData({ ...formData, estimated_hours: e.target.value })}
            />
            <p>Importance: {formData.importance}/10</p>
            <input
              type="range"
              min="1"
              max="10"
              className="w-full mb-4"
              value={formData.importance}
              onChange={(e) => setFormData({ ...formData, importance: e.target.value })}
            />
            <button
              onClick={handleSubmit}
              className="w-full bg-indigo-600 text-white py-2 rounded-lg hover:bg-indigo-700"
            >
              Add Task
            </button>

            <button
              onClick={analyzeTasks}
              disabled={loading}
              className="w-full bg-purple-600 text-white py-2 mt-3 rounded-lg hover:bg-purple-700"
            >
              {loading ? "Analyzing..." : "Analyze Tasks (via API)"}
            </button>
          </div>

          {/* RESULT PANEL */}
          <div className="md:col-span-2 bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-2">📊 Prioritized Tasks</h2>

            {apiConnected ? (
              <p className="text-green-600 text-sm mb-2">✔ Backend API Connected</p>
            ) : (
              <p className="text-red-600 text-sm mb-2">⚠ Local Scoring Used</p>
            )}

            {analyzedTasks.length === 0 ? (
              <p className="text-gray-500">No tasks analyzed yet</p>
            ) : (
              analyzedTasks.map((task, idx) => (
                <div key={task.id} className="p-4 border rounded-lg mb-2 flex justify-between">
                  <div>
                    <h3 className="font-bold">{idx + 1}. {task.title}</h3>
                    <p className="text-sm text-gray-600 flex gap-1">
                      <Calendar className="w-4 h-4" /> {task.due_date}
                    </p>
                    <p className="text-sm text-gray-600 flex gap-1">
                      <Clock className="w-4 h-4" /> {task.estimated_hours}h effort
                    </p>
                  </div>
                  <div className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-lg font-bold">
                    {task.priority_score?.toFixed(1)}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default TaskAnalyzer;
