using Serilog;
using System.Text;
using static System.Environment;

namespace Bb4Ssrp
{
    public static class InputData
    {
        public static string[] words = { };
        public static string alphabet = "";
        public static int m = 0;  // the size of a word
        public static int n = 0;  // the number of words
        public static int k = 2;  // the number of columns to remove

        public static void readData(string fileName)
        {
            try
            {
                words = File.ReadAllLines(fileName);
            }
            catch (Exception ex)
            {
                Log.Error("There is a problem with file {A}:", fileName);
                Log.Error("{A} says {B}", ex.GetType(), ex.Message);
                Exit(1);
            }
            n = words.Length;
            if (n == 0)
            {
                Log.Error("There are no words in file {A}.", fileName);
                Exit(1);
            }
            m = words[0].Length;
            Log.Debug("The length of the first word is {A}.", m);
            foreach (string w in words)
            {
                if (w.Length != m)
                {
                    Log.Error("Not all the strings have the same length!");
                    Exit(1);
                }
                foreach (char symbol in w)
                {
                    if (!alphabet.Contains(symbol))
                    {
                        alphabet += symbol;
                    }
                }
            }

        }

        public static int[] determineWordIndices(int[] arrOfCols)
        {
            Dictionary<string, HashSet<int>> result = new();
            var columns = arrOfCols.ToHashSet();
            for (int i = 0; i < n; i++)
            {
                StringBuilder str = new();
                for (int j = 0; j < m; j++)
                {
                    if (!columns.Contains(j))
                    {
                        str.Append(words[i][j]);
                    }
                }
                var s = str.ToString();
                if (!result.ContainsKey(s))
                {
                    result.Add(s, new HashSet<int>());
                }
                result[s].Add(i);
            }
            var (w, inds) = result.MaxBy(entry => entry.Value.Count);
            return inds.ToArray();
        }

        public static int determineWordSetSize(HashSet<int> columns)
        {
            Dictionary<string, int> result = new();
            for (int i = 0; i < n; i++)
            {
                StringBuilder str = new();
                for (int j = 0; j < m; j++)
                {
                    if (!columns.Contains(j))
                    {
                        str.Append(words[i][j]);
                    }
                }
                var s = str.ToString();
                if (!result.ContainsKey(s))
                {
                    result.Add(s, 0);
                }
                ++result[s];
            }
            var (_, size) = result.MaxBy(entry => entry.Value);
            return size;
        }
    }
}
