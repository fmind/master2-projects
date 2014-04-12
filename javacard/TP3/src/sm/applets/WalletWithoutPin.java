package sm.applets;

import javacard.framework.APDU;
import javacard.framework.Applet;
import javacard.framework.ISO7816;
import javacard.framework.ISOException;

public class WalletWithoutPin extends Applet {
	/* CONSTANTS DECLARATION */
	// code of CLA byte in the command APDU header
	final static byte Wallet_CLA = (byte) 0x90;
	// codes of INS byte in the command APDU header
	final static byte VERIFY = (byte) 0x20;
	final static byte CREDIT = (byte) 0x30;
	final static byte DEBIT = (byte) 0x40;
	final static byte GET_BALANCE = (byte) 0x50;
	// maximum balance
	final static short MAX_BALANCE = 0x1388;
	// maximum transaction amount
	final static byte MAX_TRANSACTION_AMOUNT = 100;
	// signal invalid transaction amount
	// amount > MAX_TRANSACTION_AMOUNT or amount < 0
	final static short SW_INVALID_TRANSACTION_AMOUNT = 0x6A83;
	// signal that the balance exceed the maximum
	final static short SW_EXCEED_MAXIMUM_BALANCE = 0x6A84;
	// signal the balance becomes negative
	final static short SW_NEGATIVE_BALANCE = 0x6A85;

	/* INSTANCE VARIABLE DECLARATION */
	short balance;

	private WalletWithoutPin() {
		balance = (short) 0;
		
		register();
	}

	public static void install(byte[] byteArray, short offset, byte length) {
		// create a Wallet applet instance
		new WalletWithoutPin();
	}

	public boolean select() {
		return true;
	}

	public void deselect() {

	}

	public void process(APDU apdu) {
		byte[] buffer = apdu.getBuffer();

		// check SELECT APDU command
		if ((buffer[ISO7816.OFFSET_CLA] == 0)
				&& (buffer[ISO7816.OFFSET_INS] == (byte) (0xA4)))
			return;

		// verify the reset of commands have the correct CLA byte
		if (buffer[ISO7816.OFFSET_CLA] != Wallet_CLA)
			ISOException.throwIt(ISO7816.SW_CLA_NOT_SUPPORTED);

		// dispatch APDU command
		switch (buffer[ISO7816.OFFSET_INS]) {
			case GET_BALANCE:
				getBalance(apdu);
				return;
			case DEBIT:
				debit(apdu);
				return;
			case CREDIT:
				credit(apdu);
				return;
			default:
				ISOException.throwIt(ISO7816.SW_INS_NOT_SUPPORTED);
		}
	}

	private void credit(APDU apdu) {
		byte[] buffer = apdu.getBuffer();
		byte byteRead = (byte)(apdu.setIncomingAndReceive());

		// the number of data bytes read does not match the number in Lc byte
		if (byteRead != 1)
			ISOException.throwIt(ISO7816.SW_WRONG_LENGTH);

		// get the credit amount
		byte creditAmount = buffer[ISO7816.OFFSET_CDATA];

		// check the credit amount
		if ((creditAmount > MAX_TRANSACTION_AMOUNT) || (creditAmount < 0))
			ISOException.throwIt(SW_INVALID_TRANSACTION_AMOUNT);

		// check the new balance
		short new_balance = (short) (balance + creditAmount);
		if (new_balance > MAX_BALANCE)
			ISOException.throwIt(SW_EXCEED_MAXIMUM_BALANCE);

		// credit the amount
		balance = new_balance;
	}

	private void debit(APDU apdu) {
		byte[] buffer = apdu.getBuffer();
		byte byteRead = (byte)(apdu.setIncomingAndReceive());

		// the number of data bytes read does not match the number in Lc byte
		if (byteRead != 1)
			ISOException.throwIt(ISO7816.SW_WRONG_LENGTH);

		// get debit amount
		byte debitAmount = buffer[ISO7816.OFFSET_CDATA];

		// check debit amount
		if ((debitAmount > MAX_TRANSACTION_AMOUNT) || (debitAmount < 0))
			ISOException.throwIt(SW_INVALID_TRANSACTION_AMOUNT);

		// check the new balance
		short new_balance = (short) (balance-debitAmount);
		if (new_balance < 0)
			ISOException.throwIt(SW_NEGATIVE_BALANCE);

		balance = new_balance;
	}

	private void getBalance(APDU apdu) {
		byte[] buffer = apdu.getBuffer();
		
		// inform system that the applet has finished processing the command
		short le = apdu.setOutgoing();
		if (le < 2)
			ISOException.throwIt(ISO7816.SW_WRONG_LENGTH);

		//informs the CAD the actual number of bytes returned
		apdu.setOutgoingLength((byte) 2);

		// move the balance data into the APDU buffer starting at the offset 0
		buffer[0] = (byte)(balance >> 8);
		buffer[1] = (byte)(balance & 0xFF);

		// send the 2-balance byte at the offset 0 in the apdu buffer
		apdu.sendBytes((short) 0, (short) 2);
	}
}
