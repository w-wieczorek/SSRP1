package ssrp

import ca.aqtech.mctreesearch4j.MDP
import java.util
import scala.jdk.CollectionConverters.IterableHasAsJava

class NodeMDP(val initState: NodeState) extends MDP[NodeState, Int] {
  override def actions(state: NodeState): util.Collection[Int] = {
    state.cols match {
      case first :: tail => (first + 1 to InputData.n - state.k + tail.length + 1).asJavaCollection
      case Nil => (0 to InputData.n - state.k).asJavaCollection
    }
  }

  override def isTerminal(state: NodeState): Boolean = {
    state.cols.length == state.k
  }

  override def initialState(): NodeState = initState.clone()

  override def reward(prevState: NodeState, action: Int, state: NodeState): Double = {
    val card = InputData.determineWordIndices(state.cols.toArray).length
    card.toDouble
  }

  override def transition(state: NodeState, action: Int): NodeState = {
    new NodeState(action :: state.cols, state.k)
  }
}