package ssrp

import io.jenetics.BitChromosome
import org.scalatest.funspec.AnyFunSpec

class GeneticAlgorithmSpec extends AnyFunSpec {
  describe("GeneticAlgorithm") {
    it("Counts columns to remove") {
      val words = Array("QMAEQGKOFEGQNGD", "QMAEQLPOFEGQNGD",
        "BMAEQMKOFEGQNMD", "AQJAENGKOAAAAGA", "QJAENGKOFEGQNGD")
      val res1 = GeneticAlgorithm.countColsToRemove(words, BitChromosome.of("10011"))
      assert(res1 == 4)
      val res2 = GeneticAlgorithm.countColsToRemove(words, BitChromosome.of("11000"))
      assert(res2 == 14)
    }

    it("Finds largest indistinguishable substrings set by UCT and GA") {
      val fileName = getClass.getResource("/words_060_0060_20_0.083.dat")
      InputData.readData(fileName.getPath)
      val extArr = Uct.mainProcedure(10, 60000, 0.1)
      // val extArr = InputData.words
      val result = GeneticAlgorithm.run(extArr, 10, 6000)
      assert(result.isDefined && result.get.length == 9)
    }
  }
}
