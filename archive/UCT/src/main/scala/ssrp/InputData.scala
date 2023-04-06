package ssrp

import com.typesafe.scalalogging._
import scala.collection.mutable
import scala.io.Source

object InputData extends StrictLogging {
  var words: Array[String] = null
  var m = 0  // the number of words
  var n = 0  // the size of a word

  def readData(fileName: String): Unit = {
    val source = Source.fromFile(fileName)
    words = try source.getLines.toArray finally source.close()
    if(words eq null) {
      logger.error(s"There is a problem with file $fileName.")
      sys.exit(1)
    }
    m = words.length
    if(m == 0) {
      logger.error(s"There are no words in file $fileName.")
      sys.exit(1)
    }
    n = words(0).length
    logger.debug(s"The length of the first word is $n.")
    for(w <- words) {
      if(w.length != n) {
        logger.error("Not all the strings have the same length!")
        sys.exit(1)
      }
    }
  }

  def determineWordIndices(arrOfCols: Array[Int]): Array[Int] = {
    val result = mutable.HashMap.empty[String, mutable.Set[Int]]
    val columns = mutable.HashSet.from(arrOfCols)
    for(i <- 0 until m) {
      val str = new mutable.StringBuilder()
      for(j <- 0 until n if !columns.contains(j)) {
        str.addOne(InputData.words(i)(j))
      }
      val s = str.toString
      if(result.contains(s))
        result(s).addOne(i)
      else
        result(s) = mutable.HashSet(i)
    }
    val (w, inds) = result.maxBy(entry => entry._2.size)
    inds.toArray
  }
}
