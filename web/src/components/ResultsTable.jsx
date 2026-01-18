import { useState, useMemo } from "react";

export default function ResultsTable({ results }) {
  const [expandedRows, setExpandedRows] = useState({});

  // ✅ SORT DESCENDING BY MATCH SCORE
  const sortedResults = useMemo(() => {
    return [...results].sort((a, b) => b.final_score - a.final_score);
  }, [results]);

  function toggleRow(idx) {
    setExpandedRows((prev) => ({ ...prev, [idx]: !prev[idx] }));
  }

  return (
    <div className="bg-white border border-slate-200 shadow-sm flex flex-col">
      {/* Header */}
      <div className="p-6 border-b border-slate-100">
        <h2 className="text-sm font-bold text-slate-900 uppercase tracking-wide">
          Candidate Rankings
        </h2>
        <p className="text-xs text-slate-500 mt-1">
          Sorted by Match Score (highest first)
        </p>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="min-w-[1500px] w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-50 border-b border-slate-200 text-xs font-bold text-slate-500 uppercase tracking-wider">
              <th className="py-3 px-4 w-16">Rank</th>

              {/* Sticky Candidate */}
              <th className="py-3 px-4 sticky left-0 bg-slate-50 z-20">
                Candidate
              </th>

              <th className="py-3 px-4">Match %</th>
              <th className="py-3 px-4">ATS %</th>
              <th className="py-3 px-4">Skills Match</th>
              <th className="py-3 px-4">Experience</th>
              <th className="py-3 px-4">Matched Skills</th>
              <th className="py-3 px-4">Skills Score</th>
              <th className="py-3 px-4">Exp Score</th>
              <th className="py-3 px-4">Edu Score</th>
              <th className="py-3 px-4">Relevance</th>
            </tr>
          </thead>

          <tbody className="divide-y divide-slate-100">
            {sortedResults.map((r, i) => {
              const isExpanded = expandedRows[i];
              const visibleSkills = isExpanded
                ? r.matched_skills
                : r.matched_skills.slice(0, 4);

              return (
                <tr key={i} className="hover:bg-slate-50 transition-colors">
                  {/* Rank */}
                  <td className="py-4 px-4">
                    <div
                      className={`w-7 h-7 flex items-center justify-center text-xs font-bold rounded
                        ${
                          i === 0
                            ? "bg-indigo-100 text-indigo-700"
                            : "bg-slate-100 text-slate-600"
                        }`}
                    >
                      {i + 1}
                    </div>
                  </td>

                  {/* Candidate (sticky) */}
                  <td className="py-4 px-4 sticky left-0 bg-white z-10">
                    <div className="font-semibold text-slate-900 text-sm">
                      {r.candidate_name ?? `Candidate ${i + 1}`}
                    </div>
                    <div className="text-xs text-slate-400">
                      ATS: {r.ats_score}%
                    </div>
                  </td>

                  {/* Match Score */}
                  <td className="py-4 px-4 font-bold text-slate-900">
                    {r.final_score}%
                  </td>

                  {/* ATS */}
                  <td className="py-4 px-4 text-sm">{r.ats_score}%</td>

                  {/* Skills Match Count */}
                  <td className="py-4 px-4 text-sm">
                    {r.matched_skills_count}
                  </td>

                  {/* Experience */}
                  <td className="py-4 px-4 text-sm">{r.experience}</td>

                  {/* Matched Skills */}
                  <td className="py-4 px-4">
                    <div className="flex flex-wrap gap-1.5">
                      {visibleSkills.map((skill, idx) => (
                        <span
                          key={idx}
                          className="px-2 py-1 bg-white border border-slate-200 text-xs text-slate-600 font-medium rounded"
                        >
                          {skill}
                        </span>
                      ))}

                      {r.matched_skills.length > 4 && !isExpanded && (
                        <button
                          onClick={() => toggleRow(i)}
                          className="px-2 py-1 bg-slate-100 text-xs text-slate-500 rounded hover:bg-slate-200"
                        >
                          +{r.matched_skills.length - 4} more
                        </button>
                      )}

                      {isExpanded && (
                        <button
                          onClick={() => toggleRow(i)}
                          className="px-2 py-1 bg-slate-100 text-xs text-slate-500 rounded hover:bg-slate-200"
                        >
                          Show less
                        </button>
                      )}
                    </div>
                  </td>

                  {/* Component Scores */}
                  <td className="py-4 px-4 text-sm">{r.skills_score}</td>
                  <td className="py-4 px-4 text-sm">{r.exp_score}</td>
                  <td className="py-4 px-4 text-sm">{r.edu_score}</td>
                  <td className="py-4 px-4 text-sm">{r.relevance_score}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
