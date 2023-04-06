ThisBuild / version := "0.1.0-SNAPSHOT"

ThisBuild / scalaVersion := "2.13.8"

lazy val root = (project in file("."))
  .settings(
    name := "ssrp",
    assembly / assemblyJarName := "ssrp.jar",
    assembly / mainClass := Some("ssrp.Main"),
    assembly / test := {},
    assembly / assemblyMergeStrategy := {
      case PathList("META-INF", xs @ _*) => MergeStrategy.discard
      case x => MergeStrategy.first
    }
  )

libraryDependencies ++= Seq(
  "ca.aqtech" % "mctreesearch4j" % "0.0.4",
  "io.jenetics" % "jenetics" % "7.0.0",
  "ch.qos.logback" % "logback-classic" % "1.2.11",
  "com.typesafe.scala-logging" %% "scala-logging" % "3.9.4",
  "org.scalatest" %% "scalatest-funspec" % "3.2.12" % "test"
)
