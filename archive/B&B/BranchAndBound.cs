using Serilog;
using System.Diagnostics;

namespace Bb4Ssrp
{
    public interface ISolution
    {
        float bound();
        bool isComplete(out int size);
        List<ISolution> sons();
    }

    public static class BranchAndBound
    {
        public static ISolution? Run(ISolution initial, out bool optimal, int? timeLimit = null)
        {
            Stopwatch stopwatch = new();
            stopwatch.Start();
            int timeElapsed = 0;
            float best_profit = 0.0f;
            ISolution? best_solution = null;
            // PriorityQueue<ISolution, float> Z = new(Comparer<float>.Create((x, y) => x > y ? -1 : 1));
            // Z.Enqueue(initial, initial.bound());
            Stack<(ISolution, float)> Z = new();
            Z.Push((initial, initial.bound()));
            UInt64 iteration = 0;
            Log.Debug("Iteration   Incubent      Bound");
            while (Z.Count > 0 && (timeLimit is null || timeElapsed < timeLimit))
            {
                ++iteration;
                ISolution w;
                float w_bound;
                // Z.TryDequeue(out w, out w_bound);
                (w, w_bound) = Z.Pop();
                // Log.Debug($"w_bound = {w_bound}, solution = {w}");
                if (w_bound > best_profit)
                {
                    List<ISolution> candidates = w.sons();
                    foreach (ISolution c in candidates)
                    {
                        float c_bound = c.bound();
                        if (c_bound > best_profit)
                        {
                            int actual_size;
                            if (c.isComplete(out actual_size) && actual_size > best_profit)
                            {
                                best_profit = actual_size;
                                best_solution = c;
                            }
                            else
                            {
                                // Z.Enqueue(c, c_bound);
                                Z.Push((c, c_bound));
                            }
                        }
                    }
                }
                timeElapsed = (int)stopwatch.Elapsed.TotalSeconds;
                if (iteration % 50 == 0)
                {
                    float? incubent = best_solution is null ? null : best_profit;
                    Log.Debug($"{iteration}: {incubent} {w_bound}");
                }
            }
            stopwatch.Stop();
            optimal = Z.Count == 0;
            return best_solution;
        }
    }
}
