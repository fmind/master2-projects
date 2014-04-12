package sm.appli;

import java.nio.ByteBuffer;

import javax.smartcardio.Card;
import javax.smartcardio.CardChannel;
import javax.smartcardio.CardException;
import javax.smartcardio.CardTerminal;
import javax.smartcardio.CardTerminals;
import javax.smartcardio.CommandAPDU;
import javax.smartcardio.ResponseAPDU;
import javax.smartcardio.TerminalFactory;

public class Wallet {
	private CardTerminal terminal;
	private CardChannel channel;
	private Card card;
	private boolean withPIN;
	
	/**
	 * Create a new wallet
	 * 
	 */
	public Wallet() {
		this.terminal = null;
		this.channel = null;
		this.card = null;
		this.withPIN = false;
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
			case 0x6300: throw new CommandError(resp.getSW(), "PIN verification failed");
			case 0x6301: throw new CommandError(resp.getSW(), "PIN verification required");
			case 0x6302: throw new CommandError(resp.getSW(), "PIN trials exceeded");
			case 0x6a83: throw new CommandError(resp.getSW(), "Invalid transaction amount");
			case 0x6a84: throw new CommandError(resp.getSW(), "Exceed maximum balance");
			case 0x6a85: throw new CommandError(resp.getSW(), "Negative balance");
			// constructor error
			case 0x6e00: throw new CommandError(resp.getSW(), "CLA not supported");
			case 0x6d00: throw new CommandError(resp.getSW(), "INS not supported");
			case 0x6999: throw new CommandError(resp.getSW(), "Card locked (Maximum authentification tries exceeded)");
			case 0x6a82: throw new CommandError(resp.getSW(), "Invalid applet ID");
			// generic error
			default: throw new CommandError(resp.getSW(), "Generic error");
		}
	}
	
	/**
	 * Initialize the terminal and the card
	 * 
	 * @throws CardException
	 */
	public void init() throws CardException {
		System.out.println("Initialiazing terminal/card ...");
		
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
		card = terminal.connect("*");
		channel = card.getBasicChannel();
	}
	
	/**
	 * Select the applet without PIN
	 * 
	 * @throws CardException
	 * @throws CommandError 
	 */
	public void selectAppletWithoutPin() throws CardException, CommandError {
		System.out.println("Selecting applet without PIN ...");
		selectApplet((short) 0x02);
		this.withPIN = false;
	}
	
	/**
	 * Select the applet with PIN
	 * 
	 * @throws CardException
	 * @throws CommandError 
	 */
	public void selectAppletWithPin() throws CardException, CommandError {
		System.out.println("Selecting applet with PIN ...");
		selectApplet((short) 0x04);
		this.withPIN = true;
	}
	
	/**
	 * Select an applet
	 * 
	 * @throws CardException
	 * @throws CommandError 
	 */
	private void selectApplet(short id) throws CardException, CommandError {
		byte[] data = {(byte) 0xEE, (byte) 0x00, (byte) 0x00, (byte) 0x00, (byte) 0x00, (byte) 0xBB, (byte) id};
		CommandAPDU req = new CommandAPDU(0x00, 0xA4, 0x04, 0x00, data, 0x02);
		ResponseAPDU resp = channel.transmit(req);
		errorHandler(resp);
		
		System.out.println("");
		System.out.println("APPLET SELECTED: " + fromBytesToHexString(req.getBytes()));
		System.out.println("");
	}
	
	/**
	 * Retrieve balance from the card
	 * @return
	 * @throws CardException
	 */
	public short getBalance() throws CardException {
		CommandAPDU req = new CommandAPDU(0x90, 0x50, 0x0, 0x0, 0x02);
		ResponseAPDU resp = channel.transmit(req);
		
		return ByteBuffer.wrap(resp.getBytes()).getShort();
	}
	
	/**
	 * Authentificate a user with a PIN
	 * 
	 * @param pin
	 * @throws CardException
	 * @throws CommandError
	 */
	public void verify(String pin) throws CardException, CommandError {
		byte[] data = fromPinToBytes(pin);
		CommandAPDU req = new CommandAPDU(0x90, 0x20, 0x0, 0x0, data, 0x02);
		ResponseAPDU resp = channel.transmit(req);
		
		errorHandler(resp);
	}
	
	/**
	 * Credit the card from a value
	 * 
	 * @param value
	 * @throws CardException
	 * @throws CommandError
	 */
	public void credit(int value) throws CardException, CommandError {
		byte[] data = {(byte) value};
		CommandAPDU req = new CommandAPDU(0x90, 0x30, 0x0, 0x0, data, 0x02);
		ResponseAPDU resp = channel.transmit(req);
		
		errorHandler(resp);
	}
	
	/**
	 * Debit the card from a value
	 * 
	 * @param value
	 * @throws CardException
	 * @throws CommandError
	 */
	public void debit(int value) throws CardException, CommandError {
		byte[] data = {(byte) value};
		CommandAPDU req = new CommandAPDU(0x90, 0x40, 0x0, 0x0, data, 0x02);
		ResponseAPDU resp = channel.transmit(req);
		
		errorHandler(resp);
	}
	
	
	/**
	 * Set the wallet balance to 0
	 * 
	 * @throws CardException
	 * @throws CommandError
	 */
	public void reset() throws CardException, CommandError {
		int balance = getBalance();
		int debit_value = 0;
		
		while (balance > 0) {
			debit_value = (balance < 100) ? balance : 100;
			debit(debit_value);
			
			balance -= debit_value;
		}
	}
	
	/**
	 * Terminate all communication
	 * 
	 * @throws CardException 
	 */
	public void end() throws CardException {
		System.out.println("Closing the application ...");
		
		card.disconnect(true);
		
		System.out.println("");
		System.out.println("Good bye :)");
	}
	
	/**
	 * Convert a byte[] array to readable Hex String format.
	 * @param in byte[] buffer to convert to string format
	 * @return result String buffer in String format
	 * 
	*/
	private String fromBytesToHexString(byte inBytes[]) {
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
	 * Convert a PIN code to a byte array
	 * @param pin
	 * @return
	 */
	public byte[] fromPinToBytes(String pin) {
		// errors
		if (pin.length() != 4) {
			throw new CommandError(0, "PIN code must be 4 characters long");
		}
		try {
			Integer.parseInt(pin);
		} catch (NumberFormatException exp) {
			throw new CommandError(0, "PIN code is not a valid number");
		}
		
		ByteBuffer buffer = ByteBuffer.allocate(4);
		for (char c : pin.toCharArray()) {
			int i = Integer.valueOf(Character.valueOf(c).toString());
			buffer.put((byte) i);
		}
		
		return buffer.array();
	}

	public boolean isWithPIN() {
		return withPIN;
	}
}
