# Ergo Contracts in the Token Distribution System

This document explains the smart contracts used in the Ergo Token Distribution System and how they are designed to be spendable.

## Overview

The system uses two main types of contracts:

1. Proxy Contract
2. Recipient Contracts (standard P2PK addresses)

## Proxy Contract

### Purpose
The proxy contract serves as a secure holding place for the minted tokens and the ERG needed for distribution. It's designed to allow only authorized spending of its contents.

### Structure
The proxy contract is created using ErgoScript and typically includes:
- A time-lock condition
- A specific spending condition (e.g., only spendable by a certain public key)

### Spendability
The proxy contract is spendable under these conditions:
1. The current block height is greater than or equal to the unlock height specified during contract creation.
2. The transaction is signed by the authorized public key (usually the distribution bot's key).

### Example (simplified ErgoScript):
```
{
  val unlockHeight = SELF.R4[Long].get
  val authorizedPubKey = SELF.R5[GroupElement].get
  
  HEIGHT >= unlockHeight && 
  proveDlog(authorizedPubKey)
}
```

In this example:
- `R4` stores the unlock height
- `R5` stores the authorized public key
- `HEIGHT` is the current block height
- `proveDlog(authorizedPubKey)` ensures that the transaction is signed by the owner of the authorized public key

## Recipient Contracts

### Purpose
Recipient contracts are standard P2PK (Pay-to-Public-Key) addresses owned by the token recipients.

### Structure
These are standard Ergo addresses, represented by the public key of the recipient.

### Spendability
Tokens sent to these addresses are spendable by anyone who can provide a valid signature corresponding to the public key of the address.

## Distribution Process

1. **Token Minting**: 
   - Tokens are minted and sent to the proxy contract along with the necessary ERG for distribution.

2. **Distribution**:
   - The distribution bot creates a transaction that:
     a. Spends the proxy contract box
     b. Creates output boxes for each recipient with their share of tokens
     c. Creates a new proxy contract box with the remaining tokens and ERG

3. **Spending Condition**:
   - The distribution transaction must satisfy the proxy contract's conditions:
     a. It must occur after the unlock height
     b. It must be signed by the authorized key

4. **Recipient Spending**:
   - Once tokens are in a recipient's address, they can spend them like any other asset in their Ergo wallet.

## Security Considerations

1. **Time-Lock**: Prevents immediate spending, allowing time for verification or cancellation if needed.
2. **Authorized Key**: Ensures only the designated bot can initiate distributions.
3. **ERG Management**: The proxy contract holds enough ERG for all planned distributions, preventing the need for additional funding.

## Conclusion

This contract system allows for secure holding of tokens, controlled distribution, and easy spending by recipients. The proxy contract acts as a programmable vault, while recipient addresses function as standard Ergo wallets.
