package ssrp

import org.scalatest.funspec.AnyFunSpec

class UctSpec extends AnyFunSpec {
  describe("Uct") {
    it("Finds largest indistinguishable substrings set by UCT") {
      InputData.words = Array("QMAEQGKOFEGQNGD", "QMAEQLPOFEGQNGD",
        "BMAEQMKOFEGQNMD", "QJAENGKOFEGQNGD")
      InputData.n = 15
      InputData.m = 4
      val result = Uct.mcts(4, 400, 0.1)
      assert(result.length == 3)
    }
  }
}
