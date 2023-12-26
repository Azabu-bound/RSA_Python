import sympy
import time

def Convert_Text(_string) -> list:
    
    # Initialize an empty list to store ASCII values.
    integer_list = [] 
    
    for character in _string:
        # Convert the character to its ASCII value using ord() and append it to the empty list.
        integer_list.append(ord(character))
    
    return integer_list

def Convert_Num(_list) -> str:
   
    # Initialize an empty string to store characters.
    _string = ''
    
    for number in _list:
        # Convert the ASCII value to its character representation using chr() and append it to the empty string.
        _string += chr(number)
    
    return _string

def Convert_Binary_String(_int) -> str:
    # Initialize an empty string to store binary digits.
    bits = ''
    
    # Edge case: if the integer value is 0 return '0'.
    if _int == 0:
        return "0"
    
    # Loop until the integer becomes 0.
    while _int != 0:
        # Next binary digit: find the remainder after dividing by 2.
        # Convert the remainder to a string and add it to the front of the bits string.
        bits = str(_int % 2) + bits
        
        # Update current integer for the next iteration using floor division.
        _int //= 2
    
    return bits

def FME(b: int, n: int, m: int) -> int:
    
    # Initialize result to 1, since any number to the power of 0 is 1.
    result = 1
    # Initialize square to the base; this value will be squared in each iteration.
    square = b
    
    # Loop until the exponent becomes 0.
    while n > 0:
        
        # Finding the least significant bit.
        lsb = n % 2
        
        # If the least significant bit is 1, multiply the result by the current square value and take modulo m.
        if lsb == 1:
            result = (result * square) % m
        square = (square * square) % m
        
        # Termination condition.
        n //= 2
        
    return result

def Euclidean_Alg(a: int, b: int) -> int:
    
     # Check if the inputs are positive integers.
    if a < 0 or b < 0:
        raise ValueError("Inputs must be positive integers")
    
    # Apply the Euclidean Algorithm to find the Greatest Common Divisor.
    while b != 0:
        # Update a and b for each iteration.
        a, b = b, a % b
    
    return a

def Find_Public_Key_e(p: int, q: int) -> tuple:
    
  # From graphic: Test to ensure p * q is > 150, as to avoid issues with ASCII.
    if (p * q) < 150:
        raise ValueError("Please input prime numbers whose product is > 150")
    
    n = p * q
     
    # Calculate phi (Euler's totient function) as (p-1)(q-1).
    phi = (p - 1) * (q - 1)
    
    # Initialize e to the smallest odd number greater than 2.
    e = 3
    
    # Find e such that 1 < e < phi and gcd(e, phi) = 1.
    while e < phi:
        if e != p and e != q and Euclidean_Alg(e, phi) == 1:
            return n, e
        # Increment e by 2 in each iteration. 
        e += 2
    
    return None

def Extended_Euclidean_Alg(a: int, b: int) -> tuple:
    # Initialize s1, t1, s2, t2
    s1, t1 = 1, 0
    s2, t2 = 0, 1

    # Continue the loop until the remainder is 0.
    while b > 0:
        # Compute the remainder (k) and the quotient (q).
        k = a % b
        q = a // b

        # Update a and b for subsequent iterations.
        a = b
        b = k

        # store the previous coefficients.
        s1_previous = s1
        t1_previous = t1

        # update the coefficients.
        s1, t1 = s2, t2
        s2, t2 = s1_previous - q * s2, t1_previous - q * t2

    # return the GCD (a) and bezout's coefficients (s1, t1).
    return (a, s1, t1)

def Find_Private_Key_d(e: int, p: int, q: int) -> int:
   
    # Calculate the totient of the product of p and q.
    phi = (p - 1) * (q - 1)
    
    # Use the Extended Euclidean Algorithm to find the modular inverse of e modulo phi.
    computations = Extended_Euclidean_Alg(e, phi)
    gcd = computations[0]
    d = computations[1]
    
    # Ensure d is positive. If d is negative, Keep adding the modulo phi to the inverse until a positive integer is reached.
    if d < 0:
        d += phi
    
    # Return the private key.
    return d

