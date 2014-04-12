package sm.appli;

import javax.smartcardio.Card;
import javax.smartcardio.CardChannel;
import javax.smartcardio.CardException;
import javax.smartcardio.CardTerminal;
import javax.smartcardio.CardTerminals;
import javax.smartcardio.CommandAPDU;
import javax.smartcardio.ResponseAPDU;
import javax.smartcardio.TerminalFactory;

/**
 * Client interface with the smartcard
 */
public class CryptoEngine {
	private CardTerminal terminal;
	private CardChannel channel;
	private Card card;
	
	/**
	 * Create a new CryptoEngine
	 */
	public CryptoEngine() {
		this.terminal = null;
		this.channel = null;
		this.card = null;
	}
	
	/**
	 * Check if a Response APDU contains errors
	 * 
	 * @param resp
	 * @throws CommandError
	 */
	private void errorHandler(ResponseAPDU resp) throws CommandError {
		switch (resp.getSW()) {
			// no error
			case 0x9000: return;
			// my error
			case 0x6660: throw new CommandError(resp.getSW(), "Key length invalid");
			case 0x6661: throw new CommandError(resp.getSW(), "Key not set");
			case 0x6662: throw new CommandError(resp.getSW(), "Message too long");
			case 0x6663: throw new CommandError(resp.getSW(), "Message empty");
			// constructor error
			case 0x6700: throw new CommandError(resp.getSW(), "Wrong data length");
			case 0x6e00: throw new CommandError(resp.getSW(), "CLA not supported");
			case 0x6d00: throw new CommandError(resp.getSW(), "INS not supported");
			case 0x6999: throw new CommandError(resp.getSW(), "Card locked (Maximum authentification tries exceeded)");
			case 0x6a82: throw new CommandError(resp.getSW(), "Invalid applet ID");
			// generic error
			default: throw new CommandError(resp.getSW(), "Generic error");
		}
	}
	
	/**
	 * Initialize the terminal, the card and the channel
	 * 
	 * @throws CardException
	 */
	public void init() throws CardException {
		System.out.println("Initialiazing terminal/card/channel ...");
		
		// init terminal
		TerminalFactory factory = TerminalFactory.getDefault();
		CardTerminals terminals = factory.terminals();
		terminal = terminals.getTerminal("SCM Microsystems Inc. SCR33x USB Smart Card Reader 0");
		if (terminal == null) {
			throw new CardException("No terminal detected :(");
		}
		
		// init card
		terminal.waitForCardPresent(15000);
		if (!terminal.isCardPresent()) {
			throw new CardException("No card detected :(");
		}
		
		// init channel
		card = terminal.connect("*");
		channel = card.getBasicChannel();
	}
	
	/**
	 * Select an applet
	 * 
	 * @throws CardException
	 * @throws CommandError 
	 */
	public void selectApplet(short id) throws CardException, CommandError {
		System.out.println("Selecting applet ...");
		byte[] data = {(byte) 0xEE, (byte) 0x00, (byte) 0x00, (byte) 0x00, (byte) 0x00, (byte) 0xBB, (byte) id};
		CommandAPDU req = new CommandAPDU(0x00, 0xA4, 0x04, 0x00, data, 0x02);
		ResponseAPDU resp = channel.transmit(req);
		
		errorHandler(resp);
		
		System.out.println("");
		System.out.println("APPLET SELECTED: " + fromBytesToHexString(req.getBytes()));
		System.out.println("");
	}
	
	/**
	 * Set the DES Key of the application
	 * 
	 * @param key
	 * @throws CardException
	 */
	public void setSymKey(String key) throws CardException {
		CommandAPDU req = new CommandAPDU(0x90, 0x10, 0x0, 0x0, key.getBytes());
		ResponseAPDU resp = channel.transmit(req);
		
		errorHandler(resp);
	}
	
	/**
	 * Encrypt a message
	 * 
	 * @param message
	 * @return encrypted message
	 * @throws CardException
	 * @throws CommandError
	 */
	public String encryptDES(String message) throws CardException, CommandError {
		CommandAPDU req = new CommandAPDU(0x90, 0x20, 0x0, 0x0, message.getBytes());
		ResponseAPDU resp = channel.transmit(req);
		
		errorHandler(resp);
		
		return fromBytesToHexString(resp.getData());
	}
	
	/**
	 * Decrypt a message
	 * 
	 * @param message
	 * @return decrypted message
	 * @throws CardException
	 * @throws CommandError
	 */
	public String decryptDES(String message) throws CardException, CommandError {
		byte[] data = fromHexStringToBytes(message);
		CommandAPDU req = new CommandAPDU(0x90, 0x30, 0x0, 0x0, data);
		ResponseAPDU resp = channel.transmit(req);
		
		errorHandler(resp);

		return new String(resp.getData()).trim();
	}
	
	/**
	 * Terminate all communication
	 * 
	 * @throws CardException 
	 */
	public void end() throws CardException {
		System.out.println("Closing the application ...");
		
		card.disconnect(true);
		
		System.out.println("Good bye :)");
	}
	
	/**
	 * Convert a byte[] array to readable Hex String format.
	 * @param in byte[] buffer to convert to string format
	 * @return result String buffer in String format
	 * 
	*/
	public static String fromBytesToHexString(byte inBytes[]) {
		StringBuffer buffer = new StringBuffer();
		
		for(int i=0;i<inBytes.length;i++) {
			// Get the first digit of the hexadecimal
			buffer.append(Integer.toHexString((inBytes[i] & 0xF0)>>4).toUpperCase());
			// Get the second digit of the hexadecimal
			buffer.append(Integer.toHexString(inBytes[i] & 0x0F).toUpperCase());
			// Append a blank space at the end of each hexadecimal
			buffer.append(" ");
		}
		
		return buffer.toString();
	}
	
	/**
	 * Convert a Hex String format to a byte[] array
	 * @param String buffer in Hex format
	 * @return byte[] buffer
	 */
	public static byte[] fromHexStringToBytes(String hex) {
		// accept format with ' ' or ':'
		hex = hex.replace(" ", "").replace(":", "");
		
		int len = hex.length();
	    byte[] data = new byte[len / 2];
	    
	    for (int i = 0; i < len; i += 2) {
	        data[i / 2] = (byte) ((Character.digit(hex.charAt(i), 16) << 4)
	                             + Character.digit(hex.charAt(i+1), 16));
	    }

	    return data;
	}
}
