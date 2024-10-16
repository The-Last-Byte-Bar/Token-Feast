name := "Token-Flight-Contracts"
version := "0.1"
scalaVersion := "2.13.8"

val AkkaVersion = "2.6.18"
val AkkaHttpVersion = "10.2.9"

libraryDependencies ++= Seq(
  "org.ergoplatform" %% "ergo-appkit" % "5.0.3",
  "com.typesafe.akka" %% "akka-actor-typed" % AkkaVersion,
  "com.typesafe.akka" %% "akka-stream" % AkkaVersion,
  "com.typesafe.akka" %% "akka-http" % AkkaHttpVersion,
  "com.typesafe.akka" %% "akka-http-spray-json" % AkkaHttpVersion,
  "io.spray" %% "spray-json" % "1.3.6"
)

resolvers ++= Seq(
  "Sonatype Releases" at "https://oss.sonatype.org/content/repositories/releases/",
  "SonaType" at "https://oss.sonatype.org/content/groups/public",
  "Sonatype Snapshots" at "https://oss.sonatype.org/content/repositories/snapshots/"
)