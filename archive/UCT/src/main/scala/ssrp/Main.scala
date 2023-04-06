package ssrp

import scala.annotation.tailrec
import ch.qos.logback.classic.{Level, Logger}
import org.slf4j.LoggerFactory
import com.typesafe.scalalogging._
import scala.collection.mutable
import scala.util.Sorting.quickSort

object Main extends StrictLogging {
  val help: String = """
  |Usage: java -jar ssrp.jar arguments
  |Where the allowed arguments are:
  |  -h | --help             Show help
  |  -f | --file file_name   The name of a file including strings (required)
  |  -k | --knum number      The number of columns to remove (required)
  |  -m | --mcts iters       The number of iterations in MCTS (default = 100 * strlen)
  |  -g | --ga iters         The number of iterations in GA (default = 40 * #strings)
  |  -c | --cparam           Exploration constant (default = 0.1)
  |  -l | --ll log_level     debug, info, or error (default = info)
  |""".stripMargin

  def quit(status: Int = 0, message: String = ""): Nothing = {
    if (message.nonEmpty) println(s"ERROR: $message")
    println(help)
    sys.exit(status)
  }

  case class Args(fileName: Option[String], kNum: Option[String], mctsIters: Option[String],
                  gaIters: Option[String], cParam: Option[String], logLevel: Option[String])

  def parseArgList(params: Array[String]): Args = {
    @tailrec
    def pa(params2: Seq[String], args: Args): Args = params2 match {
      case Nil => args
      case ("-h" | "--help") +: Nil => quit()
      case ("-f" | "--file") +: file +: tail =>
        pa(tail, args.copy(fileName = Some(file)))
      case ("-k" | "--knum") +: number +: tail =>
        pa(tail, args.copy(kNum = Some(number)))
      case ("-m" | "--mcts") +: miters +: tail =>
        pa(tail, args.copy(mctsIters = Some(miters)))
      case ("-g" | "--ga") +: giters +: tail =>
        pa(tail, args.copy(gaIters = Some(giters)))
      case ("-c" | "--cparam") +: cparam +: tail =>
        pa(tail, args.copy(cParam = Some(cparam)))
      case ("-l" | "--ll") +: ll +: tail =>
        pa(tail, args.copy(logLevel = Some(ll)))
      case _ => quit(1, s"Unrecognized argument ${params2.head}")
    }

    val argz = pa(params.toList, Args(None, None, None, None, Option("0.1"), Option("info")))
    if (argz.fileName.isEmpty || argz.kNum.isEmpty)
      quit(1, "Must specify file name and k-number.")
    argz
  }

  def main(params: Array[String]): Unit = {
    val argz = parseArgList(params)
    val newloglevel = argz.logLevel.get match {
      case "debug" => Level.DEBUG_INT
      case "info"  => Level.INFO_INT
      case "error" => Level.ERROR_INT
    }
    LoggerFactory.getLogger(org.slf4j.Logger.ROOT_LOGGER_NAME)
      .asInstanceOf[Logger].setLevel(Level.toLevel(newloglevel))
    val fileName = argz.fileName.get
    logger.debug(s"File name is $fileName.")
    val kNum = argz.kNum.get.toInt
    logger.debug(s"K-number is $kNum.")
    val cParam = argz.cParam.get.toDouble
    logger.info(s"Loading data from $fileName...")
    InputData.readData(fileName)
    logger.info(s"Read ${InputData.m} lines each of length ${InputData.n}.")
    val mctsIters = argz.mctsIters match {
      case Some(num) => num.toInt
      case None => 100 * InputData.n
    }
    logger.debug(s"$mctsIters set for MCTS iterations.")
    val extArr = Uct.mainProcedure(kNum, mctsIters, cParam)
    logger.debug(s"Extended array of ${extArr.length} strings found.")
    val gaIters = argz.gaIters match {
      case Some(num) => num.toInt
      case None => 80 * InputData.m
    }
    logger.debug(s"$gaIters set for GA iterations.")
    var resultArr = GeneticAlgorithm.run(extArr, kNum, gaIters)
    if(resultArr.isEmpty) {
      logger.info("Very poor performance of GA.")
      resultArr = Option(Uct.mcts(kNum, 2*mctsIters, cParam))
    }
    val arr = resultArr.get
    quickSort(arr)
    val resInds = mutable.HashSet.empty[Int]
    var idx = -1
    for(j <- arr.indices) {
      if(j == 0 || arr(j) != arr(j-1)) {
        idx = InputData.m
      }
      idx = InputData.words.lastIndexOf(arr(j), idx-1)
      assert(idx > -1)
      resInds.add(idx)
    }
    logger.info(s"The best solution consists of ${arr.length} words.")
    logger.info(s"String's indexes: ${resInds}")
  }
}
