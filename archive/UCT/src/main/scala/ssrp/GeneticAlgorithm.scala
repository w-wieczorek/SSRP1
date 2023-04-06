package ssrp

import com.typesafe.scalalogging._
import io.jenetics.{BitChromosome, BitGene, Genotype, RouletteWheelSelector, TournamentSelector}
import io.jenetics.engine.Engine
import io.jenetics.engine.EvolutionResult
import io.jenetics.util.Factory
import scala.jdk.CollectionConverters.IteratorHasAsScala

object GeneticAlgorithm extends StrictLogging {
  def countColsToRemove(arr: Array[String], chrom: BitChromosome): Int = {
    var result = 0
    var i = 0
    var symbol: Option[Char] = None
    if(chrom.bitCount > 0) {
      val n = arr(0).length
      for (j <- 0 until n) {
        symbol = None
        i = 0
        while(i < arr.length) {
          if(chrom.booleanValue(i)) {
            if (symbol.isEmpty) {
              symbol = Option(arr(i)(j))
            }
            if (arr(i)(j) != symbol.get) {
              result += 1
              i = Int.MaxValue - 1
            }
          }
          i += 1
        }
      }
    }
    result
  }

  def run(chosenWords: Array[String], kNum: Int, gaIters: Int): Option[Array[String]] = {
    logger.info(s"The size of chosen words set is ${chosenWords.length} (of ${InputData.words.length} all).")

    // 1.) Define the genotype (factory) suitable
    //     for the problem.
    val gtf: Factory[Genotype[BitGene]] =
    Genotype.of(BitChromosome.of(chosenWords.length, 0.5))

    // 2.) Definition of the fitness function.
    def eval(gt: Genotype[BitGene]): Integer = {
      val chrom = gt.chromosome().as(classOf[BitChromosome])
      val ncols = countColsToRemove(chosenWords, chrom)
      if(ncols <= kNum)
        chrom.bitCount()
      else
        chrom.bitCount() / ncols
    }

    // 3.) Create the execution environment.
    val engine = Engine
      .builder[BitGene, Integer](eval, gtf)
      .populationSize(math.min(50, 2*chosenWords.length))
      .survivorsSelector(new TournamentSelector(5))
      .offspringSelector(new RouletteWheelSelector())
      .build()

    // 4.) Start the execution (evolution) and
    //     collect the result.
    logger.debug("Genetic algorithm started...")
    val result = engine.stream()
      .limit(gaIters)
      .collect(EvolutionResult.toBestGenotype[BitGene, Integer])

    logger.debug(s"After $gaIters resultant chromosome:\n ${result.toString}")
    val chrom = result.chromosome().as(classOf[BitChromosome])
    val ncols = countColsToRemove(chosenWords, chrom)
    if(ncols <= kNum) {
      Option(chrom.ones().iterator().asScala.map(InputData.words(_)).toArray)
    } else {
      None
    }
  }
}
