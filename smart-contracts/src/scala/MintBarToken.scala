import org.ergoplatform.appkit._
import org.ergoplatform.appkit.config.ErgoToolConfig
import org.ergoplatform.appkit.impl.ErgoTreeContract

object MintBarToken {
  def main(args: Array[String]): Unit = {
    val conf = ErgoToolConfig.load("ergo_config.json")
    val ergoClient = RestApiErgoClient.create(conf)

    ergoClient.execute((ctx: BlockchainContext) => {
      val prover = ctx.newProverBuilder()
        .withMnemonic(
          SecretString.create(conf.getNode.getWallet.getMnemonic),
          SecretString.create(conf.getNode.getWallet.getPassword)
        )
        .build()

      val txB = ctx.newTxBuilder()

      val token = new ErgoToken(
        txB.outBoxBuilder().build().getId,
        1000000L  // 1 million Bar tokens
      )

      val outBox = txB.outBoxBuilder()
        .value(Parameters.MinChangeValue)
        .tokens(token)
        .contract(
          ctx.compileContract(ConstantsBuilder.create()
            .item("ownerPk", prover.getEip3Addresses.get(0).getPublicKey)
            .build(),
            "{ sigmaProp(INPUTS(0).R4[GroupElement].get == ownerPk) }")
        )
        .build()

      val tx = txB
        .boxesToSpend(ctx.getUnspentBoxesFor(prover.getEip3Addresses.get(0), 1000000000L))
        .outputs(outBox)
        .fee(Parameters.MinFee)
        .sendChangeTo(prover.getEip3Addresses.get(0).getErgoAddress)
        .build()

      val signed = prover.sign(tx)
      val txId = ctx.sendTransaction(signed)
      println(s"Bar tokens minted! Transaction ID: $txId")
    })
  }
}