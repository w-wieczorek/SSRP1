package ssrp

import com.typesafe.scalalogging._
import ca.aqtech.mctreesearch4j.{StateNode, StatefulSolver}
import scala.collection.mutable
import scala.jdk.CollectionConverters.CollectionHasAsScala

class SsrpSolver(val initialState: NodeState, val c: Double)
  extends StatefulSolver[NodeState, Int](new NodeMDP(initialState), InputData.n, c, 0.9, false)
    with StrictLogging {
  def getCols(iters: Int): Array[Int] = {
    runTreeSearch(iters)
    var node = getRoot
    var bestAction = -1
    var bestNode: StateNode[NodeState, Int] = null
    val arr = mutable.ArrayBuffer.empty[Int]
    while(node != null) {
      var bestN = 0
      bestAction = -1
      bestNode = null
      val actions = node.getValidActions.asScala
      for(a <- actions) {
        for(child <- node.getChildren(a).asScala) {
          if(child.getN > bestN) {
            bestN = child.getN
            bestNode = child
            bestAction = a
          }
        }
      }
      if(bestAction > - 1)
        arr.addOne(bestAction)
      node = bestNode
    }
    arr.toArray
  }
}

object Uct extends StrictLogging {
  def mcts(k: Int, iters: Int, c: Double): Array[String] = {
    val solver = new SsrpSolver(new NodeState(Nil, k), c)
    val cols = solver.getCols(iters)
    val indexes = InputData.determineWordIndices(cols)
    indexes.map(InputData.words(_))
  }

  def mainProcedure(k: Int, iters: Int, c: Double): Array[String] = {
    var arr = mcts(k, iters, c)
    var copy = arr
    var next_k = 2*k
    val initialCard = arr.length
    logger.debug(s"For k = $k cardinality = $initialCard")
    var currCard = initialCard
    var prevCard = 0
    while(next_k < InputData.n && currCard <= 5*initialCard && currCard >= prevCard) {
      copy = arr
      arr = mcts(next_k, iters, c)
      prevCard = currCard
      currCard = arr.length
      logger.debug(s"For k = $next_k cardinality = $currCard")
      next_k += k
    }
    if(arr.length >= copy.length)
      arr
    else
      copy
  }
}
