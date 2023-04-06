package ssrp

class NodeState(val cols: List[Int], val k: Int) extends Cloneable {
  def this(otherState: NodeState) = this(otherState.cols, otherState.k)
  override def clone(): NodeState = new NodeState(this)
}