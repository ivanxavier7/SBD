import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import classes.connection as connect


class passwordHandling:
	"""
        Handles the passwords for all the users
        
        Args:
        Vars:

    """
	def hashing(self, password, user_id):
		"""
        Hashes the password

        Args:
            self (undefined): The object itself
            password (String): User's unhashed password 
            user_id (Integer): Variable with the user's ID number
        Vars:
            key: key that will be read from the database. If empty, then it is equal to an empty byte
            secretKey: secretKey that is either read from the database or generated
            kfd: Key Derivation Funcitons from cryptography's Library
            hashResult: Hashed password

        """
		key = b''
		if user_id != 0:
			self.db = connect.connection(self)
			self.cur = self.db.cursor()
			self.cur.execute('''SELECT secret_key
								FROM funcionario
								WHERE (numero = %s);''', user_id)
			key = self.cur.fetchone()[0]
		if key == b'':
			secretKey = self.createSymmetricKey(user_id)
		else:
			secretKey = key
		password = password.encode()  							# Convert to type bytes
		kdf = PBKDF2HMAC(
		    algorithm = hashes.SHA256(),
		    length = 32,
		    salt = secretKey,
		    iterations = 100000,
		    backend = default_backend()
		)
		hashResult = base64.urlsafe_b64encode(kdf.derive(password))  # Can only use kdf once
		return [hashResult, secretKey]



	def createSymmetricKey(self, user_id):							# Destination should be a path, ex: classes/key.key
		"""
        Creates a symmetric key so the password can be hashed. Each symmetric key is used by a single user
        and a different one is generated every time the user changes password

        Args:
            self (undefined): The object itself
            user_id (Integer): Variable with the user's ID number
        Vars:
            key: Key that was generated

        """
		key = Fernet.generate_key()
		return key