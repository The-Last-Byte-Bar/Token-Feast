import org.ergoplatform.appkit._
import org.ergoplatform.appkit.config.ErgoToolConfig
import org.ergoplatform.appkit.impl.ErgoTreeContract
import scorex.crypto.hash.Blake2b256
import sigmastate.eval._
import special.sigma.Box

import scala.collection.JavaConverters._

object MintBarToken extends App {
  val config = ErgoToolConfig.load("ergo_config.json")
  val nodeConf = config.getNode
  val networkType = NetworkType.MAINNET // or NetworkType.TESTNET for testnet
  val nodeUrl = "http://127.0.0.1:9053" //nodeConf.getNodeUrl // Assuming nodeConf has a method to get the node URL
  val nodeAPI = 'movingtoFlorida'
  // Print the variables to check their values
  println(s"Node Config: $nodeConf")
  println(s"Network Type: $networkType")

  // Initialize the Ergo client
  val ergoClient = RestApiErgoClient.create(nodeUrl, networkType, nodeAPI, "")

  ergoClient.execute { ctx =>
    // Load your wallet (Nautilus integration would go here)
    // For this example, we'll use a mock wallet address
    val senderAddress = Address.create("9f4QF8AD1nQ3nJahQVkMj8hFSVVzVom77b52JU7EW71Zexg6N8v")

    // Define token details
    val tokenName = "Bar"
    val tokenDescription = "Bar Token"
    val tokenAmount = 1000000L // 1 million tokens

    // Create a new transaction
    val txB = ctx.newTxBuilder()

    // Define the token to be minted
    val token = new ErgoToken(
      scorex.util.encode.Base16.encode(Blake2b256.hash(tokenName)),
      tokenAmount
    )

    // Create the output box with minted tokens
    val outBox = txB.outBoxBuilder()
      .value(Parameters.MinBoxValue)
      .tokens(token)
      .contract(new ErgoTreeContract(senderAddress.getErgoAddress.script))
      .registers(
        ErgoValue.of(tokenName.getBytes()),
        ErgoValue.of(tokenDescription.getBytes())
      )
      .build()

    // Build the unsigned transaction
    val unsignedTx = txB
      .boxesToSpend(ctx.getUnspentBoxesFor(senderAddress, 0, 20).get(0))
      .outputs(outBox)
      .fee(Parameters.MinFee)
      .sendChangeTo(senderAddress.getErgoAddress)
      .build()

    // This is where you would typically sign the transaction with Nautilus
    // For demonstration, we'll just print the unsigned transaction
    println(s"Unsigned transaction: ${unsignedTx.toJson(false)}")

    // Spending the box (after some time)
    // This part would typically be in a separate transaction
    val boxesToSpend = ctx.getUnspentBoxesFor(senderAddress, 0, 20).get
    val boxWithTokens = boxesToSpend.asScala.find(_.getTokens.asScala.exists(_.getId.toString == token.getId.toString)).get

    val spendingTx = txB
      .boxesToSpend(boxWithTokens)
      .outputs(
        txB.outBoxBuilder()
          .value(Parameters.MinBoxValue)
          .tokens(token)
          .contract(new ErgoTreeContract(senderAddress.getErgoAddress.script))
          .build()
      )
      .fee(Parameters.MinFee)
      .sendChangeTo(senderAddress.getErgoAddress)
      .build()

    println(s"Unsigned spending transaction: ${spendingTx.toJson(false)}")
  }
}