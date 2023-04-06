using CommandLine;
using Serilog;
using System.Collections.Immutable;
using System.Text;

namespace Bb4Ssrp
{
    public class Options
    {
        [Option('f', "file", Required = true, HelpText = "The name of a file including strings.")]
        public string? fileName { get; set; }

        [Option('k', "knum", Required = true, HelpText = "The number of columns to remove.")]
        public int kNum { get; set; }

        [Option('t', "time", Default = 30, HelpText = "(Default: 30 seconds) time limit.")]
        public int timeLimit { get; set; }

        [Option('l', "log-level", Default = "debug", HelpText = "debug, info, or error.")]
        public string? logLevel { get; set; }
    }

    class Solution : ISolution
    {
        private ImmutableList<int> columns;
        private ImmutableList<int> indices;
        private float? _bound;
        private List<ISolution>? _sons;

        public Solution(ImmutableList<int> _columns, ImmutableList<int> _indices)
        {
            columns = _columns;
            indices = _indices;
            _bound = null;
            _sons = null;
        }

        public float bound()
        {
            if (_bound is not null) { return (float)_bound; }
            int total = 0;
            for (int i = 0; i < InputData.n; ++i)
            {
                if (!indices.Contains(i))
                {
                    bool i_is_good = true;
                    foreach (int j in indices)
                    {
                        int count = 0;
                        for (int pos = 0; pos < InputData.m; ++pos)
                        {
                            if (!columns.Contains(pos))
                            {
                                if (InputData.words[i][pos] != InputData.words[j][pos]) 
                                    ++count;
                            }
                        }
                        if (columns.Count + count > InputData.k)
                        {
                            i_is_good = false;
                            break;
                        }
                    }
                    if (i_is_good) ++total;
                }
            }
            total += indices.Count;
            _bound = total;
            return total;
        }

        public bool isComplete(out int size)
        {
            sons();
            size = indices.Count;
            return _sons!.Count() == 0;
        }

        public List<ISolution> sons()
        {
            if (_sons is not null) { return _sons; }
            List<ISolution> sons = new();
            int last_idx = indices.Count > 0 ? indices.Last() : -1;
            for (int i = last_idx + 1; i < InputData.n; ++i)
            {
                bool i_is_good = true;
                HashSet<int> must_be_removed = new();
                foreach (int j in indices)
                {
                    for (int pos = 0; pos < InputData.m; ++pos)
                    {
                        if (InputData.words[i][pos] != InputData.words[j][pos])
                            must_be_removed.Add(pos);
                    }
                    if (must_be_removed.Count > InputData.k)
                    {
                        i_is_good = false;
                        break;
                    }
                }
                if (i_is_good)
                {
                    sons.Add(new Solution(must_be_removed.ToImmutableList(), indices.Add(i)));
                }
            }
            _sons = sons;
            return sons;
        }

        public int[] toArrOfCols()
        {
            return columns.ToArray();
        }

        public override string ToString()
        {
            StringBuilder sb = new();
            sb.Append($"{indices} {columns}");
            return sb.ToString();
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            Parser.Default.ParseArguments<Options>(args).WithParsed(o =>
            {
                switch (o.logLevel)
                {
                    case "debug":
                        Log.Logger = new LoggerConfiguration()
                            .MinimumLevel.Debug()
                            .WriteTo.Console()
                            .CreateLogger();
                        break;
                    case "error":
                        Log.Logger = new LoggerConfiguration()
                            .MinimumLevel.Error()
                            .WriteTo.Console()
                            .CreateLogger();
                        break;
                    default:
                        Log.Logger = new LoggerConfiguration()
                            .MinimumLevel.Information()
                            .WriteTo.Console()
                            .CreateLogger();
                        break;
                }
                Log.Debug("File name is {A}.", o.fileName);
                Log.Debug("K-number is = {A}.", o.kNum);
                Log.Information("Loading data from {A}...", o.fileName);
                InputData.readData(o.fileName);
                InputData.k = o.kNum;
                Log.Information("Read {A} lines each of length {B}.", InputData.n, InputData.m);
                Log.Debug("{A}[s] set for time limit.", o.timeLimit);
                bool optimal;
                Solution root = new(
                    _columns: ImmutableList.Create<int>(), 
                    _indices: ImmutableList.Create<int>()
                );
                Log.Debug("Branch and bound for SSRP has just started...");
                var sol = (Solution?)BranchAndBound.Run(root, out optimal, o.timeLimit);
                if (sol is not null)
                {
                    int[] resInds = InputData.determineWordIndices(sol.toArrOfCols()); 
                    Log.Information("The best solution consists of {A} words.", resInds.Length);
                    Log.Information("String's indexes: {A}", resInds);
                    if (optimal)
                    {
                        Log.Information("The result is optimal.");
                    }
                }
                else
                {
                    Log.Information("No solution found within the given time limit.");
                }
            });
        }
    }
}
