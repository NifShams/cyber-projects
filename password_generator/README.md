# Password Generator with Entropy-Based Security

This Python script is designed to generate secure, random passwords, ensuring that they meet a minimum entropy requirement of 80 bits. The script offers both ASCII-only and Unicode-supported password generation, making it versatile for different security needs.

## Overview

### What is Entropy?

Entropy is a measure of randomness or unpredictability in a system. In the context of passwords, entropy quantifies how difficult it is to guess or crack a password. It is typically measured in bits, and higher entropy indicates a more secure password.

The formula to calculate entropy for a password is:

                      Entropy = n × log₂(S)

Where:

- **n** is the length of the password.
- **S** is the size of the character set used to generate the password.

### Why a Minimum Entropy of 80 Bits?

A password with 80 bits of entropy is generally considered strong enough for most security applications. This level of entropy ensures that the password is resistant to brute-force attacks, where every possible combination is tried until the correct one is found.

- **For example**:
  - A 6-character password using only lowercase English letters (`S=26`) has an entropy of around 28.2 bits.
  - A 12-character password using a mix of ASCII characters (`S=94`) has an entropy of around 78.8 bits, which is close to the threshold.

By ensuring that every generated password has at least 80 bits of entropy, I significantly increase the difficulty for attackers to guess or brute-force the password.

## Features

- **Entropy-Based Password Generation**: The script generates passwords that meet or exceed 80 bits of entropy, adjusting the password length as needed.

- **ASCII and Unicode Support**: Users can choose to generate passwords using only ASCII characters or a more complex set of Unicode characters.

- **User-Specified Length**: Users can specify a desired password length. If the specified length doesn't meet the entropy requirement, the script will automatically increase the length.

## Usage

1. **Clone the repository** or download the script.

2. **Run the script** using Python 3.x.

3. **Choose your preferences**:
   - ASCII or Unicode password generation.
   - Specify the desired password length or let the script determine the minimum length to achieve the required entropy.

### Example

```bash
$ python password_generator.py
