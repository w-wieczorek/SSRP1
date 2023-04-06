module Ssrp
  extend self

  class Input
    @@words = [] of String

    def self.words
      @@words
    end
  end

  def read_data(from file_name)
    unless File.exists?(file_name)
      puts "Cannot find #{file_name}."
      exit
    end
    Input.words.concat(File.read_lines file_name)
    m = Input.words.size
    unless m > 0
      puts "At least one word is needed."
      exit
    end
    n = Input.words[0].size
    Input.words.each do |w|
      if w.size != n
        puts "Not all the strings have the same length!"
        exit
      end
    end
    {n, m}
  end

  def maximalSets(left, right, k)
    m = Input.words.size
    fam = Set(Set(Int32)).new
    if left == right
      if k == 0
        j = -1
        dict = Hash(Char, Set(Int32)).new
        (0...m).each do |i|
          ch = Input.words[i][left]
          dict[ch] ||= Set(Int32).new
          dict[ch].add(i)
        end
        dict.each_value { |s| fam.add(s) }
      else
        fam << (0...m).to_set
      end
    else
      pivot = left + (right - left)//2
      (0..k).each do |k_left|
        k_right = k - k_left
        left_fam = maximalSets left, pivot, k_left
        right_fam = maximalSets pivot+1, right, k_right
        left_fam.each do |left_set|
          right_fam.each do |right_set|
            fam.add(left_set & right_set)
          end
        end
      end
    end
    fam
  end

  def mainProcedure(file_name, k)
    puts "Loading data from #{file_name}..."
    n, m = read_data from: file_name
    puts "Read #{m} lines each of length #{n}."
    puts "Time start. Searching with Divide & conquer algorithm..."
    max_set = Set(Int32).new
    elapsed_time = Time.measure do
      sol_sets = maximalSets(0, n - 1, k)
      sol_sets.each do |sol|
        max_set = sol if sol.size > max_set.size
      end
    end
    printf "Time stop. The computations took %.2f seconds.\n", elapsed_time.total_seconds
    puts "The best solution consists of #{max_set.size} words."
    puts "String's indexes: #{max_set}"
  end
end