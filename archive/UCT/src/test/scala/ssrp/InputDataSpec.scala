package ssrp

import org.scalatest.funspec.AnyFunSpec

class InputDataSpec extends AnyFunSpec {
  describe("InputData") {
    it("Reads strings from file") {
      val fileName = getClass.getResource("/words_060_0060_20_0.083.dat")
      InputData.readData(fileName.getPath)
      assert(InputData.n == 60)
      assert(InputData.m == 60)
      assert(InputData.words(49) == "MLCPMBFMCEEMAMMLODTTLMRBRFIHTQMAGQGKOPEGQNGDFDAHEABCCSPLSOHB")
    }

    it("Determine word indices") {
      InputData.words = Array("QMAEQGKOFEGQNGD", "QMAEQLPOFEGQNGD",
        "BMAEQMKOFEGQNMD", "QJAENGKOFEGQNGD")
      InputData.n = 15
      InputData.m = 4
      val indices = InputData.determineWordIndices(Array(3, 5, 6))
      assert(indices.sameElements(Array(0, 1)))
    }
  }
}
