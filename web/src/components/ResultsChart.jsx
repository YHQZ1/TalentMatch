import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

const CustomTooltip = ({ active, payload }) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-white border border-slate-200 p-3 shadow-md min-w-[120px]">
        <p className="text-xs font-bold text-slate-400 uppercase mb-1">
          {payload[0].payload.name}
        </p>
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 bg-indigo-600"></div>
          <p className="text-sm font-bold text-slate-900">
            {payload[0].value}% Match
          </p>
        </div>
      </div>
    );
  }
  return null;
};

export default function ResultsChart({ results }) {
  const data = results.map((r, i) => ({
    name: r.candidate_name ? r.candidate_name.split(" ")[0] : `Cand. ${i + 1}`,
    score: r.final_score,
  }));

  return (
    <div className="bg-white border border-slate-200 h-full p-6 flex flex-col shadow-sm">
      <div className="mb-6">
        <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wide">
          Distribution
        </h2>
        <p className="text-xs text-slate-500 mt-1">
          Final match scores comparison
        </p>
      </div>

      <div className="flex-1 min-h-[250px]">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={data}
            margin={{ top: 10, right: 0, left: -20, bottom: 0 }}
          >
            <CartesianGrid
              strokeDasharray="3 3"
              stroke="#f1f5f9"
              vertical={false}
            />
            <XAxis
              dataKey="name"
              tick={{ fill: "#64748b", fontSize: 10, fontWeight: 500 }}
              axisLine={{ stroke: "#e2e8f0" }}
              tickLine={false}
              interval={0}
            />
            <YAxis
              tick={{ fill: "#64748b", fontSize: 10 }}
              axisLine={false}
              tickLine={false}
              domain={[0, 100]}
            />
            <Tooltip content={<CustomTooltip />} cursor={{ fill: "#f8fafc" }} />
            <Bar
              dataKey="score"
              fill="#4f46e5" /* Indigo-600 */
              activeBar={{ fill: "#4338ca" }}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
