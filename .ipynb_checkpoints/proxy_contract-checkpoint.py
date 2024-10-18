# proxy_contract.py
import binascii
from ergo_python_appkit.appkit import ErgoAppKit
from org.ergoplatform.appkit import Address

def create_proxy_contract(appKit: ErgoAppKit, recipients: list[str], unlock_height: int, node_address: str) -> bytes:
    recipient_ergo_trees = [Address.create(addr).getErgoAddress().script().bytes() for addr in recipients]
    recipient_ergo_trees_hex = [binascii.hexlify(bytes(tree)).decode('utf-8') for tree in recipient_ergo_trees]
    recipient_trees_str = ', '.join(f'fromBase16("{tree}")' for tree in recipient_ergo_trees_hex)
    
    node_tree = Address.create(node_address).getErgoAddress().script().bytes()
    node_tree_hex = binascii.hexlify(bytes(node_tree)).decode('utf-8')
    
    contract_script = f"""
    {{
        val recipientTrees = Coll({recipient_trees_str})
        val unlockHeight = {unlock_height}L
        val nodeTree = fromBase16("{node_tree_hex}")
        
        sigmaProp({{
            val validRecipients = OUTPUTS.slice(0, recipientTrees.size).forall({{(out: Box) =>
                recipientTrees.exists({{(tree: Coll[Byte]) => 
                    out.propositionBytes == tree
                }})
            }})
            val heightOk = HEIGHT >= unlockHeight
            val validTokenDistribution = OUTPUTS.slice(0, recipientTrees.size).forall({{(out: Box) =>
                out.tokens.size == 1 && out.tokens(0)._2 > 0L
            }})
            
            val spentByNode = OUTPUTS(0).propositionBytes == nodeTree
            
            (validRecipients && heightOk && validTokenDistribution) || spentByNode
        }})
    }}
    """
    
    return appKit.compileErgoScript(contract_script)