require "./spec_helper"

describe Ssrp do
  it "reads strings from file" do
    Ssrp::Input.words.clear
    n, m = Ssrp.read_data from: "words_060_0060_20_0.083.dat"
    n.should eq(60)
    m.should eq(60)
    Ssrp::Input.words[49].should eq("MLCPMBFMCEEMAMMLODTTLMRBRFIHTQMAGQGKOPEGQNGDFDAHEABCCSPLSOHB")
  end

  it "finds largest indistinguishable substrings set" do
    Ssrp::Input.words.clear
    Ssrp::Input.words << "QMAEQGKOFEGQNGD"
    Ssrp::Input.words << "QMAEQLPOFEGQNGD"
    Ssrp::Input.words << "BMAEQMKOFEGQNMD"
    Ssrp::Input.words << "QJAENGKOFEGQNGD"
    max_set = Set(Int32).new
    sol_sets = Ssrp.maximalSets(0, 14, 4)
    sol_sets.each do |sol|
      max_set = sol if sol.size > max_set.size
    end
    max_set.size.should eq(3)
  end
end
