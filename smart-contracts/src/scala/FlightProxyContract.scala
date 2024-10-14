import org.ergoplatform.appkit._

object FlightProxyContract {
  def getScript: String = {
    """
      |{
      |  val ownerPk = SELF.R4[GroupElement].get
      |  val lastFlightHeight = SELF.R5[Int].get
      |  val flightInterval = 10  // blocks
      |
      |  sigmaProp(
      |    (ownerPk || (CONTEXT.preHeader.height >= lastFlightHeight + flightInterval)) &&
      |    OUTPUTS(0).R4[GroupElement].get == ownerPk &&
      |    OUTPUTS(0).R5[Int].get == CONTEXT.preHeader.height
      |  )
      |}
    """.stripMargin
  }

  def getContract(ctx: BlockchainContext, ownerPk: ErgoValue[GroupElement]): ErgoContract = {
    ctx.compileContract(
      ConstantsBuilder.create()
        .item("ownerPk", ownerPk)
        .build(),
      getScript
    )
  }
}