def Encode(n: int, e: int, message: str) -> list:
    
    # Initialize an empty list to store the encoded message.
    cipher_text = []
    
    # Convert the text message to a list of ASCII values.
    numbers = Convert_Text(message)
    
    # Encode each ASCII value using the RSA encryption formula.
    for number in numbers:
        cipher_text.append(FME(number, e, n))
    
    # Return encrypted message.
    return cipher_text

def Decode(n: int, d: int, cipher_text: list) -> str:
  
    decrypted_integers = []
    
    # Utilize the Fast Modular Exponentiation function for efficient computation.
    for number in cipher_text:
        decrypted_integers.append(FME(number, d, n))
        
    # Convert the list of decrypted integers back to the original text message.
    message = Convert_Num(decrypted_integers)

    return message

# Let's write the Brute Force Factoring algorithm in Python.
# n is a number, return the smallest factor of n
def factorize(n: int) -> int:
   
    # Iterate through numbers from 2 to (n-1)
    for i in range(2, n):
        
        # Check if i is a factor of n. Return i if it is.
        if n % i == 0:
            return i
    
    # Return false if no factors are found.
    return False

def main():
    print("Welcome, 007, to your Majesty's RSA Encoder/Decoder")

    while True: 
      # User selection: Endode or Decode or Terminate?
      choice = input("Would you like to (E)ncode, (D)ecode, or (T)erminate? ").lower()
      
      # Encoding procedure.
      # Generate two random prime numbers between 150 and 10,000 using symPy.
      if choice == 'e':
          p = sympy.randprime(150, 10000)
          q = sympy.randprime(150, 10000)
          
          # Generate Public keys.
          n, e = Find_Public_Key_e(p, q)
          print(f"Public Key: (n, e) = ({n}, {e})")
          
          # Prompt user for message to encrypt.
          message = input("Enter message: ")
          
          # Encrypt the message using the Encode function.
          cipher_text = Encode(n, e, message)
          print(f"Cipher: {cipher_text}")
          continue
          
      # Decoding procedure.    
      elif choice == 'd':
          break_or_not = input("Do you have the private key (Y/N)? ").lower()

          if break_or_not == 'y':
            # User inputs private keys.
            n = int(input("Enter public key, n: "))
            d = int(input("Enter private key, d: "))
            
            # Remove spaces, commas, and brackets from the encrypted message.
            cipher_text_input = input("Enter the encoded message as a list of integers separated by commas (e.g. [1, 2, 3, 4]): ")
            cipher_text = [int(num.strip()) for num in cipher_text_input.strip("[]").split(",")]
            
            # Decrypt the message using the Decode function. 
            message = Decode(n, d, cipher_text)
            print(f"Decoded message: {message}")
            continue
          else:
             n = int(input("Enter public key, n: "))
             p = factorize(n) 
             # We know that n = p*q. Thus, by algebra, we can say that q = n//p.
             q = n // p
             # Utilitze the private key function to get d.
             e = int(input("Please input public key, e: "))
             d = Find_Private_Key_d(e, p, q)
             print(f"The private Key is: d = {d}")

             # Decode the cipher using the private key.
             cipher_text_input = input("Enter the encoded message as a list of integers separated by commas (e.g. [1, 2, 3, 4]): ")
             cipher_text = [int(num.strip()) for num in cipher_text_input.strip("[]").split(",")]
             message = Decode(n, d, cipher_text)
             print(f"Decoded message: {message}")
             continue

      # Termination procedure.
      elif choice == 't':
          print("Thank you, 007. This device will explode in 7 seconds...")
          
          # Reverses the countdown.
          for i in range(7, 0, -1): 
              print(i)
              # Creates a one second delay.
              time.sleep(1)
          
          print("BOOM!")
          break
      
      # Invalid Entry.
      else:
          print("Invalid entry, please enter E, D, or T")
          continue
      
if __name__ == "__main__":
    main()   