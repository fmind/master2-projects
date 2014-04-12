package sm.applets;

import javacard.framework.APDU;
import javacard.framework.Applet;
import javacard.framework.ISO7816;
import javacard.framework.ISOException;
import javacard.framework.Util;
import javacard.security.DESKey;
import javacard.security.KeyBuilder;
import javacardx.crypto.Cipher;

public class CryptoApplet extends Applet {
	/* CONSTANT DECLARATION */
	// code of CLA byte in the command APDU header
	final static byte MY_CLA 					= (byte) 0x90;
	// codes of INS byte in the command APDU header
	final static byte SET_SYM_KEY 				= (byte) 0x10;
	final static byte ENCRYPT_DES 				= (byte) 0x20;
	final static byte DECRYPT_DES 				= (byte) 0x30;
	// max length of the key
	final static short MAX_KEY_LENGTH 			= (KeyBuilder.LENGTH_DES / 8);
	// signal the key length is invalid (!=MAX_KEY_LENGTH)
	final static short SW_KEY_LENGTH_INVALID 	= 0x6660;
	// signal the key is not set
	final static short SW_KEY_NOT_SET 			= 0x6661;
	// signal the message is too long
	final static short SW_MESSAGE_TOO_LONG 		= 0x6662;
	// signal the message is empty
	final static short SW_MESSAGE_EMPTY 		= 0x6663;
	
	/* INSTANCE VARIABLE DECLARATION */
	private Cipher encryptor;
	private Cipher decryptor;
	private DESKey deskey;

	/**
	 * Applet Constructor
	 */
	private CryptoApplet() {
		// initialize instance variables
		encryptor = Cipher.getInstance(Cipher.ALG_DES_CBC_ISO9797_M1, true);
		decryptor = Cipher.getInstance(Cipher.ALG_DES_CBC_ISO9797_M1, true);
		deskey = (DESKey) KeyBuilder.buildKey(KeyBuilder.TYPE_DES, KeyBuilder.LENGTH_DES, false);
		
		register();
	}

	/**
	 * Applet Installer
	 * 
	 * @param byteArray
	 * @param offset
	 * @param length
	 */
	public static void install(byte[] byteArray, short offset, byte length) {
		// create a Crypto Applet instance
		new CryptoApplet();
	}

	/**
	 * Applet Processor
	 * 
	 * @param apdu
	 */
	public void process(APDU apdu) {
		byte[] buffer = apdu.getBuffer();

		// check SELECT APDU command
		if ((buffer[ISO7816.OFFSET_CLA] == 0)
				&& (buffer[ISO7816.OFFSET_INS] == (byte) (0xA4)))
			return;

		// verify the reset of commands have the correct CLA byte
		if (buffer[ISO7816.OFFSET_CLA] != MY_CLA)
			ISOException.throwIt(ISO7816.SW_CLA_NOT_SUPPORTED);

		// dispatch APDU command
		switch (buffer[ISO7816.OFFSET_INS]) {
			case SET_SYM_KEY:
				setSymKey(apdu);
				return;
			case ENCRYPT_DES:
				encryptDES(apdu);
				return;
			case DECRYPT_DES:
				decryptDES(apdu);
				return;
			default:
				ISOException.throwIt(ISO7816.SW_INS_NOT_SUPPORTED);
		}
	}
	
	/**
	 * Set the DES key
	 * 
	 * @param apdu
	 */
	private void setSymKey(APDU apdu) {
		byte[] buffer = apdu.getBuffer();
		short lc = apdu.setIncomingAndReceive();
		
		// the number of data bytes read does not match the number in Lc byte
		if (lc != MAX_KEY_LENGTH)
			ISOException.throwIt(SW_KEY_LENGTH_INVALID);
		
		// copy the key
		byte[] key = new byte[MAX_KEY_LENGTH];
		Util.arrayCopy(buffer, ISO7816.OFFSET_CDATA, key, (short) 0, MAX_KEY_LENGTH);
		
		// re-init the cipher
		deskey.setKey(key, (short) 0);
		encryptor.init(deskey, Cipher.MODE_ENCRYPT);
		decryptor.init(deskey, Cipher.MODE_DECRYPT);
	}
	
	/**
	 * Encrypt a message
	 * 
	 * @param apdu
	 */
	private void encryptDES(APDU apdu) {
		byte[] buffer = apdu.getBuffer();
		short lc = apdu.setIncomingAndReceive();
		
		// ERRORS
		// key is not set
		if (!deskey.isInitialized())
			ISOException.throwIt(SW_KEY_NOT_SET);
		// message is not set
		if (lc ==0)
			ISOException.throwIt(SW_MESSAGE_EMPTY);
		// message is too long
		if (lc > 255)
			ISOException.throwIt(SW_MESSAGE_TOO_LONG);
		
		// encrypt the message
		short byteOutput = encryptor.doFinal(buffer, ISO7816.OFFSET_CDATA, lc, buffer, (short) 0);
		
		// send the result
		apdu.setOutgoing();
		apdu.setOutgoingLength(byteOutput);
		Util.arrayCopy(buffer, (short) 0, buffer, (short) 0, byteOutput);
		apdu.sendBytes((short) 0, byteOutput);
	}
	
	/**
	 * Decrypt a message
	 * 
	 * @param apdu
	 */
	private void decryptDES(APDU apdu) {
		byte[] buffer = apdu.getBuffer();
		short lc = apdu.setIncomingAndReceive();
		
		// ERRORS
		// key is not set
		if (!deskey.isInitialized())
			ISOException.throwIt(SW_KEY_NOT_SET);
		// message is not set
		if (lc ==0)
			ISOException.throwIt(SW_MESSAGE_EMPTY);
		// message is too long
		if (lc > 255)
			ISOException.throwIt(SW_MESSAGE_TOO_LONG);
		
		// encrypt the message
		short byteOutput = decryptor.doFinal(buffer, ISO7816.OFFSET_CDATA, lc, buffer, (short) 0);
		
		// send the result
		apdu.setOutgoing();
		apdu.setOutgoingLength(byteOutput);
		Util.arrayCopy(buffer, (short) 0, buffer, (short) 0, byteOutput);
		apdu.sendBytes((short) 0, byteOutput);
	}
}
